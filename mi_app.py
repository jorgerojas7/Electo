import streamlit as st
import pandas as pd # Se mantiene por si es necesario para db_ops, aunque no directamente aquí
import importlib.util 
import sys 
import os 

# Importar funciones de la base de datos de usuarios
from utils.db_ops import init_db, verify_user # Solamente necesitamos init_db y verify_user para el login

# NOTA: report_config_loader y sidebar_menu_builder YA NO se importan aquí,
# porque mi_app.py es ahora SOLO la página de login.

# --- Inicialización de la Base de Datos de Usuarios ---
init_db() # Asegura que la tabla de usuarios exista y que el admin por defecto esté creado.

# --- Configuración Inicial del Estado de Sesión (para la autenticación) ---
# Estas variables controlan el estado de autenticación del usuario.
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
# También inicializamos el marcador del reporte seleccionado aquí, para cuando se redirija al dashboard
if 'selected_report_file' not in st.session_state:
    st.session_state.selected_report_file = "home_page_marker" # Marcador para la página de bienvenida

# --- Configuración de la Página de Login ---
st.set_page_config(
    page_title="Login ELECTO - Perrini",
    page_icon="🔒",
    initial_sidebar_state="collapsed", # Asegura que el sidebar esté colapsado o invisible en la página de login
    layout="centered" # Diseño centrado para el formulario de login
)

# --- CSS para OCULTAR COMPLETAMENTE el sidebar, footer y header en la página de login ---
# Esto es CRUCIAL para una experiencia de login limpia y sin elementos de Streamlit.
hide_login_ui_css = """
    <style>
        #MainMenu {visibility: hidden;} /* Oculta el menú de hamburguesa de Streamlit */
        footer {visibility: hidden;} /* Oculta el footer "Made with Streamlit" */
        header {visibility: hidden;} /* Oculta el encabezado de Streamlit */
        
        /* Oculta la barra lateral completa */
        [data-testid="stSidebar"] {
            display: none !important;
        }
        /* Ajusta el contenido principal para que ocupe todo el ancho en login */
        section.main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            max-width: 100%; /* Asegura que el contenido use todo el ancho en login */
        }
    </style>
"""

# Aplicar el CSS solo si el usuario NO está logueado
if not st.session_state.logged_in:
    st.markdown(hide_login_ui_css, unsafe_allow_html=True)


# --- Lógica de la Aplicación Streamlit (Página de Acceso) ---

# Si el usuario NO está logueado, muestra el formulario de login
if not st.session_state.logged_in:
    # Usamos columnas para centrar el formulario de login
    col1_login, col2_login, col3_login = st.columns([1, 2, 1])

    with col2_login: 
        st.title("Login ELECTO 🗳️")
        st.write("Por favor, ingresa tus credenciales para acceder a la aplicación.")

        with st.form("login_form"):
            st.subheader("Acceder")
            username_input = st.text_input("Usuario", key="login_username_input")
            password_input = st.text_input("Contraseña", type="password", key="login_password_input")

            if st.form_submit_button("Ingresar"):
                user_info = verify_user(username_input, password_input)
                if user_info:
                    st.session_state.logged_in = True
                    st.session_state.username = user_info["username"]
                    st.session_state.is_admin = user_info["is_admin"]
                    # Redirige a la página principal del dashboard después del login
                    st.success(f"¡Bienvenido, {st.session_state.username}! Redirigiendo al dashboard...")
                    st.switch_page("pages/welcome_dashboard.py")
                else:
                    st.error("Usuario o contraseña incorrectos.")

else:
    # Si el usuario ya está logueado, redirige directamente a la página principal del dashboard
    st.switch_page("pages/welcome_dashboard.py")
