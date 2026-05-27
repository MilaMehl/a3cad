"""
EXEMPLOS DE USO DA API CAD

Este arquivo contém exemplos de como usar os endpoints da API CAD.
"""

# ============================================================
# 1. AUTENTICAÇÃO - REGISTRAR PROFESSOR
# ============================================================

# POST /api/v1/auth/register/professor
# Content-Type: application/json

{
  "email": "prof.silva@example.com",
  "nome_completo": "Prof. João da Silva",
  "senha": "SenhaSegura@123456",
  "disciplinas": ["Cálculo I", "Cálculo II", "Análise Matemática"],
  "bio": "Professor de Matemática com 15 anos de experiência"
}

# Response (201 Created)
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "prof.silva@example.com",
  "nome_completo": "Prof. João da Silva",
  "role": "professor",
  "ativo": true,
  "data_criacao": "2026-05-27T10:30:00+00:00",
  "data_atualizacao": "2026-05-27T10:30:00+00:00",
  "ultimo_login": null,
  "disciplinas": ["Cálculo I", "Cálculo II", "Análise Matemática"],
  "bio": "Professor de Matemática com 15 anos de experiência"
}


# ============================================================
# 2. AUTENTICAÇÃO - REGISTRAR ALUNO
# ============================================================

# POST /api/v1/auth/register/aluno
# Content-Type: application/json

{
  "email": "aluno.santos@example.com",
  "nome_completo": "Maria dos Santos",
  "senha": "SenhaSegura@123456",
  "matricula": "2024001234",
  "turma": "Turma A - Engenharia"
}

# Response (201 Created)
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "email": "aluno.santos@example.com",
  "nome_completo": "Maria dos Santos",
  "role": "aluno",
  "ativo": true,
  "data_criacao": "2026-05-27T10:35:00+00:00",
  "data_atualizacao": "2026-05-27T10:35:00+00:00",
  "ultimo_login": null,
  "matricula": "2024001234",
  "turma": "Turma A - Engenharia"
}


# ============================================================
# 3. LOGIN
# ============================================================

# POST /api/v1/auth/login
# Content-Type: application/json

{
  "email": "prof.silva@example.com",
  "senha": "SenhaSegura@123456"
}

# Response (200 OK)
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJlbWFpbCI6InByb2Yuc2lsdmFAZXhhbXBsZS5jb20iLCJyb2xlIjoicHJvZmVzc29yIiwiZXhwIjoxNjA3ODg2NDAwfQ.SIGNATURE",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "prof.silva@example.com",
    "nome_completo": "Prof. João da Silva",
    "role": "professor",
    "ativo": true,
    "data_criacao": "2026-05-27T10:30:00+00:00",
    "data_atualizacao": "2026-05-27T10:30:00+00:00",
    "ultimo_login": "2026-05-27T10:40:00+00:00"
  }
}


# ============================================================
# 4. OBTER DADOS DO USUÁRIO AUTENTICADO
# ============================================================

# GET /api/v1/auth/me
# Authorization: Bearer <token_obtido_do_login>

# Response (200 OK)
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "prof.silva@example.com",
  "nome_completo": "Prof. João da Silva",
  "role": "professor",
  "ativo": true,
  "data_criacao": "2026-05-27T10:30:00+00:00",
  "data_atualizacao": "2026-05-27T10:30:00+00:00",
  "ultimo_login": "2026-05-27T10:40:00+00:00"
}


# ============================================================
# 5. MUDAR SENHA
# ============================================================

# POST /api/v1/auth/change-password
# Authorization: Bearer <token>
# Content-Type: application/json

{
  "senha_atual": "SenhaSegura@123456",
  "senha_nova": "NovaSenhaSegura@654321",
  "confirmar_senha": "NovaSenhaSegura@654321"
}

# Response (200 OK)
{
  "message": "Senha alterada com sucesso"
}


# ============================================================
# 6. ROTA PROTEGIDA - EXEMPLO
# ============================================================

# GET /api/v1/protected-example
# Authorization: Bearer <token>

# Response (200 OK)
{
  "message": "Olá, Prof. João da Silva!",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "role": "professor"
}


# ============================================================
# USANDO CURL
# ============================================================

# 1. Registrar Professor
curl -X POST "http://localhost:8000/api/v1/auth/register/professor" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "prof.silva@example.com",
    "nome_completo": "Prof. João da Silva",
    "senha": "SenhaSegura@123456",
    "disciplinas": ["Cálculo I"],
    "bio": "Professor experiente"
  }'

# 2. Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "prof.silva@example.com",
    "senha": "SenhaSegura@123456"
  }'

# 3. Obter Usuário Autenticado
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer <seu_token_aqui>"

# 4. Acessar Rota Protegida
curl -X GET "http://localhost:8000/api/v1/protected-example" \
  -H "Authorization: Bearer <seu_token_aqui>"

# 5. Mudar Senha
curl -X POST "http://localhost:8000/api/v1/auth/change-password" \
  -H "Authorization: Bearer <seu_token_aqui>" \
  -H "Content-Type: application/json" \
  -d '{
    "senha_atual": "SenhaSegura@123456",
    "senha_nova": "NovaSenhaSegura@654321",
    "confirmar_senha": "NovaSenhaSegura@654321"
  }'


# ============================================================
# USANDO PYTHON REQUESTS
# ============================================================

import requests

BASE_URL = "http://localhost:8000/api/v1"

# 1. Registrar Professor
response = requests.post(
    f"{BASE_URL}/auth/register/professor",
    json={
        "email": "prof.silva@example.com",
        "nome_completo": "Prof. João da Silva",
        "senha": "SenhaSegura@123456",
        "disciplinas": ["Cálculo I"],
        "bio": "Professor experiente"
    }
)
print(response.json())

# 2. Login
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={
        "email": "prof.silva@example.com",
        "senha": "SenhaSegura@123456"
    }
)
token = response.json()["access_token"]
print(f"Token: {token}")

# 3. Usar Token em Requisições
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
print(response.json())


# ============================================================
# TRATAMENTO DE ERROS
# ============================================================

# Erro: Email já existe (400)
{
  "error": true,
  "status_code": 400,
  "detail": "Usuário com este email já existe"
}

# Erro: Credenciais inválidas (401)
{
  "error": true,
  "status_code": 401,
  "detail": "Email ou senha incorretos"
}

# Erro: Token inválido (401)
{
  "error": true,
  "status_code": 401,
  "detail": "Token inválido"
}

# Erro: Não autorizado (403)
{
  "error": true,
  "status_code": 403,
  "detail": "Usuário inativo"
}

# Erro: Não encontrado (404)
{
  "error": true,
  "status_code": 404,
  "detail": "Usuário não encontrado"
}
