from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    """
    Dependência injectada nas rotas FastAPI.
    Garante que a sessão é sempre fechada após o request.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
