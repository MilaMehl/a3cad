# app/schemas/__init__.py
from app.schemas.avaliacao import (
    AvaliacaoCreate,
    AvaliacaoResponse,
    RespostaAlunoCreate,
    RespostaAlunoResponse,
)
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    ProfessorCreate,
    ProfessorResponse,
    AlunoCreate,
    AlunoResponse,
    LoginRequest,
    TokenResponse,
    ChangePasswordRequest
)

__all__ = [
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "ProfessorCreate",
    "ProfessorResponse",
    "AlunoCreate",
    "AlunoResponse",
    "LoginRequest",
    "TokenResponse",
    "ChangePasswordRequest",
    "AvaliacaoCreate",
    "AvaliacaoResponse",
    "RespostaAlunoCreate",
    "RespostaAlunoResponse",
]
