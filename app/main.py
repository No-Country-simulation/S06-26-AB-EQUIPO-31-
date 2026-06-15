# =============================================================================
# app/main.py
# Entrada da aplicação — só inicializa e regista routers
# =============================================================================

from fastapi import FastAPI
from app.api.v1.router import router

app = FastAPI(
    title="HACKATHON_APPBIT",
    description="Plataforma de orientação para grupos sub-representados",
    version="1.0.0"
)

app.include_router(router)

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}