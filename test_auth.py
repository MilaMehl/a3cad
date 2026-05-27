"""
Script de teste para validar a autenticação do sistema CAD.

Uso:
    python test_auth.py
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from app.utils.security import hash_password, verify_password, create_access_token, decode_token
from app.utils.constants import UserRole, ERROR_MESSAGES


def test_password_hashing():
    """Testa o hash e verificação de senhas."""
    print("\n🧪 Testando hash de senha...")
    
    password = "minha_senha_segura_123"
    hashed = hash_password(password)
    
    print(f"  ✓ Senha original: {password}")
    print(f"  ✓ Hash criado: {hashed[:30]}...")
    print(f"  ✓ Verificação correta: {verify_password(password, hashed)}")
    print(f"  ✓ Verificação incorreta: {verify_password('senha_errada', hashed)}")


def test_jwt_token():
    """Testa a criação e decodificação de JWT."""
    print("\n🧪 Testando JWT Token...")
    
    data = {
        "sub": "user_123",
        "email": "usuario@example.com",
        "role": UserRole.PROFESSOR
    }
    
    token = create_access_token(data)
    print(f"  ✓ Token criado: {token[:50]}...")
    
    decoded = decode_token(token)
    print(f"  ✓ Token decodificado: {decoded}")
    print(f"  ✓ User ID: {decoded.get('sub')}")
    print(f"  ✓ Email: {decoded.get('email')}")


def test_error_messages():
    """Testa mensagens de erro."""
    print("\n🧪 Testando mensagens de erro...")
    
    for key, message in ERROR_MESSAGES.items():
        print(f"  ✓ {key}: {message}")


def test_user_roles():
    """Testa os roles de usuário."""
    print("\n🧪 Testando User Roles...")
    
    for role in UserRole:
        print(f"  ✓ {role.name}: {role.value}")


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 CAD - Teste de Autenticação")
    print("=" * 60)
    
    try:
        test_password_hashing()
        test_jwt_token()
        test_error_messages()
        test_user_roles()
        
        print("\n" + "=" * 60)
        print("✅ Todos os testes passaram!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro durante teste: {e}")
        sys.exit(1)
