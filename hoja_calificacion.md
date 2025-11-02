| Categorias                                             |                                                                                   | Puntos | Obtenido |
| ------------------------------------------------------ |:--------------------------------------------------------------------------------- | ------ | -------- |
| **Manuales y Documentación (10%)**                     |                                                                                   |        |          |
|                                                        | Documentación de TAD’s implementados                                              | **2**  |          |
|                                                        | Diagramas estructurales                                                           | **2**  |          |
|                                                        | Manual Técnico del Sistema                                                        | **3**  |          |
|                                                        | Manual de Usuario                                                                 | **2**  |          |
|                                                        | Archivo README                                                                    | **1**  |          |
| **SUBTOTAL**                                           |                                                                                   | **10** |          |
| **Implementación de estructuras (25%)**                |                                                                                   |        |          |
|                                                        | Árbol AVL (búsqueda e inserción por título o ISBN)                                | **2**  |          |
|                                                        | Árbol B y Árbol B+ (por género o año)                                             | **3**  |          |
|                                                        | Tabla Hash (por ISBN con manejo de colisiones)                                    | **5**  |          |
|                                                        | Listas enlazadas/doblemente enlazadas (colecciones por biblioteca)                | **1**  |          |
|                                                        | Pilas (control de devoluciones o “rollback”)                                      | **2**  |          |
|                                                        | Colas (ingreso, traspaso y salida por biblioteca)                                 | **2**  |          |
|                                                        | Grafo ponderado (red de bibliotecas con tiempo/costo)                             | **5**  |          |
| **SUBTOTAL**                                           |                                                                                   | **20** |          |
| **Inserción, eliminación y sincronización (10%)**      |                                                                                   |        |          |
|                                                        | Inserción correcta en todas las estructuras (AVL, B, B+, Hash, Listas)            | **3**  |          |
|                                                        | Eliminación coherente en todas las estructuras                                    | **3**  |          |
|                                                        | Actualización sincronizada entre estructuras (coherencia global)                  | **2**  |          |
|                                                        | Mantenimiento de estados del libro (“Disponible”, “En tránsito”, “Agotado”)       | **2**  |          |
| **SUBTOTAL**                                           |                                                                                   | **10** |          |
| **Búsquedas y rendimiento (10%)**                      |                                                                                   |        |          |
|                                                        | Búsqueda por título (AVL o secuencial)                                            | **1**  |          |
|                                                        | Búsqueda por ISBN (Hash)                                                          | **2**  |          |
|                                                        | Búsqueda por género o rango de fechas (B o B+)                                    | **1**  |          |
|                                                        | Comparación de tiempos: secuencial vs binaria vs hash                             | **2**  |          |
|                                                        | Resultados consistentes y sin duplicados                                          | **2**  |          |
| **SUBTOTAL**                                           |                                                                                   | **8**  |          |
| **Gestión de red y rutas entre bibliotecas (10%)**     |                                                                                   |        |          |
|                                                        | Creación correcta de grafo ponderado (nodos, aristas, pesos)                      | **3**  |          |
|                                                        | Implementación de rutas por tiempo mínimo.                                        | **3**  |          |
|                                                        | Implementación de rutas por costo mínimo                                          | **3**  |          |
|                                                        | Transferencia de libros entre bibliotecas (integración con colas)                 | **3**  |          |
| **SUBTOTAL**                                           |                                                                                   | **12** |          |
| **Sistema de despacho y simulación (5%)**              |                                                                                   |        |          |
|                                                        | Cola de ingreso implementada por biblioteca                                       | **2**  |          |
|                                                        | Cola de preparación de traspaso implementada                                      | **2**  |          |
|                                                        | Cola de salida implementada (FIFO, intervalo de despacho)                         | **2**  |          |
|                                                        | Control de tiempos de despacho (ingreso, traspaso, envío)                         | **2**  |          |
|                                                        | Simulación de flujo entre bibliotecas.                                            | **2**  |          |
| **SUBTOTAL**                                           |                                                                                   | **10** |          |
| **Métodos de ordenamiento y análisis (10%)**           |                                                                                   |        |          |
|                                                        | Implementación de 5 métodos (intercambio, selección, inserción, Shell, QuickSort) | **5**  |          |
|                                                        | Aplicación de los métodos al catálogo (por título, autor, ISBN o año)             | **2**  |          |
|                                                        | Comparación de tiempos y eficiencia de ordenamientos                              | **3**  |          |
| **SUBTOTAL**                                           |                                                                                   | **10** |          |
| **Carga y validación de archivos CSV (5%)**            |                                                                                   |        |          |
|                                                        | Carga correcta de catálogos, bibliotecas y conexiones                             | **2**  |          |
|                                                        | Manejo de errores: líneas mal formateadas, duplicados o vacíos                    | **2**  |          |
|                                                        | Validación de ISBN (ediciones repetidas o conflicto entre colecciones)            | **1**  |          |
| **SUBTOTAL**                                           |                                                                                   | **5**  |          |
| **Visualización y reportes (5%)**                      |                                                                                   |        |          |
|                                                        | Exportación gráfica de árboles (AVL, B, B+)                                       | **2**  |          |
|                                                        | Visualización de Tabla Hash (colisiones y factor de carga)                        | **1**  |          |
|                                                        | Visualización del Grafo (nodos, conexiones, pesos, rutas)                         | **1**  |          |
|                                                        | Visualización de colas y pilas activas por biblioteca                             | **1**  |          |
| **SUBTOTAL**                                           |                                                                                   | **5**  |          |
| **Interfaz gráfica e interacción del usuario (5%)**    |                                                                                   |        |          |
|                                                        | Interfaz funcional: gestión de libros, colecciones y bibliotecas                  | **2**  |          |
|                                                        | Visualización dinámica del grafo y estructuras                                    | **2**  |          |
|                                                        | Experiencia de usuario fluida, diseño intuitivo y limpio                          | **1**  |          |
| **SUBTOTAL**                                           |                                                                                   | **5**  |          |
| **Análisis Big-O y justificación de estructuras (5%)** |                                                                                   |        |          |
|                                                        | Análisis de complejidad                                                           | **3**  |          |
|                                                        | Justificación del uso de cada estructura en su contexto                           | **2**  |          |
| **SUBTOTAL**                                           |                                                                                   | **5**  |          |
|                                                        |                                                                                   |        |          |
| **TOTAL**                                              |                                                                                   | 100    |          |
