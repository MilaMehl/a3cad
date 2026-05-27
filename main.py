"""
CAD - Corretor Acadêmico Digital
API para correção automática de avaliações dissertativas usando Inteligência Artificial

Para iniciar a aplicação:
    uvicorn app.main:app --reload

Para ver a documentação:
    http://localhost:8000/docs

Estrutura do Projeto:
    app/
    ├── main.py              # Aplicação FastAPI principal
    ├── core/                # Configurações e banco de dados
    ├── models/              # Modelos SQLAlchemy
    ├── schemas/             # Schemas Pydantic
    ├── routes/              # Endpoints/Rotas
    └── utils/               # Utilitários (segurança, constantes, etc)
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))
