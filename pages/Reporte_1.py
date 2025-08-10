import streamlit as st
import pandas as pd
# Puedes importar otras librerías de visualización aquí (ej. matplotlib, plotly)

# --- Configuración de la Página Específica ---
st.set_page_config(
    page_title="Reporte 1: Ventas",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded" # Asegura que el sidebar esté expandido en esta página
)

# --- Lógica Principal de la Página de Reporte ---
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("Por favor, inicia sesión para acceder a este reporte.")
    st.info("Dirígete a la página principal para iniciar sesión.")
    st.stop()
else:
    st.title("📈 Reporte 1: Ventas por Región")
    st.write(f"Hola {st.session_state.username}, bienvenido al reporte de ventas por región.")
    st.markdown("---")

    st.subheader("Datos de Ventas")
    data = {
        "Región": ["Norte", "Centro", "Sur", "Este", "Oeste"],
        "Ventas": [150000, 230000, 180000, 200000, 190000],
        "Margen": [0.15, 0.20, 0.18, 0.17, 0.19]
    }
    df = pd.DataFrame(data)
    st.dataframe(df)

    st.subheader("Gráfico de Ventas por Región")
    st.bar_chart(df.set_index("Región")["Ventas"])

    st.markdown("---")
    st.info("Este reporte muestra un análisis del rendimiento de ventas por cada región geográfica. Puedes interactuar con los datos o añadir más visualizaciones.")

    # --- Contenido del Sidebar ---
    with st.sidebar:
        # 1. Botón de Cerrar Sesión (PRIMERO en el código, debería aparecer arriba)
        if st.button("Cerrar Sesión", key="logout_sidebar"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.is_admin = False
            st.success("Sesión cerrada. Volviendo a la página de acceso.")
            st.switch_page("mi_app.py")
        
        # 2. Mensaje de usuario conectado (SEGUNDO en el código)
        st.write(f"Conectado como: **{st.session_state.username}**")

        # 3. Menú de navegación de páginas (Streamlit lo agrega AUTOMÁTICAMENTE AQUÍ DEBAJO)
        #    Esto incluye "Reporte 1", "Reporte 2", etc.
