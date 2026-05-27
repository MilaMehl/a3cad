from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from app.core.config import settings

# Contexto para hash de senha com bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Cria um hash bcrypt da senha."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha corresponde ao hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um JWT token de acesso.
    
    Args:
        data: Dicionário com dados para codificar no token
        expires_delta: Tempo de expiração customizado
        
    Returns:
        String do token JWT
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    
    return encoded_jwt


def decode_token(token: str) -> dict:
    """
    Decodifica e valida um JWT token.
    
    Args:
        token: Token JWT para decodificar
        
    Returns:
        Dicionário com dados decodificados
        
    Raises:
        jwt.InvalidTokenError: Se o token for inválido ou expirado
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return payload
    except jwt.InvalidTokenError as e:
        raise Exception(f"Token inválido ou expirado: {str(e)}")
