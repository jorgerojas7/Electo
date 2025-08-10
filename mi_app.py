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
    config = get_all_reports_config()
    # Establece el primer reporte del JSON como predeterminado al inicio
    first_report_filename = None
    if config and config.get("groups"):
        if config["groups"][0].get("reports"):
            first_report_filename = config["groups"][0]["reports"][0].get("filename")
    
    st.session_state.selected_report_file = first_report_filename or "Reporte_1.py" # Fallback


# --- Configuración de la Página Global ---
# Ahora mi_app.py es la única página, así que su configuración es la general.
st.set_page_config(
    page_title="App de Reportes - Perrini",
    page_icon="📊",
    layout="wide", # Usamos wide para el contenido principal
    initial_sidebar_state="expanded" # Queremos el sidebar expandido por defecto
)

# --- CSS para OCULTAR elementos por defecto de Streamlit ---
# NOTA: Se ha quitado la ocultación de #MainMenu para permitir que la hamburguesa aparezca al colapsar.
hide_elements_css = """
    <style>
        /* #MainMenu {visibility: hidden;} */ /* ¡Esta línea ha sido eliminada o comentada! */
        footer {visibility: hidden;} /* Oculta el footer "Made with Streamlit" */
        header {visibility: hidden;} /* Oculta el encabezado de Streamlit */
    </style>
"""
st.markdown(hide_elements_css, unsafe_allow_html=True)


# --- Lógica de la Barra Lateral (Sidebar) ---
# La función build_collapsible_sidebar_menu() se encargará de dibujar todo el menú
# y de actualizar st.session_state.selected_report_file al hacer clic.
build_collapsible_sidebar_menu()


# --- Renderizado del Contenido del Reporte Seleccionado ---
st.markdown("---") # Separador visual

if st.session_state.selected_report_file:
    # Ruta a la carpeta de contenido de reportes (¡Importante!)
    report_content_dir = "report_content" 

    # Añadir la carpeta al path de importación de Python si no está
    if report_content_dir not in sys.path:
        sys.path.append(report_content_dir)

    try:
        # Extraer el nombre del módulo (sin .py)
        module_name = st.session_state.selected_report_file.replace(".py", "")
        
        # Cargar el módulo dinámicamente
        # Usamos importlib.util para un control más fino y para evitar problemas con la caché.
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
    # Esto se mostrará si st.session_state.selected_report_file es None (por ejemplo, después de "Salir")
    st.info("Selecciona un reporte del menú lateral.")
    st.image("https://placehold.co/800x400/cccccc/000000?text=Bienvenido", caption="Tu aplicación está lista.")

