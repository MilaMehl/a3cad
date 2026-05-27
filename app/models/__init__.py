# app/models/__init__.py
from app.models.user import User, Professor, Aluno
from app.models.avaliacao import Avaliacao, Gabarito, RespostaAluno

__all__ = ["User", "Professor", "Aluno", "Avaliacao", "Gabarito", "RespostaAluno"]
