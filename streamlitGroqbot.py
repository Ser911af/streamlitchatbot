import os
from dotenv import load_dotenv
from groq import Groq
import streamlit as st
from streamlit_chat import message  


# Cargar variables de entorno
load_dotenv()

# Obtener la API Key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("La API Key de Groq no está configurada.")

client = Groq(api_key=api_key)

# Función para cargar el prompt desde un archivo
def cargar_prompt(ruta_archivo="prompt.txt"):
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        st.error("⚠️ Error: No se encontró el archivo de prompt.")
        return ""

# Cargar el prompt base
PROMPT_BASE = cargar_prompt()

# Inicializar historial en session_state si no existe
if "historial" not in st.session_state:
    st.session_state.historial = [
        {"role": "system", "content": PROMPT_BASE}
    ]

# --- Interfaz de Streamlit ---
st.title("Asistente Virtual - Sergio")
st.write("Haz tus preguntas sobre tarifas, servicios y más del hotel.")

# Mostrar historial de conversación con streamlit-chat
for i, mensaje in enumerate(st.session_state.historial):
    if mensaje["role"] == "user":
        message(mensaje["content"], is_user=True, key=f"user_{i}")
    elif mensaje["role"] == "assistant":
        message(mensaje["content"], is_user=False, key=f"assistant_{i}")

# Entrada del usuario con `st.chat_input`
pregunta = st.chat_input("Escribe tu pregunta y presiona Enter...")

if pregunta:
    # Agregar pregunta al historial
    st.session_state.historial.append({"role": "user", "content": pregunta})

    st.write("Procesando...")

    try:
        # Llamar a Groq con todo el historial
        chat_completion = client.chat.completions.create(
            messages=st.session_state.historial,
            model="llama-3.3-70b-versatile",
        )

        # Obtener la respuesta
        respuesta = chat_completion.choices[0].message.content

        # Agregar respuesta al historial
        st.session_state.historial.append({"role": "assistant", "content": respuesta})

        # Actualizar la página para mostrar la nueva conversación
        st.rerun()

    except Exception as e:
        st.error(f"Error al obtener la respuesta: {e}")

# Botón para limpiar historial
if st.button("Borrar Historial"):
    st.session_state.historial = [
        {"role": "system", "content": PROMPT_BASE}
    ]
    st.rerun()
