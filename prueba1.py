import streamlit as st

st.title("¡Hola, Perrini, desde Windows!")
st.write("Esta es mi app de Streamlit funcionando.")

valor = st.slider("Ajusta el valor", 0, 10, 5)
st.write(f"Has seleccionado: {valor}")