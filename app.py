import streamlit as st
from google import genai
from audio_recorder_streamlit import audio_recorder
import time

# Configuración visual de la App
st.set_page_config(page_title="SOLARIS AI", page_icon="🔧")

st.title("🛡️ SOLARIS SYSTEM v3.1")
st.write("### DEEPSEEK ARCHITECTURE | DIAGNÓSTICO POR VOZ Y TEXTO")

# Barra lateral para meter la llave sin que nadie la vea
with st.sidebar:
    st.header("Seguridad")
    api_key = st.text_input("Introduce tu API KEY de Google:", type="password")
    st.info("Esta llave activa los núcleos de análisis DeepSeek.")

if api_key:
    try:
        client = genai.Client(api_key=api_key)
        
        # Entrada de texto para fallas comunes
        falla_txt = st.text_input("Describe la falla (ej: humo negro, tirones):")
        
        # El micrófono para que el tío grabe el motor
        st.write("---")
        st.subheader("🔊 Oído Digital: Escuchar Falla")
        audio_bytes = audio_recorder(
            text="Toca para grabar el ruido (5-10 seg)",
            icon_size="3x",
            recording_color="#ff4b4b"
        )

        if st.button("🚀 LANZAR DIAGNÓSTICO SOLARIS"):
            if falla_txt or audio_bytes:
                with st.spinner("Sincronizando con núcleos DeepSeek..."):
                    contenido = []
                    if falla_txt: 
                        contenido.append(f"Falla reportada: {falla_txt}")
                    if audio_bytes: 
                        # Aquí la IA analiza el archivo de audio directamente
                        contenido.append({"inline_data": {"mime_type": "audio/wav", "data": audio_bytes}})
                    
                    response = client.models.generate_content(
                        model="gemini-2.0-flash-exp",
                        config={'system_instruction': "Eres SOLARIS, experto técnico. Diagnostica fallas por texto o sonido."},
                        contents=contenido
                    )
                    
                    st.success("✅ ANÁLISIS COMPLETADO")
                    st.markdown(response.text)
            else:
                st.warning("Bro, describe la falla o graba un audio primero.")
    except Exception as e:
        st.error(f"Fallo de conexión: {e}")
else:
    st.warning("⚠️ Ingresa la clave en la barra lateral para encender el sistema.")
