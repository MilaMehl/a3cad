# app/models/__init__.py
from app.models.user import User, Professor, Aluno
from app.models.avaliacao import Avaliacao, RespostaAluno

__all__ = ["User", "Professor", "Aluno", "Avaliacao", "RespostaAluno"]
