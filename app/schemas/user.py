from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.utils.constants import UserRole


class UserBase(BaseModel):
    """Schema base com campos comuns de usuário."""
    email: EmailStr
    nome_completo: str = Field(..., min_length=3, max_length=255)


class UserCreate(UserBase):
    """Schema para criação de novo usuário."""
    senha: str = Field(..., min_length=8, max_length=255, description="Mínimo 8 caracteres")
    role: UserRole


class UserUpdate(BaseModel):
    """Schema para atualização de usuário."""
    nome_completo: Optional[str] = Field(None, min_length=3, max_length=255)
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    """Schema para retorno de dados de usuário."""
    id: str
    role: UserRole
    ativo: bool
    data_criacao: datetime
    data_atualizacao: datetime
    ultimo_login: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }


class ProfessorCreate(UserCreate):
    """Schema para criação de Professor."""
    disciplinas: Optional[list[str]] = None
    bio: Optional[str] = None


class ProfessorResponse(UserResponse):
    """Schema para retorno de dados de Professor."""
    disciplinas: Optional[list[str]] = None
    bio: Optional[str] = None


class AlunoCreate(UserCreate):
    """Schema para criação de Aluno."""
    matricula: str = Field(..., min_length=5, max_length=50)
    turma: Optional[str] = None


class AlunoResponse(UserResponse):
    """Schema para retorno de dados de Aluno."""
    matricula: str
    turma: Optional[str] = None


# Schemas de Autenticação
class LoginRequest(BaseModel):
    """Schema para requisição de login."""
    email: EmailStr
    senha: str


class TokenResponse(BaseModel):
    """Schema para resposta de token."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # segundos
    user: UserResponse


class ChangePasswordRequest(BaseModel):
    """Schema para mudança de senha."""
    senha_atual: str
    senha_nova: str = Field(..., min_length=8, max_length=255)
    confirmar_senha: str
    
    def validate_passwords_match(self):
        """Valida se a senha nova e confirmação são iguais."""
        if self.senha_nova != self.confirmar_senha:
            raise ValueError("Senhas não correspondem")
