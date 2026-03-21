import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="FireAI", page_icon="🔥", layout="wide")

# --- CONFIGURAÇÃO DA API ---
# Certifique-se de que instalou/atualizou: pip install -U google-generativeai
MINHA_CHAVE = "AIzaSyARLr_k733N1NtwNUzY3T9dSISrjlIZkzc" 
genai.configure(api_key=MINHA_CHAVE)

# Modelo para Chat
chat_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="Seu nome é FireAI. Você é um assistente parceiro e técnico. Ajude com textos, imagens e vídeos."
)

# --- LOGIN (SIMPLIFICADO) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True

# --- ÁREA DO CHAT ---
st.title("🔥 FIRE_AI MULTIMÍDIA")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico (Texto, Imagem e Vídeo)
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if m.get("type") == "text":
            st.markdown(m["content"])
        elif m.get("type") == "image":
            st.image(m["content"], caption="Gerado pelo FireAI")
        elif m.get("type") == "video":
            st.video(m["content"])

# Input do usuário
if prompt := st.chat_input("Peça um texto, imagem ou vídeo..."):
    st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            p_low = prompt.lower()
            
            # --- 1. LÓGICA DE VÍDEO ---
            if any(x in p_low for x in ["vídeo", "video", "filme"]):
                st.write("🎬 Iniciando rendering de vídeo...")
                try:
                    # O modelo de vídeo (Veo) pode requerer acesso específico no Google AI Studio
                    video_model = genai.GenerativeModel("veo") 
                    video_res = video_model.generate_video(prompt=prompt)
                    video_uri = video_res.videos[0].uri
                    st.video(video_uri)
                    st.session_state.messages.append({"role": "assistant", "content": video_uri, "type": "video"})
                except Exception as ve:
                    st.warning("⚠️ O motor de vídeo (Veo) ainda não está liberado na sua chave API. Tente pedir uma imagem!")

            # --- 2. LÓGICA DE IMAGEM (FORMA CORRETA) ---
            elif any(x in p_low for x in ["imagem", "desenhe", "foto", "ilustração"]):
                st.write("🎨 Gerando arte...")
                try:
                    # Chamada correta para o Imagen 3 no SDK padrão
                    img_model = genai.GenerativeModel("imagen-3.0-generate-001")
                    response = img_model.generate_content(prompt)
                    
                    # Extraindo os bytes da imagem gerada
                    img_bytes = response.candidates[0].content.parts[0].inline_data.data
                    st.image(img_bytes)
                    st.session_state.messages.append({"role": "assistant", "content": img_bytes, "type": "image"})
                except Exception as ie:
                    st.error(f"Erro no motor de imagem: {ie}")
                    st.info("Dica: Verifique se 'Imagen' está ativo no seu Google AI Studio.")

            # --- 3. LÓGICA DE TEXTO ---
            else:
                response = chat_model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text, "type": "text"})
                
    except Exception as e:
        st.error(f"Erro no sistema: {e}")
