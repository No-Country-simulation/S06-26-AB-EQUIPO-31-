
# =============================================================================
# app/models/mentorship.py
# Mentores e sessões de mentoria — módulo de mentorias
# =============================================================================
from sqlalchemy import String, Text, Boolean, ForeignKey, ARRAY, DateTime, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from app.models.base import Base
import enum


class SessionStatusEnum(str, enum.Enum):
    pending   = "pending"
    confirmed = "confirmed"
    done      = "done"
    cancelled = "cancelled"


class Mentor(Base):
    """
    Mentor registado na plataforma.
    Pode ser um utilizador existente com role especial.
    """
    __tablename__ = "mentors"

    id:         Mapped[int]       = mapped_column(primary_key=True, index=True)
    user_id:    Mapped[int]       = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    bio:        Mapped[str | None]= mapped_column(Text, nullable=True)
    expertise:  Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)
    tech_area:  Mapped[str | None]= mapped_column(String(100), nullable=True)
    is_active:  Mapped[bool]      = mapped_column(Boolean, default=True)
    calendly_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    sessions: Mapped[list["MentorshipSession"]] = relationship(back_populates="mentor", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Mentor id={self.id} user_id={self.user_id}>"


class MentorshipSession(Base):
    """
    Sessão de mentoria entre utilizador e mentor.
    Espírito: "Você quer vir a uma prática comigo?"
    """
    __tablename__ = "mentorship_sessions"

    id:           Mapped[int]                = mapped_column(primary_key=True, index=True)
    user_id:      Mapped[int]                = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    mentor_id:    Mapped[int]                = mapped_column(ForeignKey("mentors.id", ondelete="CASCADE"), nullable=False)
    scheduled_at: Mapped[datetime]           = mapped_column(DateTime(timezone=True), nullable=False)
    status:       Mapped[SessionStatusEnum]  = mapped_column(Enum(SessionStatusEnum), default=SessionStatusEnum.pending)
    notes:        Mapped[str | None]         = mapped_column(Text, nullable=True)
    meeting_url:  Mapped[str | None]         = mapped_column(String(500), nullable=True)

    user:   Mapped["User"]   = relationship(back_populates="mentorship_sessions")
    mentor: Mapped["Mentor"] = relationship(back_populates="sessions")

    def __repr__(self) -> str:
        return f"<MentorshipSession user={self.user_id} mentor={self.mentor_id} at={self.scheduled_at}>"
