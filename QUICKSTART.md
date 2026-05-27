"""
⚡ QUICKSTART - 5 MINUTOS

CAD - Corretor Acadêmico Digital (PASSO 1)
"""

═══════════════════════════════════════════════════════════════════════

1. CONFIGURAR (1 minuto)
═══════════════════════════════════════════════════════════════════════

Windows:
  $ setup.bat

Linux/Mac:
  $ bash setup.sh

Manual:
  $ python -m venv venv
  $ source venv/bin/activate  # Linux/Mac
  $ venv\Scripts\activate.bat  # Windows
  $ pip install -r requirements.txt
  $ cp .env.example .env

═══════════════════════════════════════════════════════════════════════

2. EXECUTAR (1 minuto)
═══════════════════════════════════════════════════════════════════════

$ uvicorn app.main:app --reload

Esperar mensagem: "Application startup complete" ✅

═══════════════════════════════════════════════════════════════════════

3. TESTAR (2 minutos)
═══════════════════════════════════════════════════════════════════════

Abra em seu navegador:
  http://localhost:8000/docs

Clique em "Try it out" e teste:

1. POST /api/v1/auth/register/professor
   {
     "email": "prof@example.com",
     "nome_completo": "Prof Silva",
     "senha": "SenhaSegura@123456",
     "disciplinas": ["Math"],
     "bio": "Bio"
   }
   → Deve retornar 201 ✅

2. POST /api/v1/auth/login
   {
     "email": "prof@example.com",
     "senha": "SenhaSegura@123456"
   }
   → Deve retornar token JWT ✅

3. Copiar o "access_token" da resposta

4. GET /api/v1/auth/me
   (Clique em cadeado no Swagger, cole token)
   → Deve retornar seus dados ✅

═══════════════════════════════════════════════════════════════════════

4. VALIDAR (1 minuto)
═══════════════════════════════════════════════════════════════════════

$ python test_auth.py

Deve aparecer:
  ✅ Todos os testes passaram!

═══════════════════════════════════════════════════════════════════════

✅ PRONTO! PASSO 1 FUNCIONANDO!

Próximo: Ler documentação completa ou prosseguir para PASSO 2

═══════════════════════════════════════════════════════════════════════

📚 DOCUMENTAÇÃO

Visão Completa: 00_LEIA_PRIMEIRO.md
Arquitetura:    ARCHITECTURE_PASSO1.md
Exemplos:       API_EXAMPLES.md
Validação:      VALIDACAO_PASSO1.md

═══════════════════════════════════════════════════════════════════════
"""
