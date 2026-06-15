# =============================================================================
# app/services/auth_service.py
# Regras de negócio do registo — não sabe nada de HTTP nem de banco directamente
# =============================================================================
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, RegisterResponse, UserResponse, UserProfileResponse
from app.core.security import create_access_token


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
