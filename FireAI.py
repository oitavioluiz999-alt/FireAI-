import streamlit as st
import google.generativeai as genai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="FireAI - Terminal", page_icon="🔥", layout="centered")

# --- ESTILO HACKER (CSS) ---
st.markdown("""
    <style>
    /* Fundo e texto principal */
    .stApp {
        background-color: #0d0d0d;
        color: #00ff41;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Estilização das mensagens */
    .stChatMessage {
        background-color: #1a1a1a;
        border: 1px solid #00ff41;
        border-radius: 5px;
        margin-bottom: 10px;
        box-shadow: 0 0 10px #00ff4133;
    }

    /* Input de texto */
    .stChatInput input {
        background-color: #000 !important;
        color: #00ff41 !important;
        border: 1px solid #00ff41 !important;
    }

    /* Títulos e textos */
    h1, h2, h3 {
        color: #00ff41 !important;
        text-shadow: 0 0 15px #00ff41;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Esconder o menu padrão do Streamlit para parecer um app nativo */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DA API ---
# Puxando dos Secrets para segurança total
genai.configure(api_key=st.secrets["AIzaSyARLr_k733N1NtwNUzY3T9dSISrjlIZkzc"])

# Inicializando o modelo (Gemini 2.5 Flash que você descobriu)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="Você é o FireAI, um sistema operacional hacker avançado. Responda como se fosse um terminal de computador antigo, mas seja prestativo. Use termos como 'ACESSO CONCEDIDO', 'EXECUTANDO...' e emojis de fogo."
)

st.title("🔥 FIRE_AI: TERMINAL_v2.5")
st.markdown("---")

# --- LÓGICA DO CHAT ---
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Exibir histórico com estilo hacker
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(f"**[{role.upper()}]:** {message.parts[0].text}")

# Input do usuário
if prompt := st.chat_input("LOGIN:"):
    with st.chat_message("user"):
        st.markdown(f"**[USER]:** {prompt}")

    try:
        with st.chat_message("assistant"):
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown(f"**[SYSTEM]:** {response.text}")
    except Exception as e:
        st.error(f"SYSTEM_ERROR: {e}")
