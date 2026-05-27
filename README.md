# CAD - Corretor Acadêmico Digital 📚

Sistema inteligente para correção automática de avaliações dissertativas no ensino superior, utilizando Processamento de Linguagem Natural (PLN) e integração com modelos de IA.

## 🎯 Sobre o Projeto

O **CAD** é uma plataforma web desenvolvida para automatizar o processo de correção de avaliações, oferecendo:
- ✅ Correção automática com IA
- ✅ Feedback detalhado e personalizado
- ✅ Gestão de notas e critérios
- ✅ Interface intuitiva para professores e alunos

## 🏗️ Arquitetura

```
CAD (Corretor Acadêmico Digital)
├── Backend: FastAPI + SQLAlchemy
├── Frontend: Streamlit ou React
├── IA: OpenAI API / LangChain
└── BD: SQLite + PostgreSQL (produção)
```

## 📋 Requisitos

- Python 3.9+
- pip (gerenciador de pacotes)
- Virtualenv (recomendado)

## 🚀 Setup Inicial

### 1. Clonar e Configurar Ambiente

```bash
# Criar virtual environment
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env com suas configurações
# Importante: Mudar SECRET_KEY para produção!
```

### 3. Inicializar Banco de Dados

O banco é criado automaticamente na primeira execução.

### 4. Executar a Aplicação

```bash
# Desenvolvimento (com auto-reload)
uvicorn app.main:app --reload

# Produção (porta 8000, sem reload)
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📖 Documentação da API

Após iniciar a aplicação:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📦 PASSO 1 - Implementado ✅

### Setup e Autenticação

- ✅ Estrutura de diretórios FastAPI
- ✅ Configuração com Pydantic Settings
- ✅ SQLAlchemy ORM com SQLite
- ✅ Modelos de Usuários (User, Professor, Aluno)
- ✅ Autenticação JWT
- ✅ Hash de senha com bcrypt
- ✅ Endpoints de registro e login
- ✅ Dependency injection para rotas protegidas

### Endpoints Disponíveis

#### Autenticação
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/register/professor` - Registrar professor
- `POST /api/v1/auth/register/aluno` - Registrar aluno
- `GET /api/v1/auth/me` - Obter dados do usuário autenticado
- `POST /api/v1/auth/change-password` - Mudar senha

#### Saúde
- `GET /health` - Health check
- `GET /` - Informações da API

## 🔐 Segurança

- ✅ Senhas hash com bcrypt
- ✅ JWT para autenticação
- ✅ Validação de email com EmailStr (Pydantic)
- ✅ CORS configurável
- ✅ Dependency injection para proteção de rotas

## 🗂️ Estrutura do Projeto

```
a3cad/
├── app/
│   ├── __init__.py
│   ├── main.py                 # App FastAPI principal
│   ├── core/
│   │   ├── config.py          # Configurações (Pydantic Settings)
│   │   └── database.py        # SQLAlchemy setup
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py            # Modelos: User, Professor, Aluno
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py            # Schemas Pydantic para validação
│   ├── routes/
│   │   ├── __init__.py
│   │   └── auth.py            # Endpoints de autenticação
│   └── utils/
│       ├── __init__.py
│       ├── security.py        # JWT, hash, etc
│       └── constants.py       # Constantes e mensagens
├── main.py                     # Entry point
├── requirements.txt            # Dependências
├── .env.example               # Exemplo de variáveis de ambiente
└── README.md                  # Este arquivo
```

## 🧪 Testando a API

### Exemplo: Registrar Professor

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register/professor" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "prof@example.com",
    "nome_completo": "João da Silva",
    "senha": "senha123456",
    "disciplinas": ["Matemática", "Física"],
    "bio": "Professor experiente"
  }'
```

### Exemplo: Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "prof@example.com",
    "senha": "senha123456"
  }'
```

## 📅 Próximos Passos

- **PASSO 2**: Modelagem de Avaliações (Provas, Gabaritos, Respostas)
- **PASSO 3**: Integração com IA (OpenAI/LangChain)
- **PASSO 4**: Painéis do Professor e do Aluno

## 📝 Convenções de Código

- **Nomenclatura**: snake_case para variáveis/funções, PascalCase para classes
- **Docstrings**: Google-style docstrings
- **Type Hints**: Sempre usar type hints
- **Tests**: Cobertura mínima de 80%

## 🤝 Contribuição

Este é um projeto de desenvolvimento iterativo. Sugestões e correções são bem-vindas!

## 📄 Licença

MIT License

---

**Desenvolvido com ❤️ para o ensino superior**
