# =============================================================================
# app/models/course.py
# Cursos e trilhas de formação — suporta o endpoint /orientar
# =============================================================================
from sqlalchemy import String, Text, Boolean, Float, ForeignKey, ARRAY, Enum, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.models.base import Base
from app.models.user import LevelEnum
import enum

class CourseTypeEnum(str, enum.Enum):
    free    = "free"    # Google GEAR, Oracle ONE
    paid    = "paid"


class CourseProgressEnum(str, enum.Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed   = "completed"


class Course(Base):
    """
    Curso disponível na plataforma.
    O agente recomenda cursos baseado no gap identificado.
    """
    __tablename__ = "courses"

    id:             Mapped[int]            = mapped_column(primary_key=True, index=True)
    title:          Mapped[str]            = mapped_column(String(255), nullable=False)
    provider:       Mapped[str]            = mapped_column(String(100), nullable=False)  # Google, Oracle, Alura...
    description:    Mapped[str | None]     = mapped_column(Text, nullable=True)
    skills_covered: Mapped[list[str]]      = mapped_column(ARRAY(String), default=list, nullable=False)
    level:          Mapped[LevelEnum]      = mapped_column(Enum(LevelEnum), nullable=False)
    course_type:    Mapped[CourseTypeEnum] = mapped_column(Enum(CourseTypeEnum), nullable=False)
    duration_hours: Mapped[float | None]   = mapped_column(Float, nullable=True)
    url:            Mapped[str | None]     = mapped_column(String(500), nullable=True)
    is_active:      Mapped[bool]           = mapped_column(Boolean, default=True)
    language:       Mapped[str]            = mapped_column(String(5), default="pt")  # pt | es

    enrollments: Mapped[list["UserCourse"]] = relationship(back_populates="course", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Course id={self.id} title={self.title} provider={self.provider}>"


class UserCourse(Base):
    """
    Matrícula e progresso de um utilizador num curso.
    """
    __tablename__ = "user_courses"

    id:          Mapped[int]                 = mapped_column(primary_key=True, index=True)
    user_id:     Mapped[int]                 = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id:   Mapped[int]                 = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    progress:    Mapped[CourseProgressEnum]  = mapped_column(Enum(CourseProgressEnum), default=CourseProgressEnum.not_started)
    completed_at:Mapped[datetime | None]     = mapped_column(DateTime(timezone=True), nullable=True)

    user:   Mapped["User"]   = relationship(back_populates="enrolled_courses")
    course: Mapped["Course"] = relationship(back_populates="enrollments")

    def __repr__(self) -> str:
        return f"<UserCourse user={self.user_id} course={self.course_id} progress={self.progress}>"
