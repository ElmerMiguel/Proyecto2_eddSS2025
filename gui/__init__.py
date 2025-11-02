"""
Paquete de GUI - Exporta módulos principales
"""

from .config import *
from .styles import configurar_estilos
from .dashboard_tab import crear_dashboard
from .catalogo_tab import crear_catalogo_tab
from .red_tab import crear_red_tab
from .busqueda_tab import crear_busqueda_rutas_tab
from .simulacion_tab import crear_simulacion_tab
from .visualizacion_tab import crear_visualizacion_tab
from .pruebas_tab import crear_pruebas_carga_tab

__all__ = [
    'configurar_estilos',
    'crear_dashboard',
    'crear_catalogo_tab',
    'crear_red_tab',
    'crear_busqueda_rutas_tab',
    'crear_simulacion_tab',
    'crear_visualizacion_tab',
    'crear_pruebas_carga_tab'
]