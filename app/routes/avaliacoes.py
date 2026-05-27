import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.avaliacao import Avaliacao, Gabarito, RespostaAluno
from app.models.user import User, Aluno
from app.routes.auth import get_current_user
from app.schemas.avaliacao import (
    AvaliacaoCreate,
    AvaliacaoResponse,
    GabaritoCreate,
    GabaritoResponse,
    RespostaAlunoCreate,
    RespostaAlunoResponse,
)
from app.utils.constants import UserRole

router = APIRouter(prefix="/api/v1", tags=["avaliações"])


def require_professor(current_user: User) -> User:
    if current_user.role != UserRole.PROFESSOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso permitido apenas para professores"
        )
    return current_user


def require_aluno(current_user: User) -> User:
    if current_user.role != UserRole.ALUNO:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso permitido apenas para alunos"
        )
    return current_user


@router.post("/avaliacoes", response_model=AvaliacaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_avaliacao(
    avaliacao_data: AvaliacaoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cria uma nova avaliação vinculada ao professor logado."""
    require_professor(current_user)

    avaliacao = Avaliacao(
        id=str(uuid.uuid4()),
        titulo=avaliacao_data.titulo,
        descricao=avaliacao_data.descricao,
        professor_id=current_user.id
    )

    db.add(avaliacao)
    db.commit()
    db.refresh(avaliacao)

    return AvaliacaoResponse.model_validate(avaliacao)


@router.get("/avaliacoes", response_model=List[AvaliacaoResponse])
async def listar_avaliacoes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista avaliações. Professores veem as próprias avaliações; alunos veem todas."""
    if current_user.role == UserRole.PROFESSOR:
        avaliacoes = db.query(Avaliacao).filter(Avaliacao.professor_id == current_user.id).all()
    else:
        avaliacoes = db.query(Avaliacao).all()

    return [AvaliacaoResponse.model_validate(avaliacao) for avaliacao in avaliacoes]


@router.post("/gabaritos", response_model=GabaritoResponse, status_code=status.HTTP_201_CREATED)
async def criar_gabarito(
    gabarito_data: GabaritoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cria um gabarito para uma avaliação existente."""
    require_professor(current_user)

    avaliacao = db.query(Avaliacao).filter(Avaliacao.id == gabarito_data.avaliacao_id).first()
    if not avaliacao or avaliacao.professor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avaliação não encontrada ou não pertence ao professor autenticado"
        )

    gabarito = Gabarito(
        id=str(uuid.uuid4()),
        avaliacao_id=gabarito_data.avaliacao_id,
        criterio=gabarito_data.criterio
    )

    db.add(gabarito)
    db.commit()
    db.refresh(gabarito)

    return GabaritoResponse.model_validate(gabarito)


@router.get("/gabaritos", response_model=List[GabaritoResponse])
async def listar_gabaritos(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista gabaritos visíveis ao usuário."""
    if current_user.role == UserRole.PROFESSOR:
        avaliacoes = db.query(Avaliacao.id).filter(Avaliacao.professor_id == current_user.id).subquery()
        gabaritos = db.query(Gabarito).filter(Gabarito.avaliacao_id.in_(avaliacoes)).all()
    else:
        gabaritos = db.query(Gabarito).all()

    return [GabaritoResponse.model_validate(gabarito) for gabarito in gabaritos]


@router.post("/respostas", response_model=RespostaAlunoResponse, status_code=status.HTTP_201_CREATED)
async def criar_resposta_aluno(
    resposta_data: RespostaAlunoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cria uma resposta do aluno para uma avaliação."""
    require_aluno(current_user)

    aluno = db.query(Aluno).filter(Aluno.user_id == current_user.id).first()
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de aluno não encontrado"
        )

    avaliacao = db.query(Avaliacao).filter(Avaliacao.id == resposta_data.avaliacao_id).first()
    if not avaliacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avaliação não encontrada"
        )

    resposta = RespostaAluno(
        id=str(uuid.uuid4()),
        avaliacao_id=resposta_data.avaliacao_id,
        aluno_id=aluno.id,
        texto_resposta=resposta_data.texto_resposta,
        nota=None,
        feedback=None
    )

    db.add(resposta)
    db.commit()
    db.refresh(resposta)

    return RespostaAlunoResponse.model_validate(resposta)


@router.get("/respostas", response_model=List[RespostaAlunoResponse])
async def listar_respostas(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista respostas de acordo com o perfil do usuário."""
    if current_user.role == UserRole.ALUNO:
        aluno = db.query(Aluno).filter(Aluno.user_id == current_user.id).first()
        if not aluno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil de aluno não encontrado"
            )
        respostas = db.query(RespostaAluno).filter(RespostaAluno.aluno_id == aluno.id).all()
    else:
        avaliacoes = db.query(Avaliacao.id).filter(Avaliacao.professor_id == current_user.id).subquery()
        respostas = db.query(RespostaAluno).filter(RespostaAluno.avaliacao_id.in_(avaliacoes)).all()

    return [RespostaAlunoResponse.model_validate(resposta) for resposta in respostas]
