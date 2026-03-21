import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="FireAI", page_icon="🔥", layout="wide")

# (O CSS permanece o mesmo que o anterior, omitido aqui para focar na lógica)

# --- CONFIGURAÇÃO DA API ---
MINHA_CHAVE = "AIzaSyARLr_k733N1NtwNUzY3T9dSISrjlIZkzc" 
genai.configure(api_key=MINHA_CHAVE)

# Usaremos o modelo gemini-2.5-flash para conversas 
# e o modelo 'imagen-3' (ou similar disponível na sua conta) para fotos
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="Seu nome é FireAI. Você é um assistente parceiro. Se o usuário pedir para gerar uma imagem, use suas capacidades de criação visual."
)

# --- LÓGICA DE LOGIN (Simplificada para o exemplo) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True # Pulando para facilitar o teste

# --- ÁREA DO CHAT ---
st.title("🔥 FIRE_AI VISUAL")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico (Texto e Imagens)
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if m["type"] == "text":
            st.markdown(m["content"])
        elif m["type"] == "image":
            st.image(m["content"], caption="Imagem gerada pelo FireAI")

# Input
if prompt := st.chat_input("Peça uma imagem ou tire uma dúvida..."):
    st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # Lógica: Se o prompt contiver "gere uma imagem" ou "desenhe"
            if "gere uma imagem" in prompt.lower() or "desenhe" in prompt.lower():
                st.write("🎨 Gerando arte para você, parceiro...")
                
                # Chamada para o modelo de imagem (Exemplo usando Imagen)
                img_model = genai.ImageGenerationModel("imagen-3")
                response = img_model.generate_images(prompt=prompt)
                
                # Pegar a primeira imagem gerada
                generated_img = response.images[0]
                
                # Exibir no Streamlit
                st.image(generated_img._pil_image)
                
                # Salvar no histórico
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": generated_img._pil_image, 
                    "type": "image"
                })
            else:
                # Resposta de texto normal
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response.text, 
                    "type": "text"
                })
                
    except Exception as e:
        st.error(f"Erro na geração: {e}")
