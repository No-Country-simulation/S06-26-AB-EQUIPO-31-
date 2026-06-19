# =============================================================================
# app/main.py
# Entrada da aplicação — só inicializa e regista routers
# =============================================================================

from fastapi import FastAPI
from app.api.v1.router import router
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="HACKATHON_APPBIT",
    description="Plataforma de orientação para grupos sub-representados",
    version="1.0.0"
)

app.include_router(router)

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}

# Configura o Swagger para usar Bearer token (HTTPBearer) em vez de OAuth2
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi
