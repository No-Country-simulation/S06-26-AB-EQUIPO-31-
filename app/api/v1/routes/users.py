# =============================================================================
# Exemplo de uso — como proteger qualquer rota
# =============================================================================

# app/api/v1/routes/users.py  (exemplo de rota protegida)
from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    summary="Perfil do utilizador autenticado",
)
def get_me(current_user: User = Depends(get_current_active_user)):
    """
    Rota protegida — devolve o perfil do utilizador autenticado.
    Qualquer rota protegida segue este padrão.
    """
    return {
        "id":       current_user.id,
        "email":    current_user.email,
        "profile":  {
            "full_name": current_user.profile.full_name,
            "country":   current_user.profile.country,
            "level":     current_user.profile.level,
            "goal":      current_user.profile.goal,
            "skills":    current_user.profile.skills,
        }
    }