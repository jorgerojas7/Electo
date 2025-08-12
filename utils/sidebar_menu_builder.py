import streamlit as st
from utils.report_config_loader import get_all_reports_config # Importar funciones de JSON

def build_collapsible_sidebar_menu():
    """
    Construye el menú colapsable de reportes en el sidebar,
    leyendo la configuración desde reports_config.json.
    Cuando se hace clic en un reporte, actualiza st.session_state.selected_report_file.
    """
    with st.sidebar:
        # --- Botón "Cerrar Sesión" ahora es el PRIMER elemento y funcional ---
        st.markdown('<div id="logout-button-container">', unsafe_allow_html=True) 
        if st.button("Cerrar Sesión 🚪", key="logout_button_final"): # Texto y emoji de puerta
            st.session_state.logged_in = False # Restablecemos el estado a no logueado
            st.session_state.username = ""     # Limpiamos el nombre de usuario
            st.session_state.is_admin = False  # Limpiamos el estado de admin
            st.session_state.selected_report_file = "home_page_marker" # Vuelve al marcador de la página de bienvenida
            st.success("Sesión cerrada. Volviendo a la página de acceso.")
            st.switch_page("mi_app.py") # Redirige a la página principal de login (mi_app.py)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---") # Separador visual

        # st.header("Menú de Reportes") # Hemos eliminado este encabezado para mayor limpieza
        # st.markdown("---") # Hemos eliminado este separador para mayor limpieza

        config = get_all_reports_config() # Obtener la configuración desde el JSON

        if config and config.get("groups"):
            # Ordenar grupos por 'display_order'
            sorted_groups = sorted(config["groups"], key=lambda g: g.get("display_order", 999))
            
            # Iterar sobre los grupos y crear expanders (secciones colapsables)
            for group in sorted_groups:
                group_name = group.get("name", "Sin Grupo")
                group_reports = group.get("reports", [])

                with st.expander(f"📁 {group_name}", expanded=False): # Los expanders inician COLAPSADOS por defecto
                    # Ordenar reportes dentro del grupo por 'display_order'
                    sorted_group_reports = sorted(group_reports, key=lambda r: r.get("display_order", 999))
                    
                    for report in sorted_group_reports:
                        report_name = report.get("name", "Reporte Desconocido")
                        report_filename = report.get("filename")

                        if report_filename: # Asegurarse de que haya un filename válido
                            # Al hacer clic en el botón, actualizamos el estado de la sesión
                            # con el nombre del archivo del reporte.
                            if st.button(report_name, key=f"btn_{report_filename}"):
                                st.session_state.selected_report_file = report_filename
                                # Streamlit hará un rerun automático al cambiar el estado.
        else:
            st.warning("No se encontraron grupos de reportes en la configuración.")

        # st.markdown("---") # Hemos quitado este separador al final para mayor limpieza
