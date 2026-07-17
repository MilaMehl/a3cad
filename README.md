# CAD — Corretor Acadêmico Digital

Sistema inteligente para correção automática de avaliações dissertativas no ensino superior, utilizando Processamento de Linguagem Natural (PLN) e engenharia de prompt avançada integrada a Grandes Modelos de Linguagem (LLMs).

---

## Sobre o Projeto

O CAD é uma plataforma desenvolvida para automatizar e otimizar o processo de correção de avaliações discursivas, mitigando a subjetividade e o tempo de resposta na correção pedagógica. O sistema oferece:

*   **Análise Semântica Automatizada:** Correção baseada em critérios e gabaritos pré-definidos pelo docente.
*   **Feedback Analítico Personalizado:** Geração de devolutivas detalhadas apontando lacunas de conhecimento e pontos fortes do estudante.
*   **Gestão de Critérios de Avaliação (Rubricas):** Interface para parametrização de pesos, penalidades e critérios específicos por questão.
*   **Gestão de Notas:** Dashboards e relatórios para monitoramento do desempenho da turma.

---

## Arquitetura e Tecnologias

*   **Backend:** FastAPI (Python), SQLAlchemy (ORM), Uvicorn.
*   **Orquestração de IA:** LangChain / OpenAI API (Modelos de Chat e Embeddings).
*   **Persistência de Dados:** SQLite (Desenvolvimento) | PostgreSQL (Produção).
*   **Ambiente e Ferramentas:** Python 3.9+, Virtualenv.

---

## Instalação e Execução

### 1. Clonar e Configurar o Ambiente

Certifique-se de ter o Python 3.9+ instalado em sua máquina.

```bash
# Clonar o repositório
git clone https://github.com/MilaMehl/cad-corretor-academico.git
cd cad-corretor-academico

# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```
### 2. Variáveis de Ambiente

Copie o arquivo de exemplo e configure suas credenciais, incluindo as chaves de API necessárias para a execução dos modelos de IA.
```bash
cp .env.example .env
```
⚠️ Importante: Altere a SECRET_KEY em ambiente de produção e certifique-se de que o arquivo .env está listado no seu .gitignore.

### 3. Execução do Servidor


O banco de dados relacional é inicializado automaticamente via SQLAlchemy na primeira execução.
```bash
# Modo Desenvolvimento (com live-reload)
uvicorn app.main:app --reload

# Modo Produção
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
### Documentação e Uso da API

Com a aplicação em execução, a documentação interativa da API fica disponível nos seguintes endpoints:

Swagger UI (Interativo): http://localhost:8000/docs

ReDoc (Estático): http://localhost:8000/redoc

### Autenticação: Registrar Professor
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register/professor" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "prof@example.com",
    "nome_completo": "João da Silva",
    "senha": "senhaSegura123456",
    "disciplinas": ["Cálculo I", "Álgebra Linear"],
    "bio": "Professor adjunto do departamento de Matemática"
  }'
```
### Autenticação: Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "prof@example.com",
    "senha": "senhaSegura123456"
  }'
```
### Contribuição
Este é um projeto de pesquisa e desenvolvimento de caráter iterativo. Pull Requests, correções em issues e sugestões de arquitetura são bem-vindos.

### Licença
Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.
