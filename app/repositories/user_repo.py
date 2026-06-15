# =============================================================================
# app/repositories/user_repo.py
# Acesso ao banco — só CRUD, sem regras de negócio
# =============================================================================
from sqlalchemy.orm import Session
from app.models.user import User, UserProfile
from app.schemas.user import UserCreate
from app.core.security import hash_password


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def create(self, data: UserCreate) -> User:
        """
        Cria User + UserProfile numa única transacção.
        O repo não decide nada — só persiste.
        """
        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
        )
        self.db.add(user)
        self.db.flush()  # gera user.id sem fechar a transacção

        profile = UserProfile(
            user_id=user.id,
            full_name=data.full_name,
            birth_date=data.birth_date,
            gender=data.gender,
            whatsapp=data.whatsapp,
            continent=data.continent,
            country=data.country,
            state=data.state,
            city=data.city,
            education=data.education,
            level=data.level,
            tech_area=data.tech_area,
            goal=data.goal,
            skills=data.skills,
            preferred_language=data.preferred_language,
        )
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(user)
        return user

    def email_exists(self, email: str) -> bool:
        return self.get_by_email(email) is not None
