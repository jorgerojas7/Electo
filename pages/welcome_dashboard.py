import streamlit as st
import pandas as pd
import importlib.util # Para importar módulos dinámicamente
import sys # Para añadir directorios al path de importación
import os # Para construir rutas de archivo

# Importar funciones de la base de datos de usuarios
from utils.db_ops import init_db, verify_user # Solo necesitamos init_db aquí para asegurar que la BD está lista

# Importar funciones para la configuración de reportes (desde JSON)
from utils.report_config_loader import init_reports_data, get_all_reports_config

# Importar la función para construir el sidebar
from utils.sidebar_menu_builder import build_collapsible_sidebar_menu

# --- Inicialización de Base de Datos y Configuración de Reportes ---
init_db() # Asegura que la BD de usuarios esté lista
init_reports_data() # Asegura que el JSON de reportes esté listo

# --- Configuración Inicial del Estado de Sesión para el Contenido del Reporte ---
# Define el marcador para la página de bienvenida.
if 'selected_report_file' not in st.session_state: 
    st.session_state.selected_report_file = "home_page_marker" 

# --- Configuración General de la Página Streamlit ---
st.set_page_config(
    page_title="Dashboard Principal - Perrini",
    page_icon="📊",
    layout="wide", 
    initial_sidebar_state="expanded" # Queremos el sidebar EXPANDIDO por defecto aquí
)

# --- CSS para OCULTAR el footer y el header predeterminados de Streamlit ---
# NOTA: NO hay reglas aquí para ocultar el sidebar principal ni el botón de hamburguesa.
# Es crucial que Streamlit los maneje para la funcionalidad de expandir/colapsar.
hide_elements_css = """
    <style>
        footer {visibility: hidden;} /* Oculta el footer "Made with Streamlit" */
        header {visibility: hidden;} /* Oculta el encabezado de Streamlit */
    </style>
"""
st.markdown(hide_elements_css, unsafe_allow_html=True)

# --- Carga y Aplica el CSS Externo (styles/main.css) ---
# Aquí es donde se cargarán tus estilos personalizados, incluyendo la ocultación del stSidebarNav.
css_file_path = os.path.join("styles", "main.css")
try:
    with open(css_file_path, "r", encoding="utf-8") as f:
        custom_styles_css = f.read()
    st.markdown(f"<style>{custom_styles_css}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.error(f"Error: No se encontró el archivo de estilos CSS en '{css_file_path}'.")
    st.warning("Asegúrate de que el archivo 'main.css' está en la carpeta 'styles/' en la raíz del proyecto.")


# --- Lógica de Seguridad: Redirigir si no está logueado ---
# Si el usuario NO está logueado en la sesión, lo redirigimos a la página de login.
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("No has iniciado sesión. Redirigiendo a la página de acceso...")
    st.switch_page("mi_app.py") # Redirige al login si no está autenticado
    st.stop() # Detiene la ejecución para evitar mostrar contenido no autorizado


# --- Lógica de la Barra Lateral (Sidebar) ---
# Construye el menú personalizado del sidebar.
build_collapsible_sidebar_menu() 

# --- Función para Mostrar el Mensaje de Bienvenida ---
def display_home_page_content():
    st.title(f"👋 ¡Bienvenido al Dashboard Principal, {st.session_state.username}!")
    st.write("Esta es tu plataforma centralizada para explorar todos tus análisis de datos.")
    st.markdown("---")
    st.info("Para comenzar, por favor, selecciona un reporte de la **lista en el menú lateral de la izquierda**.")
    st.write("Puedes navegar entre diferentes grupos y reportes, y el contenido se cargará aquí mismo.")
    st.image("https://placehold.co/800x400/80C0D0/FFFFFF?text=Selecciona+un+Reporte",
             caption="Tu información está a solo un clic de distancia.")


# --- Renderizado del Contenido (Dashboard o Reporte Seleccionado) ---
st.markdown("---") # Separador visual para el contenido principal

# Si 'selected_report_file' es nuestro marcador, mostramos la página de inicio.
if st.session_state.selected_report_file == "home_page_marker":
    display_home_page_content()
# Si hay un nombre de archivo de reporte seleccionado en la sesión, intentamos cargarlo.
elif st.session_state.selected_report_file:
    report_content_dir = "report_content" # Ruta a la carpeta de contenido de reportes

    # Añadir la carpeta al path de importación de Python si no está
    if report_content_dir not in sys.path:
        sys.path.append(report_content_dir)

    try:
        module_name = st.session_state.selected_report_file.replace(".py", "")
        # Cargamos el módulo dinámicamente desde report_content
        spec = importlib.util.spec_from_file_location(module_name, os.path.join(report_content_dir, st.session_state.selected_report_file))
        if spec and spec.loader:
            report_module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = report_module # Añadir al sys.modules para que pueda ser importado
            spec.loader.exec_module(report_module)

            # Verificar si el módulo tiene la función 'render_content' y llamarla
            if hasattr(report_module, 'render_content') and callable(report_module.render_content):
                report_module.render_content()
            else:
                st.error(f"Error: El archivo {st.session_state.selected_report_file} no tiene la función 'render_content()'.")
        else:
            st.error(f"Error: No se pudo cargar la especificación para {st.session_state.selected_report_file}.")
            st.warning(f"Asegúrate de que el archivo '{st.session_state.selected_report_file}' existe en la carpeta '{report_content_dir}/'.")

    except FileNotFoundError:
        st.error(f"Error: El archivo de reporte '{st.session_state.selected_report_file}' no fue encontrado en '{report_content_dir}/'.")
        st.warning("Verifica que el nombre del archivo en 'reports_config.json' coincide con el nombre real en la carpeta 'report_content/'.")
    except Exception as e:
        st.error(f"Ocurrió un error al cargar o renderizar el reporte: {e}")
        st.warning("Asegúrate de que no haya errores de sintaxis en el archivo del reporte.")

else:
    # Esto se mostrará si st.session_state.selected_report_file es None o no es válido
    st.info("Por favor, selecciona un reporte para empezar.")
    display_home_page_content() # Muestra el mensaje de bienvenida como fallback

