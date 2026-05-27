from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AvaliacaoCreate(BaseModel):
    """Schema para criação de avaliação."""
    titulo: str = Field(..., min_length=3, max_length=255)
    descricao: Optional[str] = Field(None, max_length=2000)


class AvaliacaoResponse(AvaliacaoCreate):
    """Schema para retorno de avaliação."""
    id: str
    professor_id: str
    data_criacao: datetime
    data_atualizacao: datetime

    model_config = {"from_attributes": True}


class GabaritoCreate(BaseModel):
    """Schema para criação de gabarito."""
    avaliacao_id: str
    criterio: str = Field(..., min_length=5)


class GabaritoResponse(GabaritoCreate):
    """Schema para retorno de gabarito."""
    id: str
    data_criacao: datetime
    data_atualizacao: datetime

    model_config = {"from_attributes": True}


class RespostaAlunoCreate(BaseModel):
    """Schema para criação de resposta do aluno."""
    avaliacao_id: str
    texto_resposta: str = Field(..., min_length=10)


class RespostaAlunoResponse(RespostaAlunoCreate):
    """Schema para retorno de resposta do aluno."""
    id: str
    aluno_id: str
    nota: Optional[float] = None
    feedback: Optional[str] = None
    data_criacao: datetime
    data_atualizacao: datetime

    model_config = {"from_attributes": True}
