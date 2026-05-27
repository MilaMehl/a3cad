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
