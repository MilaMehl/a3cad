from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Avaliacao(Base):
    """Modelo de avaliação vinculada a um professor."""
    __tablename__ = "avaliacoes"

    id = Column(String, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(Text, nullable=True)
    instrucoes = Column(Text, nullable=True)
    enunciado = Column(Text, nullable=False)
    gabarito_esperado = Column(Text, nullable=False)
    professor_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    data_atualizacao = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    respostas_aluno = relationship("RespostaAluno", back_populates="avaliacao", cascade="all, delete-orphan")


class RespostaAluno(Base):
    """Modelo de resposta de aluno vinculado a uma avaliação."""
    __tablename__ = "respostas_aluno"

    id = Column(String, primary_key=True, index=True)
    avaliacao_id = Column(String, ForeignKey("avaliacoes.id", ondelete="CASCADE"), nullable=False, index=True)
    aluno_id = Column(String, ForeignKey("alunos.id", ondelete="CASCADE"), nullable=False, index=True)
    texto_resposta = Column(Text, nullable=False)
    nota = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    data_atualizacao = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    avaliacao = relationship("Avaliacao", back_populates="respostas_aluno")
