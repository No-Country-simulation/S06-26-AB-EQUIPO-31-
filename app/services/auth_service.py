# =============================================================================
# app/services/auth_service.py
# Regras de negócio do registo — não sabe nada de HTTP nem de banco directamente
# =============================================================================
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, RegisterResponse, UserResponse, UserProfileResponse
from app.core.security import create_access_token
from app.core.security import verify_password  # já tens este import
from app.schemas.user import LoginRequest, LoginResponse

class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register(self, data: UserCreate) -> RegisterResponse:
        # Regra de negócio: email único
        if self.repo.email_exists(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este email já está registado.",
            )

        user = self.repo.create(data)
        token = create_access_token(user.id)

        return RegisterResponse(
            token=token,
            user=UserResponse.model_validate(user),
            profile=UserProfileResponse.model_validate(user.profile),
        )

    def login(self, data: LoginRequest) -> LoginResponse:
        # 1. Verifica se o email existe
        user = self.repo.get_by_email(data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou password incorrectos.",
            )
    
        # 2. Verifica a password
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou password incorrectos.",  # mesma mensagem — não revela qual está errado
            )
    
        # 3. Verifica se a conta está activa
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Conta desactivada. Contacta o suporte.",
            )
    
        token = create_access_token(user.id)
    
        return LoginResponse(
            token=token,
            user=UserResponse.model_validate(user),
            profile=UserProfileResponse.model_validate(user.profile),
        )
        
    