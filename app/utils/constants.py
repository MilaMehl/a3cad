from enum import Enum


class UserRole(str, Enum):
    """Tipos/Roles de usuários do sistema."""
    PROFESSOR = "professor"
    ALUNO = "aluno"
    ADMIN = "admin"


class TokenType(str, Enum):
    """Tipos de tokens."""
    BEARER = "bearer"


# Mensagens de erro padrão
ERROR_MESSAGES = {
    "user_not_found": "Usuário não encontrado",
    "invalid_credentials": "Email ou senha incorretos",
    "user_already_exists": "Usuário com este email já existe",
    "token_expired": "Token expirado",
    "token_invalid": "Token inválido",
    "unauthorized": "Não autorizado",
    "forbidden": "Acesso proibido",
    "internal_error": "Erro interno do servidor"
}

# Mensagens de sucesso
SUCCESS_MESSAGES = {
    "login_success": "Login realizado com sucesso",
    "user_created": "Usuário criado com sucesso",
    "user_updated": "Usuário atualizado com sucesso",
    "user_deleted": "Usuário deletado com sucesso"
}
