import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="FireAI", page_icon="🔥", layout="wide")

# --- CONFIGURAÇÃO DA API ---
# Nota: pip install -U google-generativeai
MINHA_CHAVE = "AIzaSyARLr_k733N1NtwNUzY3T9dSISrjlIZkzc" 
genai.configure(api_key=MINHA_CHAVE)

# DEFINIÇÃO DOS MODELOS DA SUA LISTA (2026)
TEXT_MODEL_NAME = "models/gemini-3-flash-preview"
IMAGE_MODEL_NAME = "models/gemini-3.1-flash-image-preview" # Nano Banana 2
VIDEO_MODEL_NAME = "models/veo" # Verifique se liberado no AI Studio

# --- LÓGICA DE LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True

# --- INICIALIZAÇÃO DO MODELO DE CHAT ---
chat_model = genai.GenerativeModel(
    model_name=TEXT_MODEL_NAME,
    system_instruction="Seu nome é FireAI. Você é um assistente parceiro e técnico. Você domina geração de texto, imagem e vídeo."
)

# --- ÁREA DO CHAT ---
st.title("🔥 FIRE_AI MULTIMÍDIA")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if m.get("type") == "text":
            st.markdown(m["content"])
        elif m.get("type") == "image":
            st.image(m["content"], caption="Gerado pelo FireAI")
        elif m.get("type") == "video":
            st.video(m["content"])

# --- PROCESSAMENTO DO INPUT ---
if prompt := st.chat_input("Peça uma imagem, texto ou vídeo..."):
    st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            p_low = prompt.lower()
            
            # --- 1. LÓGICA DE VÍDEO (VEO) ---
            if any(x in p_low for x in ["vídeo", "video", "filme"]):
                st.write("🎬 Renderizando vídeo com Veo...")
                try:
                    v_model = genai.GenerativeModel(VIDEO_MODEL_NAME)
                    video_res = v_model.generate_video(prompt=prompt)
                    video_uri = video_res.videos[0].uri
                    st.video(video_uri)
                    st.session_state.messages.append({"role": "assistant", "content": video_uri, "type": "video"})
                except Exception:
                    st.warning("⚠️ O motor Veo ainda está em preview restrito para sua chave.")

            # --- 2. LÓGICA DE IMAGEM (NANO BANANA 2) ---
            elif any(x in p_low for x in ["imagem", "desenhe", "foto", "ilustração"]):
                st.write("🎨 Criando arte com Nano Banana 2...")
                try:
                    # Usando o modelo gemini-3.1-flash-image-preview da sua lista
                    img_model = genai.GenerativeModel(IMAGE_MODEL_NAME)
                    response = img_model.generate_content(prompt)
                    
                    # Extraindo bytes da imagem
                    img_bytes = response.candidates[0].content.parts[0].inline_data.data
                    st.image(img_bytes)
                    st.session_state.messages.append({"role": "assistant", "content": img_bytes, "type": "image"})
                except Exception as ie:
                    st.error(f"Erro no motor de imagem: {ie}")

            # --- 3. LÓGICA DE TEXTO (GEMINI 3 FLASH) ---
            else:
                response = chat_model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text, "type": "text"})
                
    except Exception as e:
        st.error(f"Erro no sistema: {e}")
