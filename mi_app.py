import streamlit as st
import pandas as pd
import importlib.util # Para importar módulos dinámicamente
import sys # Para añadir directorios al path de importación
import os # Para construir rutas de archivo

from utils.report_config_loader import init_reports_data, get_all_reports_config
from utils.sidebar_menu_builder import build_collapsible_sidebar_menu

# --- Inicialización del Archivo JSON de Reportes ---
init_reports_data()

# --- Configuración Inicial del Estado de Sesión ---
# Define el archivo del reporte seleccionado para mostrar su contenido.
if 'selected_report_file' not in st.session_state:
    st.session_state.selected_report_file = "welcome_page"


# --- Configuración de la Página Global ---
# Ahora mi_app.py es la única página, así que su configuración es la general.
st.set_page_config(
    page_title="App de Reportes - Perrini",
    page_icon="📊",
    layout="wide", # Usamos wide para el contenido principal
    initial_sidebar_state="collapsed" # <-- ¡CAMBIO CLAVE! Inicia COLAPSADO por defecto
)

# --- CSS para OCULTAR elementos por defecto de Streamlit (MÁS LIGERO Y SEGURO) ---
# Hemos eliminado TODAS las reglas CSS que intentaban manipular el sidebar o el MainMenu
# para dejar que Streamlit los maneje de forma nativa y fiable.
hide_elements_css = """
    <style>
        footer {visibility: hidden;} /* Oculta el footer "Made with Streamlit" */
        header {visibility: hidden;} /* Oculta el encabezado de Streamlit */

        /* No hay reglas CSS aquí para #MainMenu o [data-testid="stSidebar"]
           Dejamos que Streamlit los controle completamente de forma nativa. */
    </style>
"""
st.markdown(hide_elements_css, unsafe_allow_html=True)


# --- Lógica de la Barra Lateral (Sidebar) ---
# La función build_collapsible_sidebar_menu() se encargará de dibujar todo el menú
# y de actualizar st.session_state.selected_report_file al hacer clic.
build_collapsible_sidebar_menu()


# --- Función para Mostrar el Mensaje de Bienvenida ---
def display_welcome_message():
    st.title("👋 ¡Bienvenido a tu App de Reportes, Perrini!")
    st.write("Esta es tu plataforma centralizada para explorar todos tus análisis de datos.")
    st.markdown("---")
    st.info("Para comenzar, por favor, selecciona un reporte de la **lista en el menú lateral de la izquierda**.")
    st.write("Puedes navegar entre diferentes grupos y reportes, y el contenido se cargará aquí mismo.")
    st.image("https://placehold.co/800x400/80C0D0/FFFFFF?text=Selecciona+un+Reporte",
             caption="Tu información está a solo un clic de distancia.")


# --- Renderizado del Contenido del Reporte Seleccionado ---
st.markdown("---")

if st.session_state.selected_report_file == "welcome_page":
    display_welcome_message()
elif st.session_state.selected_report_file:
    # Ruta a la carpeta de contenido de reportes (¡Importante!)
    report_content_dir = "report_content" 

    # Añadir la carpeta al path de importación de Python si no está
    if report_content_dir not in sys.path:
        sys.path.append(report_content_dir)

    try:
        module_name = st.session_state.selected_report_file.replace(".py", "")
        spec = importlib.util.spec_from_file_location(module_name, os.path.join(report_content_dir, st.session_state.selected_report_file))
        if spec and spec.loader:
            report_module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = report_module
            spec.loader.exec_module(report_module)

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
    st.info("Por favor, selecciona un reporte para empezar.")
    st.image("https://placehold.co/800x400/cccccc/000000?text=Bienvenido", caption="Tu aplicación está lista.")