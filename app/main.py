from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
import logging
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import init_db, get_db
from app.routes import auth_router, avaliacoes_router
from app.models.user import User
from app.routes.auth import get_current_user

# Configurar logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

# Inicializar FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API para Corretor Acadêmico Digital (CAD)"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== INICIALIZAÇÃO ==============

@app.on_event("startup")
async def startup():
    """Executado ao iniciar a aplicação."""
    logger.info(f"🚀 Iniciando {settings.app_name}")
    init_db()
    logger.info("✅ Banco de dados inicializado")


@app.on_event("shutdown")
async def shutdown():
    """Executado ao desligar a aplicação."""
    logger.info(f"🛑 Desligando {settings.app_name}")


# ============== ROTAS PÚBLICAS ==============

@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint.
    Verifica se a API está funcionando.
    """
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version
    }


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint.
    Retorna informações sobre a API.
    """
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "status": "running"
    }


# ============== ROTAS DE AUTENTICAÇÃO ==============

app.include_router(auth_router)
app.include_router(avaliacoes_router)


# ============== ROTAS PROTEGIDAS (Exemplo) ==============

@app.get("/api/v1/protected-example", tags=["example"])
async def protected_example(current_user: User = Depends(get_current_user)):
    """
    Exemplo de rota protegida que requer autenticação.
    """
    return {
        "message": f"Olá, {current_user.nome_completo}!",
        "user_id": current_user.id,
        "role": current_user.role
    }


# ============== CUSTOMIZAR OPENAPI ==============

def custom_openapi():
    """Customiza a documentação OpenAPI."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.app_name,
        version=settings.app_version,
        description="API para correção automática de avaliações usando Inteligência Artificial",
        routes=app.routes,
    )
    
    # Adiciona informações de segurança
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# ============== HANDLER DE ERROS ==============

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}, # Aqui está o segredo: devolvemos o JSON encapsulado na Resposta
    )


# ============== INFORMAÇÕES ADICIONAIS ==============

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
