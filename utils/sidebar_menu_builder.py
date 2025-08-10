import streamlit as st
from utils.report_config_loader import get_all_reports_config # Importar funciones de JSON

def build_collapsible_sidebar_menu():
    """
    Construye el menú colapsable de reportes en el sidebar,
    leyendo la configuración desde reports_config.json.
    Cuando se hace clic en un reporte, actualiza st.session_state.selected_report_file.
    """
    with st.sidebar:
        st.header("Menú de Reportes")
        st.markdown("---")

        config = get_all_reports_config() # Obtener la configuración desde el JSON

        if config and config.get("groups"):
            # Ordenar grupos por 'display_order'
            sorted_groups = sorted(config["groups"], key=lambda g: g.get("display_order", 999))
            
            # Iterar sobre los grupos y crear expanders (secciones colapsables)
            for group in sorted_groups:
                group_name = group.get("name", "Sin Grupo")
                group_reports = group.get("reports", [])

                # --- ¡CAMBIO CLAVE AQUÍ! expanded=False para que inicie colapsado ---
                with st.expander(f"📁 {group_name}", expanded=False): 
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

        st.markdown("---") # Separador al final del menú

        # Botón "Salir" (simulado, ya que no hay autenticación real)
        if st.button("Salir (Simulado)", key="exit_simulated"):
            st.info("Saliendo de la aplicación (simulado).")
            st.session_state.selected_report_file = None # Vuelve al estado inicial de "Selecciona un reporte"
            st.rerun() # Para forzar la actualización de la página.

