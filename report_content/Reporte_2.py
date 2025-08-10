import streamlit as st
import pandas as pd

# Esta función dibuja el contenido del Reporte 1.
# No tiene lógica de sidebar ni st.set_page_config.
def render_content():
    st.title("📈 Reporte 2: Ventas por Región")
    st.write("Bienvenido al reporte de ventas por región.")
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

