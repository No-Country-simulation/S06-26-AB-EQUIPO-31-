# =============================================================================
# app/schemas/user.py
# Validação de entrada e saída — não sabe nada de banco nem de HTTP
# =============================================================================
from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
from typing import Optional
from app.models.user import GenderEnum, EducationEnum, LevelEnum, GoalEnum


class UserCreate(BaseModel):
    """Dados enviados pelo utilizador no registo."""
    # Dados de acesso
    email:    EmailStr
    password: str

    # Dados pessoais
    full_name:  str
    birth_date: Optional[date]   = None
    gender:     Optional[GenderEnum] = None
    whatsapp:   Optional[str]    = None

    # Localização
    continent:  Optional[str]    = None
    country:    str
    state:      Optional[str]    = None
    city:       Optional[str]    = None

    # Dados profissionais
    education:  EducationEnum
    level:      LevelEnum
    tech_area:  Optional[str]    = None
    goal:       GoalEnum
    skills:     list[str]        = []

    # Preferência de idioma
    preferred_language: str = "pt"

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password deve ter no mínimo 8 caracteres")
        return v

    @field_validator("skills")
    @classmethod
    def skills_not_empty_strings(cls, v: list[str]) -> list[str]:
        return [s.strip() for s in v if s.strip()]

    model_config = {"str_strip_whitespace": True}


class UserResponse(BaseModel):
    """O que a API devolve após registo — nunca inclui password."""
    id:    int
    email: str

    model_config = {"from_attributes": True}


class UserProfileResponse(BaseModel):
    """Perfil completo devolvido após registo."""
    id:        int
    full_name: str
    country:   str
    level:     LevelEnum
    goal:      GoalEnum
    skills:    list[str]

    model_config = {"from_attributes": True}


class RegisterResponse(BaseModel):
    """Resposta completa do endpoint POST /auth/register."""
    token:   str
    user:    UserResponse
    profile: UserProfileResponse