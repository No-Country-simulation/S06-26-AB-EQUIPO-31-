# =============================================================================
# app/core/security.py
# Hashing e JWT — responsabilidade única: segurança
# =============================================================================
import hashlib
import base64
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt, JWTError

from app.core.config import settings


def _prepare_password(password: str) -> bytes:
    """
    Faz SHA-256 da password e converte para base64.
    Garante que nunca ultrapassa os 72 bytes do bcrypt.
    """
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.b64encode(digest)  # sempre 44 bytes


def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(_prepare_password(password), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(_prepare_password(plain), hashed.encode("utf-8"))


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

def decode_token(token: str) -> int:
    """
    Decodifica o token JWT e devolve o user_id.
    Lança JWTError se o token for inválido ou expirado.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise JWTError("Token sem subject.")
        return int(user_id)
    except JWTError:
        raise  # propaga para o dependencies.py tratar
