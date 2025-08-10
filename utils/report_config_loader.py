import json
import os

# --- Configuración del Archivo JSON de Reportes ---
JSON_FILE_REPORTS = 'reports_config.json' # Nombre del archivo JSON para la configuración de reportes

def _default_report_config():
    """Define la estructura por defecto de los reportes en JSON."""
    return {
        "groups": [
            {
                "name": "Grupo 1: Operaciones",
                "display_order": 1,
                "reports": [
                    {"name": "Reporte 1: Ventas por Región", "filename": "Reporte_1.py", "display_order": 1},
                    {"name": "Reporte 2: Desempeño de Productos", "filename": "Reporte_2.py", "display_order": 2},
                    {"name": "Reporte 3: Análisis de Clientes", "filename": "Reporte_3.py", "display_order": 3}
                ]
            },
            {
                "name": "Grupo 2: Estratégicos",
                "display_order": 2,
                "reports": [
                    {"name": "Reporte 4: Proyecciones Futuras", "filename": "Reporte_4.py", "display_order": 1},
                    {"name": "Reporte 5: Resumen Ejecutivo", "filename": "Reporte_5.py", "display_order": 2}
                ]
            }
        ]
    }

def init_reports_data():
    """
    Inicializa el archivo JSON de reportes con la configuración por defecto
    si no existe.
    """
    if not os.path.exists(JSON_FILE_REPORTS):
        with open(JSON_FILE_REPORTS, 'w', encoding='utf-8') as f:
            json.dump(_default_report_config(), f, indent=4, ensure_ascii=False)

def get_all_reports_config():
    """
    Obtiene toda la configuración de reportes desde el archivo JSON.
    """
    if not os.path.exists(JSON_FILE_REPORTS):
        init_reports_data() # Asegurarse de que el archivo exista
        
    with open(JSON_FILE_REPORTS, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

