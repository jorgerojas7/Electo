import streamlit as st

# --- Configuración Inicial del Estado de Sesión ---
# Streamlit Cloud configurará 'st.session_state.logged_in' después de su proceso de autenticación.
# Aquí, simplemente nos aseguramos de que las variables existan.
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False # Puedes usar esto si en el futuro quieres roles de admin con Google

# --- Configuración de la Página Principal ---
# Esta página no mostrará el sidebar ni el footer si el usuario no está logueado.
st.set_page_config(
    page_title="App Privada de Perrini",
    page_icon="🔒",
    initial_sidebar_state="collapsed", # No se muestra el sidebar en esta página
    layout="centered"
)

# --- CSS para OCULTAR COMPLETAMENTE la barra lateral, menú principal y footer ---
# Esto asegura que no haya rastro del sidebar en la página de login (si el usuario no está logueado).
hide_elements_css = """
    <style>
        #MainMenu {visibility: hidden;} /* Oculta el menú de hamburguesa de Streamlit */
        footer {visibility: hidden;} /* Oculta el footer "Made with Streamlit" */
        header {visibility: hidden;} /* Oculta el encabezado de Streamlit */
        
        /* Oculta la barra lateral completa */
        [data-testid="stSidebar"] {
            display: none !important;
        }
        /* Ajusta el contenido principal para que ocupe todo el ancho */
        section.main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            max-width: 100%;
        }
    </style>
"""

# Si el usuario NO está logueado por Streamlit Cloud, mostramos un mensaje y aplicamos CSS
if not st.session_state.logged_in:
    st.markdown(hide_elements_css, unsafe_allow_html=True)
    st.title("Acceso Requerido 🔒")
    st.write("Por favor, inicia sesión con tu cuenta de Google para acceder a esta aplicación privada.")
    st.info("Esta aplicación requiere autenticación. Serás redirigido a la página de login de Streamlit Cloud.")
    # No se necesita botón de login, Streamlit Cloud lo manejará antes.
    # No hay `st.rerun()` aquí, la autenticación de Streamlit Cloud se encarga de la redirección.
else:
    # Si el usuario ya está logueado por Streamlit Cloud,
    # lo redirigimos directamente a la primera página de reportes.
    st.switch_page("pages/Reporte_1.py") # Asegúrate que esta ruta sea correcta para tu primer reporte
