#!/bin/bash

# Script de setup rápido para CAD - Corretor Acadêmico Digital

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════╗"
echo "║  CAD - Corretor Acadêmico Digital                      ║"
echo "║  Setup Inicial                                         ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. Criar Virtual Environment
echo -e "${BLUE}[1/4]${NC} Criando Virtual Environment..."
python -m venv venv
echo -e "${GREEN}✓${NC} Virtual Environment criado"
echo ""

# 2. Ativar Virtual Environment
echo -e "${BLUE}[2/4]${NC} Ativando Virtual Environment..."
source venv/bin/activate || . venv/Scripts/activate
echo -e "${GREEN}✓${NC} Virtual Environment ativado"
echo ""

# 3. Instalar dependências
echo -e "${BLUE}[3/4]${NC} Instalando dependências..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
echo -e "${GREEN}✓${NC} Dependências instaladas"
echo ""

# 4. Configurar arquivo .env
if [ ! -f .env ]; then
    echo -e "${BLUE}[4/4]${NC} Configurando arquivo .env..."
    cp .env.example .env
    echo -e "${GREEN}✓${NC} Arquivo .env criado"
    echo ""
    echo -e "${BLUE}⚠️  IMPORTANTE:${NC} Edite o arquivo .env e configure:"
    echo "  - SECRET_KEY (mude para produção)"
    echo "  - DATABASE_URL (se necessário)"
    echo ""
else
    echo -e "${BLUE}[4/4]${NC} Arquivo .env já existe, pulando..."
    echo ""
fi

echo "╔════════════════════════════════════════════════════════╗"
echo "║  ✅ Setup Completo!                                   ║"
echo "╠════════════════════════════════════════════════════════╣"
echo "║  Para iniciar o servidor:                              ║"
echo "║                                                        ║"
echo "║  1. Ativar venv:                                       ║"
echo "║     $ source venv/bin/activate                         ║"
echo "║                                                        ║"
echo "║  2. Iniciar servidor:                                  ║"
echo "║     $ uvicorn app.main:app --reload                    ║"
echo "║                                                        ║"
echo "║  3. Acessar documentação:                              ║"
echo "║     $ http://localhost:8000/docs                       ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
