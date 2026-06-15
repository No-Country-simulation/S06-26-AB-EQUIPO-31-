# =============================================================================
# app/models/user.py
# Dados pessoais + profissionais do utilizador (onboarding completo)
# =============================================================================
import enum
from sqlalchemy import String, Enum, Date, Boolean, Text, ForeignKey, ARRAY
from datetime import date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.base import Base




class GenderEnum(str, enum.Enum):
    male        = "male"
    female      = "female"
    non_binary  = "non_binary"
    prefer_not  = "prefer_not_to_say"


class EducationEnum(str, enum.Enum):
    high_school     = "high_school"
    technical       = "technical"
    undergraduate   = "undergraduate"
    graduate        = "graduate"
    postgraduate    = "postgraduate"


class LevelEnum(str, enum.Enum):
    student     = "student"
    junior      = "junior"
    mid         = "mid"
    senior      = "senior"


class GoalEnum(str, enum.Enum):
    study           = "study"
    define_path     = "define_path"
    find_job        = "find_job"
    change_career   = "change_career"


class User(Base):
    """
    Identidade e acesso — separado do perfil para ortogonalidade.
    Contém apenas o necessário para autenticação.
    """
    __tablename__ = "users"

    id:             Mapped[int]  = mapped_column(primary_key=True, index=True)
    email:          Mapped[str]  = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password:Mapped[str]  = mapped_column(String(255), nullable=False)
    is_active:      Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified:    Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relações — lazy="select" é o padrão seguro para APIs REST
    profile:             Mapped["UserProfile"]          = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    job_applications:    Mapped[list["JobApplication"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    enrolled_courses:    Mapped[list["UserCourse"]]     = relationship(back_populates="user", cascade="all, delete-orphan")
    mentorship_sessions: Mapped[list["MentorshipSession"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    checkins:            Mapped[list["CheckIn"]]        = relationship(back_populates="user", cascade="all, delete-orphan")
    event_registrations: Mapped[list["EventRegistration"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"


class UserProfile(Base):
    """
    Dados pessoais e profissionais do onboarding.
    Separado de User para não misturar autenticação com perfil.
    """
    __tablename__ = "user_profiles"

    id:         Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id:    Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Dados pessoais
    full_name:      Mapped[str]           = mapped_column(String(255), nullable=False)
    birth_date:     Mapped[date]          = mapped_column(Date, nullable=True)
    gender:         Mapped[GenderEnum]    = mapped_column(Enum(GenderEnum), nullable=True)
    whatsapp:       Mapped[str | None]    = mapped_column(String(20), nullable=True)
    avatar_url:     Mapped[str | None]    = mapped_column(String(500), nullable=True)

    # Localização
    continent:  Mapped[str | None] = mapped_column(String(100), nullable=True)
    country:    Mapped[str]        = mapped_column(String(100), nullable=False)
    state:      Mapped[str | None] = mapped_column(String(100), nullable=True)   # Relevante para BR
    city:       Mapped[str | None] = mapped_column(String(100), nullable=True)
    lat:        Mapped[float | None] = mapped_column(nullable=True)              # Geolocalização CDRView
    lng:        Mapped[float | None] = mapped_column(nullable=True)

    # Dados profissionais
    education:      Mapped[EducationEnum] = mapped_column(Enum(EducationEnum), nullable=False)
    level:          Mapped[LevelEnum]     = mapped_column(Enum(LevelEnum), nullable=False)
    tech_area:      Mapped[str | None]    = mapped_column(String(100), nullable=True)  # backend, frontend, data...
    goal:           Mapped[GoalEnum]      = mapped_column(Enum(GoalEnum), nullable=False)
    skills:         Mapped[list[str]]     = mapped_column(ARRAY(String), default=list, nullable=False)
    bio:            Mapped[str | None]    = mapped_column(Text, nullable=True)
    linkedin_url:   Mapped[str | None]    = mapped_column(String(500), nullable=True)
    github_url:     Mapped[str | None]    = mapped_column(String(500), nullable=True)

    # Preferências
    preferred_language: Mapped[str] = mapped_column(String(5), default="pt", nullable=False)  # pt | es

    user: Mapped["User"] = relationship(back_populates="profile")

    def __repr__(self) -> str:
        return f"<UserProfile user_id={self.user_id} name={self.full_name}>"
