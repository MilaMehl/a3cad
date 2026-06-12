import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.avaliacao import Avaliacao, RespostaAluno
from app.models.user import User, Aluno
from app.routes.auth import get_current_user
from app.schemas.avaliacao import (
    AvaliacaoCreate,
    AvaliacaoResponse,
    RespostaAlunoCreate,
    RespostaAlunoResponse,
)
from app.services.ia_service import corrigir_resposta_com_ia
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
        instrucoes=avaliacao_data.instrucoes,
        enunciado=avaliacao_data.enunciado,
        gabarito_esperado=avaliacao_data.gabarito_esperado,
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

    try:
        resultado = await corrigir_resposta_com_ia(
            resposta_texto=resposta.texto_resposta,
            gabarito_texto=avaliacao.gabarito_esperado,
            descricao_avaliacao=avaliacao.enunciado
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Falha na correção da IA: {str(exc)}"
        )

    resposta.nota = resultado["nota"]
    resposta.feedback = resultado["feedback"]
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
        return [RespostaAlunoResponse.model_validate(resposta) for resposta in respostas]

    avaliacoes = db.query(Avaliacao.id).filter(Avaliacao.professor_id == current_user.id).subquery()
    resposta_rows = (
        db.query(RespostaAluno, User.nome_completo.label("aluno_nome"))
        .join(Aluno, RespostaAluno.aluno_id == Aluno.id)
        .join(User, Aluno.user_id == User.id)
        .filter(RespostaAluno.avaliacao_id.in_(avaliacoes))
        .all()
    )

    resultados = []
    for resposta, aluno_nome in resposta_rows:
        resultados.append(
            RespostaAlunoResponse.model_validate({
                "id": resposta.id,
                "avaliacao_id": resposta.avaliacao_id,
                "aluno_id": resposta.aluno_id,
                "aluno_nome": aluno_nome,
                "texto_resposta": resposta.texto_resposta,
                "nota": resposta.nota,
                "feedback": resposta.feedback,
                "data_criacao": resposta.data_criacao,
                "data_atualizacao": resposta.data_atualizacao,
            })
        )

    return resultados


@router.post("/respostas/{resposta_id}/corrigir", response_model=RespostaAlunoResponse)
async def corrigir_resposta_aluno(
    resposta_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Corrige a resposta do aluno usando IA e salva nota e feedback no banco."""
    require_professor(current_user)

    resposta = db.query(RespostaAluno).filter(RespostaAluno.id == resposta_id).first()
    if not resposta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resposta do aluno não encontrada"
        )

    avaliacao = db.query(Avaliacao).filter(Avaliacao.id == resposta.avaliacao_id).first()
    if not avaliacao or avaliacao.professor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avaliação não encontrada ou não pertence ao professor autenticado"
        )

    try:
        resultado = await corrigir_resposta_com_ia(
            resposta_texto=resposta.texto_resposta,
            gabarito_texto=avaliacao.gabarito_esperado,
            descricao_avaliacao=avaliacao.enunciado
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Falha na correção da IA: {str(exc)}"
        )

    resposta.nota = resultado["nota"]
    resposta.feedback = resultado["feedback"]
    db.add(resposta)
    db.commit()
    db.refresh(resposta)

    return RespostaAlunoResponse.model_validate(resposta)
