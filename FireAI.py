import streamlit as st
import google.generativeai as genai

# 1. Configuração Visual
st.set_page_config(page_title="FireAI - Gemini", page_icon="🔥")
st.title("🔥 FireAI Chat")

# 2. Configurar a API (Substitua pela sua chave real aqui)
GOOGLE_API_KEY = "AIzaSyARLr_k733N1NtwNUzY3T9dSISrjlIZkzc"
genai.configure(api_key=GOOGLE_API_KEY)

# 3. Inicializar o Modelo (Usando o nome estável completo)
# Se der erro 404, trocaremos 'gemini-1.5-flash' por 'gemini-pro'
@st.cache_resource
def load_model():
    return genai.GenerativeModel("gemini-2.5-flash")

model = load_model()

# 4. Gerenciar Histórico
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Exibir mensagens anteriores
for message in st.session_state.chat_session.history:
    with st.chat_message("assistant" if message.role == "model" else "user"):
        st.markdown(message.parts[0].text)

# 5. Lógica do Chat
if prompt := st.chat_input("Como posso ajudar hoje?"):
    st.chat_message("user").markdown(prompt)
    
    try:
        response = st.session_state.chat_session.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Erro na API: {e}")
        st.info("Dica: Se o erro for 404, tente mudar 'gemini-1.5-flash' para 'gemini-1.5-pro' no código.")