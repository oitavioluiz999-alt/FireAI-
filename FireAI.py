import streamlit as st
import google.generativeai as genai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="FireAI", page_icon="🔥", layout="wide")

# --- ESTILO MODERNO E LIMPO (CSS) ---
st.markdown("""
    <style>
    /* Fundo Antracite Profundo (Mais suave que o preto puro) */
    .stApp {
        background: radial-gradient(circle at top, #1e2130 0%, #0f1016 100%);
        color: #e0e0e0;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Sidebar com transparência */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 16, 22, 0.8);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Balões de Chat modernos */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin-bottom: 1rem !important;
    }

    /* Títulos */
    h1 {
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        letter-spacing: -0.5px;
    }
    
    /* Botões Estilo Fire */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        border: none;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        font-weight: bold;
        padding: 0.6rem;
        transition: all 0.4s ease;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3);
    }

    /* Input de Chat */
    .stChatInput input {
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background-color: #1a1c26 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE ACESSO ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def tela_auth():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h1 style='font-size: 3rem;'>🔥 FireAI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888;'>Sua inteligência parceira para execução.</p>", unsafe_allow_html=True)
        st.write("---")
        
        aba_log, aba_reg = st.tabs(["Acessar", "Registrar"])
        
        with aba_log:
            u = st.text_input("Usuário", key="login_user")
            p = st.text_input("Senha", type="password", key="login_pw")
            if st.button("Entrar"):
                st.session_state.logged_in = True
                st.rerun()
        
        with aba_reg:
            st.text_input("E-mail")
            st.text_input("Usuário")
            st.text_input("Senha", type="password")
            st.button("Criar Conta")

if not st.session_state.logged_in:
    tela_auth()
    st.stop()

# --- CONFIGURAÇÃO IA ---
# IMPORTANTE: Coloque sua chave aqui
genai.configure(api_key="AIzaSyARLr_k733N1NtwNUzY3T9dSISrjlIZkzc")

# Personalidade do modelo (Vibe parceira)
system_prompt = (
    "Seu nome é FireAI. Você fala de forma direta, autêntica e inteligente. "
    "Você é um parceiro de projetos do usuário. Use um tom encorajador, mas profissional. "
    "Seja breve e evite enrolação. Mostre que você está no controle técnico."
)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_prompt
)

# --- MENU LATERAL (SIDEBAR) ---
with st.sidebar:
    st.markdown("### 💠 Painel de Controle")
    if st.button("➕ Nova Conversa"):
        st.session_state.messages = []
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
    
    st.divider()
    st.markdown("### 🕒 Histórico")
    st.caption("• Projeto Streamlit")
    st.caption("• Automação Python")
    st.caption("• Design de Interface")
    
    st.sidebar.markdown("---")
    if st.button("🚪 Sair"):
        st.session_state.logged_in = False
        st.rerun()

# --- ÁREA DE MENSAGENS ---
st.markdown("<h1>FIREAI</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_session = model.start_chat(history=[])

# Loop para exibir as mensagens salvas
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Input
if prompt := st.chat_input("Diga o que precisa, parceiro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            resp = st.session_state.chat_session.send_message(prompt)
            st.markdown(resp.text)
            st.session_state.messages.append({"role": "assistant", "content": resp.text})
    except Exception as e:
        st.error(f"Erro no sistema: {e}")
