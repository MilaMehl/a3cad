@echo off
REM Script de setup rápido para CAD - Corretor Acadêmico Digital (Windows)

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║  CAD - Corretor Acadêmico Digital                      ║
echo ║  Setup Inicial (Windows)                               ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM 1. Criar Virtual Environment
echo [1/4] Criando Virtual Environment...
python -m venv venv
if !errorlevel! neq 0 (
    echo Erro ao criar venv
    exit /b 1
)
echo ✓ Virtual Environment criado
echo.

REM 2. Ativar Virtual Environment
echo [2/4] Ativando Virtual Environment...
call venv\Scripts\activate.bat
if !errorlevel! neq 0 (
    echo Erro ao ativar venv
    exit /b 1
)
echo ✓ Virtual Environment ativado
echo.

REM 3. Instalar dependências
echo [3/4] Instalando dependências...
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
if !errorlevel! neq 0 (
    echo Erro ao instalar dependências
    exit /b 1
)
echo ✓ Dependências instaladas
echo.

REM 4. Configurar arquivo .env
echo [4/4] Configurando arquivo .env...
if not exist .env (
    copy .env.example .env
    echo ✓ Arquivo .env criado
    echo.
    echo ⚠️  IMPORTANTE: Edite o arquivo .env e configure:
    echo   - SECRET_KEY ^(mude para produção^)
    echo   - DATABASE_URL ^(se necessário^)
    echo.
) else (
    echo ✓ Arquivo .env já existe, pulando...
    echo.
)

echo ╔════════════════════════════════════════════════════════╗
echo ║  ✅ Setup Completo!                                   ║
echo ╠════════════════════════════════════════════════════════╣
echo ║  Para iniciar o servidor:                              ║
echo ║                                                        ║
echo ║  1. Ativar venv:                                       ║
echo ║     ^> venv\Scripts\activate.bat                        ║
echo ║                                                        ║
echo ║  2. Iniciar servidor:                                  ║
echo ║     ^> uvicorn app.main:app --reload                    ║
echo ║                                                        ║
echo ║  3. Acessar documentação:                              ║
echo ║     http://localhost:8000/docs                         ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.

pause
