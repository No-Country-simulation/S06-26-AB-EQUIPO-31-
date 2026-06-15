# =============================================================================
# app/models/mental_health.py
# Check-ins diários e alertas de crise — suporta o endpoint /saude
# =============================================================================
from sqlalchemy import String, Float, Text, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.models.base import Base
import enum
from datetime import datetime
CVV_THRESHOLD = 4.0  # Constante de negócio centralizada aqui


class HumorEnum(str, enum.Enum):
    happy       = "happy"
    tired       = "tired"
    sad         = "sad"
    anxious     = "anxious"
    overwhelmed = "overwhelmed"
    neutral     = "neutral"


class CheckIn(Base):
    """
    Check-in diário de saúde mental via emoji.
    nota_semanal < CVV_THRESHOLD activa derivação para o CVV.
    """
    __tablename__ = "checkins"

    id:             Mapped[int]       = mapped_column(primary_key=True, index=True)
    user_id:        Mapped[int]       = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    humor:          Mapped[HumorEnum] = mapped_column(Enum(HumorEnum), nullable=False)
    nota_semanal:   Mapped[float]     = mapped_column(Float, nullable=False)       # 0.0 a 10.0
    contexto:       Mapped[str | None]= mapped_column(Text, nullable=True)         # texto livre opcional
    acao_sugerida:  Mapped[str | None]= mapped_column(Text, nullable=True)         # resposta do agente
    derivar_cvv:    Mapped[bool]      = mapped_column(Boolean, default=False, nullable=False)

    user:          Mapped["User"]          = relationship(back_populates="checkins")
    crisis_alert:  Mapped["CrisisAlert | None"] = relationship(back_populates="checkin", uselist=False, cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<CheckIn user={self.user_id} humor={self.humor} nota={self.nota_semanal}>"


class CrisisAlert(Base):
    """
    Registo de situação de crise — criado automaticamente quando
    nota_semanal < CVV_THRESHOLD. Separado para auditoria e LGPD.
    """
    __tablename__ = "crisis_alerts"

    id:          Mapped[int]  = mapped_column(primary_key=True, index=True)
    checkin_id:  Mapped[int]  = mapped_column(ForeignKey("checkins.id", ondelete="CASCADE"), unique=True, nullable=False)
    user_id:     Mapped[int]  = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    nota:        Mapped[float]= mapped_column(Float, nullable=False)
    resolved:    Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    checkin: Mapped["CheckIn"] = relationship(back_populates="crisis_alert")

    def __repr__(self) -> str:
        return f"<CrisisAlert checkin={self.checkin_id} nota={self.nota} resolved={self.resolved}>"
