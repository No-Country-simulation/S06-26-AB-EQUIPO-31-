# =============================================================================
# app/models/__init__.py
# Exporta todos os models para o Alembic detectar automaticamente
# =============================================================================
from app.models.base import Base
from app.models.user import User, UserProfile
from app.models.job import Job, JobApplication
from app.models.course import Course, UserCourse
from app.models.mentorship import Mentor, MentorshipSession
from app.models.mental_health import CheckIn, CrisisAlert
from app.models.event import Event, EventRegistration

__all__ = [
    "Base",
    "User", "UserProfile",
    "Job", "JobApplication",
    "Course", "UserCourse",
    "Mentor", "MentorshipSession",
    "CheckIn", "CrisisAlert",
    "Event", "EventRegistration",
]
