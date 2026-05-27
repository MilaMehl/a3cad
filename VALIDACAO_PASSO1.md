"""
✅ CHECKLIST DE VALIDAÇÃO - PASSO 1

Use este checklist para validar se o PASSO 1 está completo e funcionando.
"""

═══════════════════════════════════════════════════════════════
FASE 1: VERIFICAÇÃO DE ARQUIVOS
═══════════════════════════════════════════════════════════════

Estrutura de Diretórios:
☐ app/                         (diretório existe)
☐ app/core/                    (diretório existe)
☐ app/models/                  (diretório existe)
☐ app/schemas/                 (diretório existe)
☐ app/routes/                  (diretório existe)
☐ app/utils/                   (diretório existe)

Arquivos Python:
☐ app/__init__.py              (existe)
☐ app/main.py                  (existe)
☐ app/core/__init__.py         (existe)
☐ app/core/config.py           (existe)
☐ app/core/database.py         (existe)
☐ app/models/__init__.py       (existe)
☐ app/models/user.py           (existe)
☐ app/schemas/__init__.py      (existe)
☐ app/schemas/user.py          (existe)
☐ app/routes/__init__.py       (existe)
☐ app/routes/auth.py           (existe)
☐ app/utils/__init__.py        (existe)
☐ app/utils/security.py        (existe)
☐ app/utils/constants.py       (existe)

Arquivos Raiz:
☐ main.py                      (existe)
☐ requirements.txt             (existe com 16 pacotes)
☐ .env.example                 (existe)
☐ .gitignore                   (existe)
☐ setup.sh                     (existe)
☐ setup.bat                    (existe)
☐ test_auth.py                 (existe)

Documentação:
☐ README.md                    (existe)
☐ ARCHITECTURE_PASSO1.md       (existe)
☐ API_EXAMPLES.md              (existe)
☐ SUMMARY_PASSO1.md            (existe)
☐ 00_LEIA_PRIMEIRO.md          (existe)
☐ TREE.md                      (existe)


═══════════════════════════════════════════════════════════════
FASE 2: SETUP DO AMBIENTE
═══════════════════════════════════════════════════════════════

☐ Executar script de setup:
    Windows: setup.bat
    Linux/Mac: bash setup.sh

OU manual:
☐ Criar virtual environment: python -m venv venv
☐ Ativar virtual environment
☐ Instalar dependências: pip install -r requirements.txt
☐ Copiar arquivo: cp .env.example .env
☐ Editar .env se necessário


═══════════════════════════════════════════════════════════════
FASE 3: INICIAR SERVIDOR
═══════════════════════════════════════════════════════════════

☐ Ativar virtual environment (venv)
☐ Executar: uvicorn app.main:app --reload
☐ Servidor iniciando sem erros
☐ Mensagem no console: "Application startup complete"

═══════════════════════════════════════════════════════════════
FASE 4: TESTAR ENDPOINTS PÚBLICOS
═══════════════════════════════════════════════════════════════

Health Check:
☐ GET http://localhost:8000/health
  └─ Deve retornar: {status: "ok", app: "CAD - ...", version: "0.1.0"}

Root:
☐ GET http://localhost:8000/
  └─ Deve retornar: {name: "CAD - ...", version: "0.1.0", ...}

Swagger UI:
☐ Acessar: http://localhost:8000/docs
  └─ Deve mostrar documentação interativa com todos os endpoints

ReDoc:
☐ Acessar: http://localhost:8000/redoc
  └─ Deve mostrar documentação em formato ReDoc


═══════════════════════════════════════════════════════════════
FASE 5: TESTAR AUTENTICAÇÃO
═══════════════════════════════════════════════════════════════

Registro de Professor:
☐ POST /api/v1/auth/register/professor
  {
    "email": "prof@example.com",
    "nome_completo": "Professor Silva",
    "senha": "SenhaSegura@123456",
    "disciplinas": ["Matemática"],
    "bio": "Professor experiente"
  }
  └─ Deve retornar: 201 Created com dados do professor

Registro de Aluno:
☐ POST /api/v1/auth/register/aluno
  {
    "email": "aluno@example.com",
    "nome_completo": "João Aluno",
    "senha": "SenhaSegura@123456",
    "matricula": "2024001234",
    "turma": "Turma A"
  }
  └─ Deve retornar: 201 Created com dados do aluno

Validação de Dupla:
☐ Tentar registrar com mesmo email novamente
  └─ Deve retornar: 400 "Usuário com este email já existe"

Validação de Senha Fraca:
☐ Registrar com senha < 8 caracteres
  └─ Deve retornar: 422 (Validation Error)


═══════════════════════════════════════════════════════════════
FASE 6: TESTAR LOGIN E JWT
═══════════════════════════════════════════════════════════════

Login com Sucesso:
☐ POST /api/v1/auth/login
  {
    "email": "prof@example.com",
    "senha": "SenhaSegura@123456"
  }
  └─ Deve retornar: 200 OK com:
     - access_token (string JWT)
     - token_type: "bearer"
     - expires_in (em segundos)
     - user (objeto com dados)

Login com Credenciais Erradas:
☐ POST /api/v1/auth/login (com email/senha incorretos)
  └─ Deve retornar: 401 "Email ou senha incorretos"

Copiar Token:
☐ Copiar o valor de "access_token" da resposta
  └─ Este é o JWT que será usado nas próximas requisições


═══════════════════════════════════════════════════════════════
FASE 7: TESTAR ROTAS PROTEGIDAS
═══════════════════════════════════════════════════════════════

Obter Usuário (Autenticado):
☐ GET /api/v1/auth/me
  Com Header: Authorization: Bearer <seu_token>
  └─ Deve retornar: 200 OK com dados do usuário

Sem Token:
☐ GET /api/v1/auth/me (sem Authorization header)
  └─ Deve retornar: 422 (Validation Error)

Token Inválido:
☐ GET /api/v1/auth/me
  Com Header: Authorization: Bearer invalid_token
  └─ Deve retornar: 401 "Token inválido"

Rota Protegida de Exemplo:
☐ GET /api/v1/protected-example
  Com Header: Authorization: Bearer <seu_token>
  └─ Deve retornar: 200 com {message: "Olá, nome!", user_id: "...", role: "..."}


═══════════════════════════════════════════════════════════════
FASE 8: TESTAR MUDANÇA DE SENHA
═══════════════════════════════════════════════════════════════

Mudar Senha com Sucesso:
☐ POST /api/v1/auth/change-password
  Com Header: Authorization: Bearer <seu_token>
  {
    "senha_atual": "SenhaSegura@123456",
    "senha_nova": "NovaSenha@654321",
    "confirmar_senha": "NovaSenha@654321"
  }
  └─ Deve retornar: 200 {"message": "Senha alterada com sucesso"}

Validar Nova Senha no Login:
☐ POST /api/v1/auth/login
  {
    "email": "prof@example.com",
    "senha": "NovaSenha@654321"
  }
  └─ Deve retornar: 200 OK com novo token

Senha Atual Incorreta:
☐ POST /api/v1/auth/change-password (com senha_atual errada)
  └─ Deve retornar: 401 "Senha atual incorreta"

Senhas Novas Diferentes:
☐ POST /api/v1/auth/change-password (senha_nova ≠ confirmar_senha)
  └─ Deve retornar: 422 (Validation Error ou mensagem de erro)


═══════════════════════════════════════════════════════════════
FASE 9: TESTAR BANCO DE DADOS
═══════════════════════════════════════════════════════════════

Arquivo do BD:
☐ Verificar se cad.db foi criado na raiz do projeto

Tabelas Criadas:
☐ Verificar 3 tabelas: users, professores, alunos
  (Usar SQLite Browser ou comando sqlite3)

Dados Inseridos:
☐ Verificar que registros foram inseridos:
  - user na tabela users
  - professor na tabela professores (se professor)
  - aluno na tabela alunos (se aluno)


═══════════════════════════════════════════════════════════════
FASE 10: TESTAR COM PYTHON/REQUESTS
═══════════════════════════════════════════════════════════════

Executar test_auth.py:
☐ python test_auth.py
  └─ Deve passar todos os 4 testes:
     ✓ Testando hash de senha
     ✓ Testando JWT Token
     ✓ Testando mensagens de erro
     ✓ Testando User Roles


═══════════════════════════════════════════════════════════════
FASE 11: VALIDAÇÕES DE CÓDIGO
═══════════════════════════════════════════════════════════════

Type Hints:
☐ Verificar se todos os endpoints têm type hints
  ☐ app/routes/auth.py
  ☐ app/utils/security.py
  ☐ app/schemas/user.py

Docstrings:
☐ Verificar docstrings em funções principais
  ☐ create_access_token()
  ☐ decode_token()
  ☐ hash_password()
  ☐ verify_password()

Validação Pydantic:
☐ EmailStr validando emails incorretos
☐ Senhas validando tamanho mínimo
☐ Enums validando valores permitidos


═══════════════════════════════════════════════════════════════
FASE 12: TESTE FINAL
═══════════════════════════════════════════════════════════════

Fluxo Completo:
☐ 1. Registrar professor com email prof_final@example.com
☐ 2. Registrar aluno com email aluno_final@example.com
☐ 3. Login com professor
☐ 4. Copiar token
☐ 5. Acessar GET /api/v1/auth/me com token
☐ 6. Mudar senha
☐ 7. Fazer login com nova senha
☐ 8. Verificar que todos os passos funcionaram


═══════════════════════════════════════════════════════════════
RESULTADO FINAL
═══════════════════════════════════════════════════════════════

Marque com um X quando confirmar:

FASE 1 ✅
☐ Todos os arquivos existem

FASE 2 ✅
☐ Ambiente configurado

FASE 3 ✅
☐ Servidor iniciado

FASE 4 ✅
☐ Endpoints públicos funcionando

FASE 5 ✅
☐ Autenticação funcionando

FASE 6 ✅
☐ JWT gerado e validado

FASE 7 ✅
☐ Rotas protegidas funcionando

FASE 8 ✅
☐ Mudança de senha funcionando

FASE 9 ✅
☐ Banco de dados criado corretamente

FASE 10 ✅
☐ Testes de autenticação passando

FASE 11 ✅
☐ Código validado

FASE 12 ✅
☐ Fluxo completo funcionando


═══════════════════════════════════════════════════════════════
🎉 PASSO 1 - VALIDADO E PRONTO!
═══════════════════════════════════════════════════════════════

Se todas as fases foram confirmadas ✅, o PASSO 1 está
completamente implementado e pronto para o PASSO 2!

Próximo: Modelagem de Avaliações (Provas, Gabaritos, Respostas)

═══════════════════════════════════════════════════════════════
"""
