"""
GUIA DE ARQUITETURA - PASSO 1: SETUP E AUTENTICAÇÃO

Este documento descreve a arquitetura técnica do PASSO 1 do CAD.
"""

# ============================================================
# 1. ESTRUTURA DE CAMADAS
# ============================================================

A aplicação segue uma arquitetura em camadas bem definida:

┌─────────────────────────────────────────────────────────┐
│                    ROUTES (Endpoints)                   │
│              ↓ (Requisições HTTP)                       │
├─────────────────────────────────────────────────────────┤
│                  SCHEMAS (Validação)                    │
│          (Pydantic - Entrada/Saída)                     │
│              ↓                                           │
├─────────────────────────────────────────────────────────┤
│              UTILS (Negócio/Segurança)                  │
│   (JWT, Hash, Constantes, etc)                          │
│              ↓                                           │
├─────────────────────────────────────────────────────────┤
│              MODELS (Banco de Dados)                    │
│          (SQLAlchemy - ORM)                             │
│              ↓                                           │
├─────────────────────────────────────────────────────────┤
│         DATABASE & CONFIG (Configurações)               │
│              ↓                                           │
├─────────────────────────────────────────────────────────┤
│                 SQLite (Banco de Dados)                 │
└─────────────────────────────────────────────────────────┘


# ============================================================
# 2. FLUXO DE AUTENTICAÇÃO (Login)
# ============================================================

1. Usuário envia credenciais:
   POST /api/v1/auth/login
   {
     "email": "usuario@example.com",
     "senha": "senha_texto_plana"
   }

2. Route (auth.py) recebe a requisição

3. Busca usuário no banco (models.User)

4. Valida senha com bcrypt (utils/security.py):
   - verify_password(senha_texto_plana, hash_no_bd)
   - Retorna True/False

5. Se válido, cria JWT token:
   - Payload: {sub, email, role, exp}
   - Assinado com SECRET_KEY
   - Retorna access_token

6. Cliente armazena token

7. Para próximas requisições:
   Authorization: Bearer <token>

8. Middleware/Dependency valida token:
   - decode_token(token)
   - Verifica assinatura e expiração
   - Extrai user_id
   - Busca usuário no BD

9. Injeta user object na route:
   async def protected_route(current_user: User = Depends(get_current_user))


# ============================================================
# 3. MODELS (SQLAlchemy)
# ============================================================

User (Tabela: users)
├── id: UUID (Primary Key)
├── email: String (Unique, Index)
├── nome_completo: String
├── senha_hash: String (bcrypt)
├── role: Enum (professor, aluno, admin)
├── ativo: Boolean
├── data_criacao: DateTime
├── data_atualizacao: DateTime
└── ultimo_login: DateTime (Nullable)

Professor (Tabela: professores)
├── id: UUID (Primary Key)
├── user_id: String (Foreign Key → users.id)
├── disciplinas: String (JSON stringificado)
├── bio: String
└── data_criacao: DateTime

Aluno (Tabela: alunos)
├── id: UUID (Primary Key)
├── user_id: String (Foreign Key → users.id)
├── matricula: String (Unique, Index)
├── turma: String
└── data_criacao: DateTime


# ============================================================
# 4. SEGURANÇA
# ============================================================

4.1 Hashing de Senha
   - Algoritmo: bcrypt
   - Função: hash_password(senha) → hash
   - Verificação: verify_password(senha_texto, hash) → True/False
   - NUNCA armazenar senha em texto plano

4.2 JWT (JSON Web Tokens)
   - Algoritmo: HS256 (HMAC com SHA-256)
   - Componentes:
     * Header: {"alg": "HS256", "typ": "JWT"}
     * Payload: {"sub": user_id, "email": email, "role": role, "exp": expiration}
     * Signature: HMAC(header.payload, SECRET_KEY)
   - Token formato: header.payload.signature
   - Expiração: 30 minutos (configurável)

4.3 Validação
   - Todo token é validado antes de usar
   - Verifica assinatura
   - Verifica expiração
   - Verifica se usuário existe e está ativo

4.4 Senhas
   - Mínimo 8 caracteres
   - Validado pelo Pydantic (FieldValidator)
   - Recomendação: incluir números, caracteres especiais


# ============================================================
# 5. BANCO DE DADOS
# ============================================================

5.1 Configuração
   - Engine: SQLite (desenvolvimento)
   - URL: sqlite:///./cad.db
   - Arquivo criado na raiz do projeto
   - Auto-create na primeira execução

5.2 Sessão
   - SessionLocal = sessionmaker(bind=engine)
   - Dependency: get_db() - cria nova sessão por requisição
   - Garante isolamento de transações

5.3 Migrations
   - Usar Alembic para versionamento de esquema
   - Comandos:
     * alembic init
     * alembic revision --autogenerate
     * alembic upgrade head


# ============================================================
# 6. VALIDAÇÃO (Pydantic)
# ============================================================

Todos os inputs são validados com Pydantic:

UserCreate
├── email: EmailStr (validação de formato)
├── nome_completo: str (min 3, max 255)
├── senha: str (min 8, max 255)
└── role: Enum (professor, aluno, admin)

LoginRequest
├── email: EmailStr
└── senha: str

TokenResponse
├── access_token: str
├── token_type: str (padrão: bearer)
├── expires_in: int (segundos)
└── user: UserResponse


# ============================================================
# 7. TRATAMENTO DE ERROS
# ============================================================

Todos os erros retornam JSON estruturado:

{
  "error": true,
  "status_code": 400,
  "detail": "Mensagem de erro específica"
}

Status Codes:
- 200 OK - Sucesso
- 201 CREATED - Criado com sucesso
- 400 BAD REQUEST - Validação falhou / dados inválidos
- 401 UNAUTHORIZED - Autenticação falhou / token inválido
- 403 FORBIDDEN - Acesso proibido / usuário inativo
- 404 NOT FOUND - Recurso não encontrado
- 500 INTERNAL SERVER ERROR - Erro do servidor


# ============================================================
# 8. ENDPOINTS
# ============================================================

POST   /api/v1/auth/register/professor
→ Cria novo professor
← ProfessorResponse (201)

POST   /api/v1/auth/register/aluno
→ Cria novo aluno
← AlunoResponse (201)

POST   /api/v1/auth/login
→ Email + Senha
← TokenResponse (200)

GET    /api/v1/auth/me
→ Requer token (Authorization: Bearer)
← UserResponse (200)

POST   /api/v1/auth/change-password
→ Requer token + senhas
← {message} (200)

GET    /health
→ Sem autenticação
← {status, app, version} (200)

GET    /
→ Sem autenticação
← {name, version, docs, status} (200)

GET    /api/v1/protected-example
→ Requer token
← {message, user_id, role} (200)


# ============================================================
# 9. CONFIGURAÇÕES
# ============================================================

app/core/config.py
├── app_name: "CAD - Corretor Acadêmico Digital"
├── app_version: "0.1.0"
├── debug: True (desenvolvimento)
├── database_url: "sqlite:///./cad.db"
├── secret_key: "your-secret-key..." (MUDAR EM PRODUÇÃO!)
├── algorithm: "HS256"
├── access_token_expire_minutes: 30
├── allowed_origins: [...] (CORS)
└── log_level: "INFO"

Arquivo: .env
Exemplo: .env.example


# ============================================================
# 10. BOAS PRÁTICAS IMPLEMENTADAS
# ============================================================

✅ Type Hints - Todos os parâmetros e retornos tipados
✅ Docstrings - Documentação em Google Style
✅ Validação - Schemas Pydantic para entrada/saída
✅ Segurança - Hash bcrypt + JWT
✅ CORS - Configurado para múltiplas origens
✅ DRY - Código reutilizável (Depends, Routers)
✅ Logging - Configurado em startup/shutdown
✅ Error Handling - Erros estruturados em JSON
✅ Config Management - Pydantic Settings com .env
✅ ORM - SQLAlchemy para queries seguras (SQL Injection proof)
✅ Async - Suporte completo a assincronicidade (async/await)
✅ Dependency Injection - FastAPI Depends


# ============================================================
# 11. PRÓXIMO PASSO (PASSO 2)
# ============================================================

Após validar o PASSO 1 (autenticação funcionando), 
passaremos para:

PASSO 2: Modelagem de Avaliações
├── Modelos:
│   ├── Prova (título, descrição, professor_id)
│   ├── Gabarito (prova_id, critério_resposta, pontuação)
│   └── Resposta (aluno_id, prova_id, texto_resposta)
├── Endpoints CRUD para:
│   ├── POST /api/v1/provas (criar prova)
│   ├── GET /api/v1/provas (listar provas)
│   ├── POST /api/v1/provas/{id}/gabarito (criar gabarito)
│   └── POST /api/v1/respostas (submeter resposta)
└── Validações e relações de foreign keys
