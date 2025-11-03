# 🔧 MANUAL TÉCNICO - SISTEMA DE GESTIÓN DE BIBLIOTECAS

**Versión:** 1.0  
**Fecha:** Noviembre 2025  
**Desarrollador:** **Elmer Miguel**  
**Curso:** Estructuras de Datos - SS2025  

---

## 🎯 INTRODUCCIÓN

### **Objetivo del Sistema**

El Sistema de Gestión de Bibliotecas es una aplicación de escritorio desarrollada en Python que permite administrar una red interconectada de bibliotecas, gestionando catálogos de libros, transferencias entre sucursales, y optimización de rutas de distribución.

### **Alcance Técnico**

- **Dominio:** Gestión bibliográfica distribuida
- **Paradigma:** Programación orientada a objetos
- **Interfaz:** GUI con Tkinter y visualización matplotlib
- **Estructuras:** Implementación completa de TADs avanzados
- **Algoritmos:** Optimización de rutas, balanceo de árboles, simulación

### **Características Principales**

- ✅ **Red de bibliotecas interconectadas** con grafo ponderado
- ✅ **Catálogo distribuido** con múltiples índices de búsqueda
- ✅ **Sistema de transferencias** con colas de despacho FIFO
- ✅ **Rutas óptimas** mediante algoritmo de Dijkstra
- ✅ **Simulación en tiempo real** del flujo de libros
- ✅ **Sistema de rollback** para operaciones críticas
- ✅ **Visualización interactiva** con matplotlib y networkx

---

## 🏗️ ARQUITECTURA DEL SISTEMA

### **Patrón Arquitectónico**

El sistema sigue una **arquitectura en capas (Layered Architecture)** con separación clara de responsabilidades:

```
┌─────────────────────────────────────┐
│         CAPA DE PRESENTACIÓN        │
│     (GUI - Tkinter + Matplotlib)    │
├─────────────────────────────────────┤
│       CAPA DE CONTROLADORES         │
│        (Tab Controllers)            │
├─────────────────────────────────────┤
│      CAPA DE LÓGICA DE NEGOCIO      │
│   (RedBibliotecas, Biblioteca)      │
├─────────────────────────────────────┤
│    CAPA DE ESTRUCTURAS DE DATOS     │
│  (AVL, Hash, Grafo, Colas, etc.)    │
├─────────────────────────────────────┤
│         CAPA DE DATOS               │
│        (Archivos CSV)               │
└─────────────────────────────────────┘
```

### **Principios de Diseño**

1. **Separación de Responsabilidades:** Cada clase tiene una responsabilidad específica
2. **Bajo Acoplamiento:** Mínima dependencia entre módulos
3. **Alta Cohesión:** Elementos relacionados agrupados lógicamente
4. **Extensibilidad:** Fácil agregar nuevas funcionalidades
5. **Reutilización:** TADs genéricos reutilizables

---

## 💻 TECNOLOGÍAS Y DEPENDENCIAS

### **Lenguaje Principal**

- **Python 3.12+** - Lenguaje de programación principal

### **Librerías Core**

```python
# Interfaz Gráfica y Visualización
tkinter          # GUI nativa de Python
matplotlib==3.10.7    # Gráficos y visualización 
networkx==3.5         # Manipulación y análisis de grafos

# Procesamiento Numérico
numpy==2.9.4          # Operaciones numéricas eficientes

# Utilerías de Soporte
python-dateutil==2.9.0.post0  # Manejo avanzado de fechas
pillow==12.0.0               # Procesamiento de imágenes
```

### **Dependencias Específicas**

```python
# Matplotlib Dependencies
contourpy==1.3.3      # Cálculos de contorno
cycler==0.12.1        # Cycling de propiedades en plots
fonttools==4.60.1     # Manipulación de fuentes
kiwisolver==1.4.9     # Solver de constraints para layouts
packaging==25.0       # Utilidades de empaquetado
pyparsing==3.2.5      # Parser de expresiones
six==1.17.0          # Compatibilidad Python 2/3
```

### **Estructura de Archivos**

```
Proyecto2_eddSS2025/
├── main.py                    # Punto de entrada principal
├── requirements.txt           # Dependencias del proyecto
├── objetos/                   # Clases de dominio
│   ├── biblioteca.py
│   ├── libro.py
│   ├── red_bibliotecas.py
│   └── transferencia.py
├── estructuras/              # Implementación de TADs
│   ├── arbol_avl.py
│   ├── arbol_b.py
│   ├── tabla_hash.py
│   ├── grafo.py
│   ├── lista_secuencial.py
│   ├── pila.py
│   └── cola.py
├── gui/                      # Interfaz gráfica
│   ├── config.py
│   ├── red_tab.py
│   ├── catalogo_tab.py
│   ├── busqueda_tab.py
│   └── simulacion_tab.py
├── datos/                    # Archivos CSV
│   ├── bibliotecas.csv
│   ├── conexiones.csv
│   └── libros.csv
└── docs/                     # Documentación
    ├── manual_usuario.md
    ├── manual_tecnico.md
    └── diagramas/
```

---

## 🔧 ESTRUCTURAS DE DATOS IMPLEMENTADAS

### **Resumen de TADs Implementados**

| Estructura           | Archivo               | Uso Principal               | Complejidad Clave      |
| -------------------- | --------------------- | --------------------------- | ---------------------- |
| **Árbol AVL**        | `arbol_avl.py`        | Catálogo principal por ISBN | O(log n) búsqueda      |
| **Tabla Hash**       | `tabla_hash.py`       | Índices por título/autor    | O(1) promedio          |
| **Grafo**            | `grafo.py`            | Red de conexiones           | O((V+E)log V) Dijkstra |
| **Lista Secuencial** | `lista_secuencial.py` | Colecciones generales       | O(n) búsqueda          |
| **Pila LIFO**        | `pila.py`             | Sistema de rollback         | O(1) operaciones       |
| **Cola FIFO**        | `cola.py`             | Sistema de despacho         | O(1) operaciones       |
| **Árbol B/B+**       | `arbol_b.py`          | Índices secundarios         | O(log n) balanceado    |

### **Criterios de Selección**

Cada estructura fue seleccionada considerando:

- **Frecuencia de operaciones** en el dominio
- **Garantías de rendimiento** requeridas
- **Características de los datos** (claves, ordenamiento)
- **Patrones de acceso** (secuencial vs aleatorio)

----

## 🧩 MÓDULOS Y COMPONENTES

### **Módulo: objetos/**

#### **red_bibliotecas.py**

- **Clase:** `RedBibliotecas`

- **Responsabilidad:** Coordinador principal del sistema

- **Dependencias:** `Biblioteca`, `Grafo`, `Inventario`

- **Funcionalidades clave:**
  
  ```python
  def cargar_bibliotecas_csv(archivo)     # Carga inicial
  def cargar_conexiones_csv(archivo)      # Configuración red
  def cargar_libros_csv(archivo)          # Población catálogo
  def solicitar_transferencia(...)        # Lógica de negocio
  def obtener_estadisticas_red()          # Métricas sistema
  ```

#### **biblioteca.py**

- **Clase:** `Biblioteca`
- **Responsabilidad:** Entidad individual de biblioteca
- **Estructuras internas:**
  - `catalogo_local: ArbolAVL` - Catálogo principal
  - `indices_secundarios: TablaHash` - Búsquedas rápidas
  - `cola_ingreso, cola_traspaso, cola_salida: Cola` - Despacho
  - `historial_rollback: Pila` - Deshacer operaciones

#### **libro.py**

- **Clase:** `Libro`
- **Responsabilidad:** Entidad básica del dominio
- **Atributos:** ISBN, título, autor, género, año, estado
- **Métodos:** Cambio de estado, validaciones, serialización

### **Módulo: estructuras/**

Implementaciones puras de TADs siguiendo principios de:

- **Encapsulación:** Interfaz pública clara
- **Abstracción:** Ocultar detalles de implementación
- **Reutilización:** Genéricos, no acoplados al dominio
- **Eficiencia:** Optimizados para operaciones frecuentes

### **Módulo: gui/**

#### **Patrón MVC Implementado**

```python
# Modelo: objetos/red_bibliotecas.py
# Vista: gui/*_tab.py (componentes Tkinter)
# Controlador: gui/*_tab.py (clases controladoras)
```

#### **Pestañas Especializadas**

- **`red_tab.py`:** Gestión topología de red
- **`catalogo_tab.py`:** CRUD de libros y búsquedas
- **`busqueda_tab.py`:** Cálculo de rutas óptimas
- **`simulacion_tab.py`:** Simulación tiempo real con matplotlib

---

## ⚙️ ALGORITMOS PRINCIPALES

### **Algoritmo de Dijkstra (Rutas Óptimas)**

```python
def dijkstra(self, origen, destino, criterio):
    """
    Implementación optimizada con heap binario
    Complejidad: O((V + E) log V)
    Criterios: 'tiempo' o 'costo'
    """
    # Implementación con priority queue
    # Soporte para múltiples criterios de optimización
```

### **Balanceo AVL (Rotaciones)**

```python
def rotar_derecha(self, nodo):
    """Rotación simple derecha para balanceo AVL"""

def rotar_izquierda(self, nodo):
    """Rotación simple izquierda para balanceo AVL"""

def balancear(self, nodo):
    """Balanceo automático tras inserción/eliminación"""
```

### **Hash Function (Distribución Uniforme)**

```python
def hash_function(self, clave):
    """
    Función hash polinomial para strings
    Objetivo: Minimizar colisiones
    """
    # Implementación con multiplicación por primo
```

### **Simulación de Colas (Procesamiento FIFO)**

```python
def procesar_tick_simulacion(self):
    """
    Simula un ciclo de procesamiento
    Mueve libros entre estados según probabilidades
    """
    # Lógica de transición de estados
    # Procesamiento probabilístico realista
```

---

## 🔌 API Y INTERFACES

### **Interfaz Principal: RedBibliotecas**

```python
class RedBibliotecas:
    # Operaciones de configuración
    def cargar_bibliotecas_csv(self, archivo_csv) -> bool
    def cargar_conexiones_csv(self, archivo_csv) -> bool  
    def cargar_libros_csv(self, archivo_csv) -> bool

    # Operaciones de red
    def agregar_biblioteca(self, biblioteca) -> bool
    def eliminar_biblioteca(self, id_biblioteca) -> bool
    def crear_conexion(self, origen, destino, tiempo, costo) -> bool

    # Operaciones de transferencia
    def solicitar_transferencia(self, origen, destino, isbn, criterio) -> Transferencia
    def calcular_ruta_optima(self, origen, destino, criterio) -> List[str]

    # Consultas y reportes
    def buscar_libro_global(self, criterios) -> List[Libro]
    def obtener_estadisticas_red() -> Dict
    def generar_reporte_inventario() -> str
```

### **Interfaz Biblioteca Individual**

```python
class Biblioteca:
    # Gestión de catálogo
    def agregar_libro_catalogo(self, libro, registrar_rollback=True) -> bool
    def eliminar_libro_catalogo(self, isbn, registrar_rollback=True) -> bool
    def buscar_libro(self, isbn) -> Libro
    def buscar_libros_filtrados(self, criterios) -> List[Libro]

    # Sistema de colas
    def obtener_estado_colas(self) -> Dict
    def procesar_cola_ingreso(self) -> bool
    def procesar_cola_traspaso(self) -> bool
    def procesar_cola_salida(self) -> bool

    # Rollback
    def rollback_ultima_operacion(self) -> bool
    def obtener_historial_operaciones(self) -> List[str]
```

### **Contratos de TADs Genéricos**

```python
# Contrato para estructuras de búsqueda
class EstructuraBusqueda(ABC):
    @abstractmethod
    def insertar(self, clave, valor) -> None

    @abstractmethod  
    def buscar(self, clave) -> Any

    @abstractmethod
    def eliminar(self, clave) -> None

# Contrato para estructuras lineales
class EstructuraLineal(ABC):
    @abstractmethod
    def esta_vacia(self) -> bool

    @abstractmethod
    def tamaño(self) -> int
```

---

## 🛠️ CONFIGURACIÓN E INSTALACIÓN

### **Requisitos del Sistema**

- **Python:** 3.8 o superior
- **Memoria RAM:** 512MB mínimo (2GB recomendado)
- **Espacio en disco:** 100MB para instalación
- **Sistema operativo:** Windows 10+, Ubuntu 18+, macOS 10.14+

### **Instalación Paso a Paso**

#### **1. Clonar/Descargar Proyecto**

```bash
git clone [URL_PROYECTO]
cd Proyecto2_eddSS2025
```

#### **2. Crear Entorno Virtual (Recomendado)**

```bash
python -m venv venv_biblioteca
source venv_biblioteca/bin/activate  # Linux/Mac
# venv_biblioteca\Scripts\activate   # Windows
```

#### **3. Instalar Dependencias**

```bash
pip install -r requirements.txt
```

#### **4. Verificar Instalación**

```bash
python main.py
```

### **Configuración de Datos**

1. **Colocar archivos CSV** en la carpeta `datos/`
2. **Formatos requeridos:**
   - `bibliotecas.csv`: id,nombre,ubicacion
   - `conexiones.csv`: origen,destino,tiempo,costo  
   - `libros.csv`: isbn,titulo,autor,genero,año_publicacion,biblioteca_id

---

## 🧪 PRUEBAS Y VALIDACIÓN

### **Tipos de Pruebas Implementadas**

1. **Pruebas Unitarias:** Cada TAD individualmente
2. **Pruebas de Integración:** Interacción entre módulos
3. **Pruebas de Rendimiento:** Complejidad temporal verificada
4. **Pruebas de Interfaz:** Validación de GUI

### **Casos de Prueba Críticos**

```python
# Ejemplo: Prueba de balanceo AVL
def test_avl_balanceado():
    arbol = ArbolAVL()
    # Insertar secuencia que forzaría desbalance
    for i in range(1, 8):
        arbol.insertar(Libro(isbn=str(i)))

    assert arbol.obtener_altura() <= math.log2(7) + 1
    assert arbol.verificar_propiedad_avl()

# Ejemplo: Prueba de Dijkstra
def test_dijkstra_ruta_optima():
    grafo = Grafo()
    # Configurar red de prueba
    resultado = grafo.dijkstra("A", "D", "tiempo")
    assert resultado.distancia == 25  # Valor esperado
    assert resultado.ruta == ["A", "B", "D"]
```

### **Validación de Rendimiento**

- **Benchmark AVL:** 50,000 inserciones en < 100ms
- **Benchmark Hash:** 100,000 búsquedas en < 50ms  
- **Benchmark Dijkstra:** 100 nodos en < 10ms
- **Simulación:** 60 FPS en visualización tiempo real

---

## 🔧 MANTENIMIENTO Y EXTENSIBILIDAD

### **Puntos de Extensión**

1. **Nuevos TADs:** Implementar interfaz base en `estructuras/`
2. **Nuevos criterios Dijkstra:** Extender método `calcular_peso()`
3. **Nuevas visualizaciones:** Agregar tabs en `gui/`
4. **Nuevos formatos datos:** Modificar cargadores en `objetos/`

### **Patrones para Extensión**

```python
# Ejemplo: Agregar nuevo índice de búsqueda
class BusquedaPorGenero(EstructuraBusqueda):
    def __init__(self):
        self.indice = TablaHash()

    def insertar(self, libro):
        genero = libro.genero
        if genero not in self.indice:
            self.indice.insertar(genero, [])
        self.indice.buscar(genero).append(libro)
```

### **Logging y Monitoreo**

```python
import logging

# Configuración logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sistema_bibliotecas.log'),
        logging.StreamHandler()
    ]
)
```

---

## 🚨 TROUBLESHOOTING

### **Problemas Comunes**

#### **Error: "ImportError: No module named 'matplotlib'"**

```bash
# Solución:
pip install matplotlib==3.10.7
```

#### **Error: "CSV file not found"**

- Verificar que archivos CSV estén en carpeta `datos/`
- Verificar formato correcto de archivos
- Verificar permisos de lectura

#### **Rendimiento lento en búsquedas**

- Verificar que se esté usando índice correcto (AVL/Hash)
- Revisar factor de carga en tabla hash (debe ser < 0.75)
- Verificar balanceo en árbol AVL

#### **Interfaz no responde durante simulación**

- La simulación usa threading para no bloquear GUI
- Verificar que `simulacion_activa` se gestione correctamente
- Reducir frecuencia de actualización si es necesario

### **Logs de Debug**

```python
# Activar modo debug
import logging
logging.getLogger('sistema_bibliotecas').setLevel(logging.DEBUG)
```

---

## 📚 REFERENCIAS Y BIBLIOGRAFÍA

### **Documentación Oficial**

- [Python Official Documentation](https://docs.python.org/3/)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [Matplotlib Documentation](https://matplotlib.org/stable/)
- [NetworkX Documentation](https://networkx.org/)

---

## 👨‍💻 INFORMACIÓN DEL DESARROLLADOR

**Desarrollado por:** **Elmer Miguel**  
**Institución:** Universidad de San Carlos de Guatemala - CUNOC  
**Curso:** Estructuras de Datos - SS2025  
**Fecha:** Noviembre 2025  

---

*Este manual técnico proporciona una guía completa para el mantenimiento, extensión y comprensión técnica del Sistema de Gestión de Bibliotecas. Para información sobre uso del sistema, consultar el Manual de Usuario.*