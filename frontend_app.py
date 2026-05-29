import streamlit as st
import requests
from typing import Optional, Dict, Any

# Configuração da página
st.set_page_config(
    page_title="CAD - Corretor Acadêmico Digital",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuração da API
API_BASE_URL = "http://localhost:8000/api/v1"

# Inicializar session_state
if "token" not in st.session_state:
    st.session_state.token = None
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None


# ============================================================================
# Funções Utilitárias de API
# ============================================================================

def fazer_requisicao(
    metodo: str,
    endpoint: str,
    dados: Optional[Dict[str, Any]] = None,
    usar_token: bool = True
) -> Dict[str, Any]:
    """Wrapper para fazer requisições à API FastAPI."""
    url = f"{API_BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    if usar_token and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    
    try:
        if metodo == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif metodo == "POST":
            response = requests.post(url, json=dados, headers=headers, timeout=10)
        elif metodo == "PUT":
            response = requests.put(url, json=dados, headers=headers, timeout=10)
        elif metodo == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            return {"erro": "Método HTTP inválido"}
        
        return response.json()
    
    except requests.exceptions.ConnectionError:
        return {"erro": "Não foi possível conectar à API. Verifique se o servidor está rodando."}
    except requests.exceptions.Timeout:
        return {"erro": "Requisição expirou. Tente novamente."}
    except Exception as e:
        return {"erro": f"Erro ao comunicar com a API: {str(e)}"}


# ============================================================================
# Tela de Login
# ============================================================================

def tela_login():
    """Tela de autenticação do sistema."""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("---")
        st.title("🔐 CAD - Corretor Acadêmico Digital")
        st.markdown("Sistema de Avaliação e Correção Automática")
        st.markdown("---")
        
        email = st.text_input("📧 Email", placeholder="seu.email@universidade.edu.br")
        senha = st.text_input("🔑 Senha", type="password", placeholder="Digite sua senha")
        
        if st.button("Entrar", use_container_width=True, type="primary"):
            if not email or not senha:
                st.error("❌ Preencha todos os campos!")
                return
            
            with st.spinner("Autenticando..."):
                url = f"{API_BASE_URL}/auth/login"
                payload = {"username": email, "password": senha}
                response = requests.post(url, data=payload, timeout=10)
                resposta = response.json()
            
            if "access_token" in resposta:
                st.session_state.token = resposta["access_token"]
                st.session_state.user_role = resposta.get("role", "aluno")
                st.session_state.user_id = resposta.get("id")
                st.session_state.user_email = resposta.get("email")
                st.success(f"✅ Bem-vindo, {resposta.get('nome', 'usuário')}!")
                st.rerun()
            else:
                st.error(f"❌ Erro no login: {resposta.get('detail', 'Email ou senha inválidos')}")

# ============================================================================
# Painel do Professor
# ============================================================================

def listar_avaliacoes_professor():
    """Lista todas as avaliações criadas pelo professor."""
    resposta = fazer_requisicao("GET", "/avaliacoes")
    
    if "erro" in resposta:
        st.error(f"❌ Erro ao buscar avaliações: {resposta['erro']}")
        return
    
    if not resposta or len(resposta) == 0:
        st.info("📭 Nenhuma avaliação criada ainda.")
        return
    
    st.subheader("📋 Minhas Avaliações")
    for avaliacao in resposta:
        with st.expander(f"📖 {avaliacao.get('titulo', 'Sem título')} (ID: {avaliacao.get('id')})"):
            st.write(f"**Descrição:** {avaliacao.get('descricao', 'Sem descrição')}")
            st.write(f"**Data de Criação:** {avaliacao.get('data_criacao', 'N/A')}")
            st.write(f"**Instruções:** {avaliacao.get('instrucoes', 'Nenhuma')}")


def criar_avaliacao():
    """Formulário para criar nova avaliação."""
    st.subheader("✏️ Cadastrar Nova Avaliação")
    
    titulo = st.text_input("📝 Título da Avaliação")
    descricao = st.text_area("📄 Descrição da Avaliação", height=100)
    instrucoes = st.text_area("📋 Instruções para o Aluno", height=100)
    
    if st.button("Criar Avaliação", type="primary", use_container_width=True):
        if not titulo or not descricao:
            st.error("❌ Preencha pelo menos Título e Descrição!")
            return
        
        dados = {
            "titulo": titulo,
            "descricao": descricao,
            "instrucoes": instrucoes or None
        }
        
        with st.spinner("Criando avaliação..."):
            resposta = fazer_requisicao("POST", "/avaliacoes", dados)
        
        if "id" in resposta:
            st.success(f"✅ Avaliação criada com ID: {resposta['id']}")
            st.session_state.avaliacao_id_criada = resposta['id']
        else:
            st.error(f"❌ Erro ao criar avaliação: {resposta.get('detail', 'Erro desconhecido')}")


def listar_respostas_alunos():
    """Lista todas as respostas de alunos para correção."""
    st.subheader("📥 Respostas dos Alunos")
    
    # Filtro por avaliação (opcional)
    avaliacao_id = st.text_input("🔍 Filtrar por ID da Avaliação (deixe em branco para ver todas)")
    
    endpoint = "/respostas"
    if avaliacao_id:
        endpoint += f"?avaliacao_id={avaliacao_id}"
    
    resposta = fazer_requisicao("GET", endpoint)
    
    if "erro" in resposta:
        st.error(f"❌ Erro ao buscar respostas: {resposta['erro']}")
        return
    
    if not resposta or len(resposta) == 0:
        st.info("📭 Nenhuma resposta encontrada.")
        return
    
    for idx, resposta_aluno in enumerate(resposta):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            status_nota = "✅ Corrigida" if resposta_aluno.get('nota') is not None else "⏳ Pendente"
            st.write(
                f"**{status_nota}** | Aluno: {resposta_aluno.get('aluno_id', 'N/A')} | "
                f"Nota: {resposta_aluno.get('nota', '--')} | "
                f"ID: {resposta_aluno.get('id', 'N/A')}"
            )
        
        with col2:
            if resposta_aluno.get('nota') is None:
                if st.button(
                    "🤖 Corrigir",
                    key=f"corrigir_{idx}",
                    use_container_width=True
                ):
                    corrigir_resposta_aluno(resposta_aluno['id'])
        
        with st.expander(f"📖 Ver Resposta Completa"):
            st.write(f"**Resposta:** {resposta_aluno.get('texto_resposta', 'Vazio')}")
            if resposta_aluno.get('feedback'):
                st.write(f"**Feedback da IA:** {resposta_aluno.get('feedback', 'N/A')}")


def corrigir_resposta_aluno(resposta_id: str):
    """Executa a correção de uma resposta via IA."""
    with st.spinner("🤖 Processando correção com IA (aguarde ~2s)..."):
        resposta = fazer_requisicao("POST", f"/respostas/{resposta_id}/corrigir", {})
    
    if "erro" in resposta:
        st.error(f"❌ Erro ao corrigir: {resposta.get('erro', resposta.get('detail', 'Erro desconhecido'))}")
    elif "nota" in resposta:
        st.success(f"✅ Resposta corrigida! Nota: {resposta['nota']}")
        st.info(f"**Feedback:** {resposta.get('feedback', 'N/A')}")
        st.rerun()
    else:
        st.error(f"❌ Resposta inesperada da API: {resposta}")


def painel_professor():
    """Interface principal do professor."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title(f"👨‍🏫 Painel do Professor")
    
    with col2:
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.token = None
            st.session_state.user_role = None
            st.session_state.user_id = None
            st.session_state.user_email = None
            st.rerun()
    
    st.markdown(f"Logado como: **{st.session_state.user_email}**")
    st.markdown("---")
    
    abas = st.tabs(["📝 Cadastrar Avaliação", "📋 Listar Avaliações", "📥 Corrigir Respostas"])
    
    with abas[0]:
        criar_avaliacao()
    
    with abas[1]:
        listar_avaliacoes_professor()
    
    with abas[2]:
        listar_respostas_alunos()


# ============================================================================
# Painel do Aluno
# ============================================================================

def painel_aluno():
    """Interface principal do aluno."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title(f"👨‍🎓 Painel do Aluno")
    
    with col2:
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.token = None
            st.session_state.user_role = None
            st.session_state.user_id = None
            st.session_state.user_email = None
            st.rerun()
    
    st.markdown(f"Logado como: **{st.session_state.user_email}**")
    st.markdown("---")
    
    st.subheader("📊 Consultar Minha Resposta")
    
    resposta_id = st.text_input(
        "🔍 Digite o ID da sua resposta",
        placeholder="ex: 550e8400-e29b-41d4-a716-446655440000"
    )
    
    if st.button("Buscar", type="primary", use_container_width=True):
        if not resposta_id:
            st.error("❌ Digite o ID da resposta!")
            return
        
        with st.spinner("Buscando resposta..."):
            resposta = fazer_requisicao("GET", f"/respostas/{resposta_id}")
        
        if "erro" in resposta:
            st.error(f"❌ Erro: {resposta['erro']}")
        elif "id" in resposta:
            st.success("✅ Resposta encontrada!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if resposta.get('nota') is not None:
                    st.metric("Nota Final", f"{resposta['nota']}/10.0")
                else:
                    st.warning("⏳ Sua resposta ainda está sendo corrigida.")
            
            with col2:
                st.metric("Status", "✅ Corrigida" if resposta.get('nota') is not None else "⏳ Pendente")
            
            st.markdown("---")
            
            with st.expander("📖 Ver Minha Resposta"):
                st.write(resposta.get('texto_resposta', 'Vazio'))
            
            if resposta.get('feedback'):
                with st.expander("💬 Feedback Detalhado", expanded=True):
                    st.info(resposta['feedback'])
            else:
                st.info("Aguarde o feedback quando a correção for concluída.")
        else:
            st.error("❌ Resposta não encontrada.")


# ============================================================================
# Função Principal (Roteamento)
# ============================================================================

def main():
    """Função principal que controla o fluxo da aplicação."""
    if st.session_state.token is None:
        tela_login()
    elif st.session_state.user_role == "professor":
        painel_professor()
    elif st.session_state.user_role == "aluno":
        painel_aluno()
    else:
        st.error("❌ Role de usuário desconhecida. Faça login novamente.")
        if st.button("Sair"):
            st.session_state.token = None
            st.rerun()


if __name__ == "__main__":
    main()
