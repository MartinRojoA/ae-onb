import streamlit as st
from utils import inference

def main():
    # Título de la aplicación
    st.title("Asistente Virtual de Analytics Engineering")

    # Instrucciones
    st.write(
        "Bienvenido al asistente virtual especializado en Analytics Engineering. "
        "Por favor, ingresa tu pregunta y recibirás una respuesta generada por el modelo."
    )

    # Entrada de texto para la pregunta del usuario
    pregunta = st.text_input("¿Cuál es tu pregunta?")

    if pregunta:
        # Obtener la respuesta utilizando la función definida
        respuesta = inference(pregunta)

        # Mostrar la respuesta generada
        st.subheader("Respuesta:")
        st.write(respuesta)

if __name__ == "__main__":
    main()
