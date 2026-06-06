import uuid
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.schemas.user import (
    TokenResponse,
    UserResponse,
    ProfessorCreate,
    ProfessorResponse,
    AlunoCreate,
    AlunoResponse,
    ChangePasswordRequest
)
from app.models.user import User, Professor, Aluno
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token
)
from app.utils.constants import UserRole

router = APIRouter(prefix="/api/v1/auth", tags=["autenticação"])

# Configuração para o FastAPI extrair o token JWT do cabeçalho "Authorization: Bearer"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# ============== AUTENTICAÇÃO ==============

@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Endpoint de login.
    
    Retorna um token JWT para usar nas requisições autenticadas.
    """
    # No padrão OAuth2, o username é usado para receber o email
    user = db.query(User).filter(User.email == credentials.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail incorreto ou usuário não existe"
        )
    
    if not verify_password(credentials.password, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha incorreta"
        )
    
    if not user.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )
    
    # Atualiza último login
    user.ultimo_login = datetime.now(timezone.utc)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Cria o token
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role}
    )
    
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expires_in = int(expires_delta.total_seconds())
    
    return TokenResponse(
        access_token=access_token,
        expires_in=expires_in,
        user=UserResponse.model_validate(user)
    )


# ============== REGISTRO DE PROFESSOR ==============

@router.post("/register/professor", response_model=ProfessorResponse, status_code=status.HTTP_201_CREATED)
async def register_professor(
    professor_data: ProfessorCreate,
    db: Session = Depends(get_db)
):
    """
    Registra um novo professor.
    """
    # Verifica se email já existe
    if db.query(User).filter(User.email == professor_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está em uso"
        )
    
    # Cria novo usuário
    user_id = str(uuid.uuid4())
    user = User(
        id=user_id,
        email=professor_data.email,
        nome_completo=professor_data.nome_completo,
        senha_hash=hash_password(professor_data.senha),
        role=UserRole.PROFESSOR,
        ativo=True
    )
    
    db.add(user)
    db.flush()  # Garante que o user_id está no DB
    
    # Cria perfil de professor
    professor = Professor(
        id=str(uuid.uuid4()),
        user_id=user_id,
        disciplinas=",".join(professor_data.disciplinas) if professor_data.disciplinas else None,
        bio=professor_data.bio
    )
    
    db.add(professor)
    db.commit()
    db.refresh(user)
    db.refresh(professor)
    
    user_data = UserResponse.model_validate(user).model_dump()
    return ProfessorResponse.model_validate({
        **user_data,
        "disciplinas": professor.disciplinas.split(",") if professor.disciplinas else None,
        "bio": professor.bio
    })


@router.post("/register/aluno", response_model=AlunoResponse, status_code=status.HTTP_201_CREATED)
async def register_aluno(
    aluno_data: AlunoCreate,
    db: Session = Depends(get_db)
):
    """
    Registra um novo aluno.
    """
    # Verifica se email já existe
    if db.query(User).filter(User.email == aluno_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está em uso"
        )
    
    # Verifica se matrícula já existe
    if db.query(Aluno).filter(Aluno.matricula == aluno_data.matricula).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Matrícula já registrada"
        )
    
    # Cria novo usuário
    user_id = str(uuid.uuid4())
    user = User(
        id=user_id,
        email=aluno_data.email,
        nome_completo=aluno_data.nome_completo,
        senha_hash=hash_password(aluno_data.senha),
        role=UserRole.ALUNO,
        ativo=True
    )
    
    db.add(user)
    db.flush()
    
    # Cria perfil de aluno
    aluno = Aluno(
        id=str(uuid.uuid4()),
        user_id=user_id,
        matricula=aluno_data.matricula,
        turma=aluno_data.turma
    )
    
    db.add(aluno)
    db.commit()
    db.refresh(user)
    db.refresh(aluno)
    
    user_data = UserResponse.model_validate(user).model_dump()
    return AlunoResponse.model_validate({
        **user_data,
        "matricula": aluno.matricula,
        "turma": aluno.turma
    })

# ============== OBTER USUÁRIO ATUAL ==============

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency que valida o token JWT e retorna o usuário atual.
    """
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou expirado"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    if not user.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )
    
    return user


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Retorna os dados do usuário autenticado.
    """
    return UserResponse.model_validate(current_user)


# ============== MUDANÇA DE SENHA ==============

@router.post("/change-password")
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Permite que o usuário autenticado mude sua senha.
    """
    password_data.validate_passwords_match()
    
    # Verifica senha atual
    if not verify_password(password_data.senha_atual, current_user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha atual incorreta"
        )
    
    # Atualiza a senha
    current_user.senha_hash = hash_password(password_data.senha_nova)
    db.add(current_user)
    db.commit()
    
    return {"message": "Senha alterada com sucesso"}