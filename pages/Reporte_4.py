import streamlit as st
import pandas as pd
# Puedes importar otras librerías de visualización aquí (ej. matplotlib, plotly)

# --- Configuración de la Página Específica ---
# Este page_config se aplicará solo a esta página cuando sea visible.
# Cuando el usuario está en una página de reporte y está logueado, queremos el sidebar expandido.
st.set_page_config(
    page_title="Reporte 1: Ventas",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded" # <-- Asegura que el sidebar esté expandido en esta página
)

# --- Lógica Principal de la Página de Reporte ---
# Verifica si el usuario está logueado. Si no, muestra un mensaje y detiene la ejecución.
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("Por favor, inicia sesión para acceder a este reporte.")
    st.info("Dirígete a la página principal para iniciar sesión.")
    st.stop() # ¡Importante! Detiene la ejecución de esta página si no está logueado
                # y así evita que el contenido o el sidebar de esta página se muestren.
else:
    # Si el usuario está logueado, muestra el contenido del reporte
    st.title("📈 Reporte 1: Ventas por Región")
    st.write(f"Hola {st.session_state.username}, bienvenido al reporte de ventas por región.")
    st.markdown("---")

    st.subheader("Datos de Ventas")
    # Ejemplo de datos (reemplaza con datos reales de tu BD o análisis)
    data = {
        "Región": ["Norte", "Centro", "Sur", "Este", "Oeste"],
        "Ventas": [150000, 230000, 180000, 200000, 190000],
        "Margen": [0.15, 0.20, 0.18, 0.17, 0.19]
    }
    df = pd.DataFrame(data)
    st.dataframe(df)

    st.subheader("Gráfico de Ventas por Región")
    # Ejemplo de gráfico simple
    st.bar_chart(df.set_index("Región")["Ventas"])

    st.markdown("---")
    st.info("Este reporte muestra un análisis del rendimiento de ventas por cada región geográfica. Puedes interactuar con los datos o añadir más visualizaciones.")

    # Botón de Cerrar Sesión en el Sidebar (buena práctica para Multi-Page Apps)
    # Solo se muestra si el usuario está logueado en las páginas de reportes.
    with st.sidebar:
        st.write(f"Conectado como: **{st.session_state.username}**")
        if st.button("Cerrar Sesión", key="logout_sidebar"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.is_admin = False
            st.success("Sesión cerrada. Volviendo a la página de acceso.")
            st.rerun() # Fuerza la recarga para volver a la página de login
