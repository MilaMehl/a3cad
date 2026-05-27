# app/routes/__init__.py
from app.routes.auth import router as auth_router
from app.routes.avaliacoes import router as avaliacoes_router

__all__ = ["auth_router", "avaliacoes_router"]
