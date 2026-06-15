# =============================================================================
# app/models/job.py
# Vagas e candidaturas — suporta o endpoint /orientar
# =============================================================================
from sqlalchemy import String, Text, Float, Integer, ForeignKey, ARRAY, Enum, Boolean
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.models.base import Base
import enum
from app.models.user import LevelEnum


class JobStatusEnum(str, enum.Enum):
    open    = "open"
    closed  = "closed"
    paused  = "paused"


class ApplicationStatusEnum(str, enum.Enum):
    applied     = "applied"
    in_review   = "in_review"
    rejected    = "rejected"
    hired       = "hired"


class Job(Base):
    """
    Vaga de emprego. O serviço de orientação faz o match com o perfil
    e calcula o gap percentual.
    """
    __tablename__ = "jobs"

    id:             Mapped[int]            = mapped_column(primary_key=True, index=True)
    title:          Mapped[str]            = mapped_column(String(255), nullable=False)
    company:        Mapped[str]            = mapped_column(String(255), nullable=False)
    description:    Mapped[str]            = mapped_column(Text, nullable=True)
    required_skills:Mapped[list[str]]      = mapped_column(ARRAY(String), default=list, nullable=False)
    level:          Mapped[LevelEnum]      = mapped_column(Enum(LevelEnum), nullable=False)
    tech_area:      Mapped[str | None]     = mapped_column(String(100), nullable=True)
    country:        Mapped[str]            = mapped_column(String(100), nullable=False)
    state:          Mapped[str | None]     = mapped_column(String(100), nullable=True)
    city:           Mapped[str | None]     = mapped_column(String(100), nullable=True)
    is_remote:      Mapped[bool]           = mapped_column(Boolean, default=False)
    status:         Mapped[JobStatusEnum]  = mapped_column(Enum(JobStatusEnum), default=JobStatusEnum.open)
    source_url:     Mapped[str | None]     = mapped_column(String(500), nullable=True)

    applications: Mapped[list["JobApplication"]] = relationship(back_populates="job", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Job id={self.id} title={self.title} company={self.company}>"


class JobApplication(Base):
    """
    Candidatura de um utilizador a uma vaga.
    Regista o gap calculado no momento da candidatura.
    """
    __tablename__ = "job_applications"

    id:             Mapped[int]                    = mapped_column(primary_key=True, index=True)
    user_id:        Mapped[int]                    = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id:         Mapped[int]                    = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    gap_percentual: Mapped[float]                  = mapped_column(Float, nullable=False)        # ex: 0.30 = 30% de gap
    gap_items:      Mapped[list[str]]              = mapped_column(ARRAY(String), default=list)  # skills em falta
    status:         Mapped[ApplicationStatusEnum]  = mapped_column(Enum(ApplicationStatusEnum), default=ApplicationStatusEnum.applied)
    notes:          Mapped[str | None]             = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship(back_populates="job_applications")
    job:  Mapped["Job"]  = relationship(back_populates="applications")

    def __repr__(self) -> str:
        return f"<JobApplication user={self.user_id} job={self.job_id} gap={self.gap_percentual}>"

