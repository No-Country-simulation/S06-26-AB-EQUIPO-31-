# =============================================================================
# app/api/v1/routes/auth.py
# Camada HTTP — só recebe, delega ao service e devolve
# =============================================================================
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, RegisterResponse, LoginRequest, LoginResponse
from app.services.auth_service import AuthService
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registo de novo utilizador",
)
def register(data: UserCreate, db: Session = Depends(get_db)):
    """
    Cria conta com dados pessoais e profissionais.
    Devolve token JWT + perfil criado.
    """
    return AuthService(db).register(data)

@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Login de utilizador",
)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Autentica o utilizador com email e password.
    Devolve token JWT + perfil.
    """
    return AuthService(db).login(data)