# =============================================================================
# app/models/event.py
# Eventos ao vivo/gravados — Experiências Estruturantes + CDRView
# =============================================================================
from sqlalchemy import String, Text, Boolean, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.base import Base
import enum
from datetime import datetime

class EventFormatEnum(str, enum.Enum):
    live        = "live"
    recorded    = "recorded"


class Event(Base):
    """
    Eventos com testemunhos e experiências estruturantes.
    lat/lng permitem filtrar por proximidade via dataset CDRView.
    """
    __tablename__ = "events"

    id:          Mapped[int]              = mapped_column(primary_key=True, index=True)
    title:       Mapped[str]              = mapped_column(String(255), nullable=False)
    description: Mapped[str | None]       = mapped_column(Text, nullable=True)
    speaker:     Mapped[str | None]       = mapped_column(String(255), nullable=True)
    format:      Mapped[EventFormatEnum]  = mapped_column(Enum(EventFormatEnum), nullable=False)
    scheduled_at:Mapped[datetime | None]  = mapped_column(DateTime(timezone=True), nullable=True)
    video_url:   Mapped[str | None]       = mapped_column(String(500), nullable=True)
    is_online:   Mapped[bool]             = mapped_column(Boolean, default=True)

    # Geolocalização para integração CDRView
    country:     Mapped[str | None]  = mapped_column(String(100), nullable=True)
    state:       Mapped[str | None]  = mapped_column(String(100), nullable=True)
    city:        Mapped[str | None]  = mapped_column(String(100), nullable=True)
    lat:         Mapped[float | None]= mapped_column(Float, nullable=True)
    lng:         Mapped[float | None]= mapped_column(Float, nullable=True)

    # Offline support para regiões com baixa conectividade (CDRView)
    offline_content_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    registrations: Mapped[list["EventRegistration"]] = relationship(back_populates="event", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Event id={self.id} title={self.title} format={self.format}>"


class EventRegistration(Base):
    """
    Inscrição de utilizador num evento.
    """
    __tablename__ = "event_registrations"

    id:       Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id:  Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    attended: Mapped[bool]= mapped_column(Boolean, default=False)

    user:  Mapped["User"]  = relationship(back_populates="event_registrations")
    event: Mapped["Event"] = relationship(back_populates="registrations")

    def __repr__(self) -> str:
        return f"<EventRegistration user={self.user_id} event={self.event_id}>"