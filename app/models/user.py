from sqlalchemy import Column, String, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.sql import func
from app.core.database import Base
from app.utils.constants import UserRole
from datetime import datetime


class User(Base):
    """
    Modelo base de usuário do sistema.
    Tabela: users
    """
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nome_completo = Column(String, nullable=False)
    senha_hash = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, index=True)
    ativo = Column(Boolean, default=True, nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    data_atualizacao = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    ultimo_login = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<User {self.email} - {self.role}>"


class Professor(Base):
    """
    Modelo específico de Professor.
    Tabela: professores
    """
    __tablename__ = "professores"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, unique=True, nullable=False, index=True)
    disciplinas = Column(String, nullable=True)  # JSON stringificado das disciplinas
    bio = Column(String, nullable=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Professor {self.user_id}>"


class Aluno(Base):
    """
    Modelo específico de Aluno.
    Tabela: alunos
    """
    __tablename__ = "alunos"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, unique=True, nullable=False, index=True)
    matricula = Column(String, unique=True, nullable=False, index=True)
    turma = Column(String, nullable=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Aluno {self.matricula}>"
