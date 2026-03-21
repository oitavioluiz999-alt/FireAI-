import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="FireAI", page_icon="🔥", layout="wide")

# --- GERENCIAMENTO DE MÚLTIPLAS CHAVES ---
# Adicione suas chaves aqui dentro da lista
LISTA_DE_CHAVES = [
    "AIzaSyARLr_k733N1NtwNUzY3T9dSISrjlIZkzc", 
    "AIzaSyBfk8iFcSa47IkMJl_26LQ9Q8l8UhsMF_I",
    "AIzaSyA9rNROaT3jmVOONZSvKaMNte4BtE28MeM"
]

# MODELOS 2026
TEXT_MODEL = "models/gemini-3-flash-preview"
IMAGE_MODEL = "models/gemini-3.1-flash-image-preview" 
VIDEO_MODEL = "models/veo"

# --- FUNÇÃO MESTRE PARA EXECUTAR COM FALLBACK ---
def executar_com_rodizio(prompt, modelo_nome, modo="texto"):
    """Tenta executar o pedido percorrendo a lista de chaves se houver erro de cota."""
    for i, chave in enumerate(LISTA_DE_CHAVES):
        try:
            genai.configure(api_key=chave)
            model = genai.GenerativeModel(modelo_nome)
            
            # Se for imagem, precisa de uma configuração específica de personalidade às vezes
            if modo == "imagem":
                response = model.generate_content(prompt)
                return response.candidates[0].content.parts[0].inline_data.data
            elif modo == "texto":
                # Configura personalidade apenas para o chat de texto
                chat = genai.GenerativeModel(
                    model_name=modelo_nome,
                    system_instruction="Seu nome é FireAI. Você é um assistente técnico e parceiro."
                )
                response = chat.generate_content(prompt)
                return response.text
            elif modo == "video":
                v_model = genai.GenerativeModel(modelo_nome)
                video_res = v_model.generate_video(prompt=prompt)
                return video_res.videos[0].uri
                
        except Exception as e:
            # Se for erro de cota (429), tenta a próxima chave
            if "429" in str(e) or "quota" in str(e).lower():
                if i < len(LISTA_DE_CHAVES) - 1:
                    st.info(f"🔄 Cota da chave {i+1} esgotada. Alternando motor...")
                    continue
                else:
                    st.error("🚨 Todas as chaves atingiram o limite! Tente novamente em 1 minuto.")
            else:
                # Se for outro tipo de erro, mostra o erro real
                st.error(f"Erro técnico na chave {i+1}: {e}")
                break
    return None

# --- LOGIN (SIMPLIFICADO) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True

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
            
            # 1. LÓGICA DE VÍDEO
            if any(x in p_low for x in ["vídeo", "video", "filme"]):
                st.write("🎬 Renderizando vídeo...")
                res = executar_com_rodizio(prompt, VIDEO_MODEL, modo="video")
                if res:
                    st.video(res)
                    st.session_state.messages.append({"role": "assistant", "content": res, "type": "video"})

            # 2. LÓGICA DE IMAGEM
            elif any(x in p_low for x in ["imagem", "desenhe", "foto", "ilustração"]):
                st.write("🎨 Criando arte...")
                res = executar_com_rodizio(prompt, IMAGE_MODEL, modo="imagem")
                if res:
                    st.image(res)
                    st.session_state.messages.append({"role": "assistant", "content": res, "type": "image"})

            # 3. LÓGICA DE TEXTO
            else:
                res = executar_com_rodizio(prompt, TEXT_MODEL, modo="texto")
                if res:
                    st.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res, "type": "text"})
                
    except Exception as e:
        st.error(f"Erro crítico no sistema: {e}")
