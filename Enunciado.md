# 📚 BIBLIOTECA MÁGICA ALREDEDOR DEL MUNDO

## 🎯 Objetivo General

Desarrollar una aplicación con interfaz gráfica que gestione una **red de bibliotecas interconectadas**, cada una con su propio catálogo de libros y características de procesamiento. El sistema deberá aplicar estructuras de datos avanzadas (**listas, árboles, búsquedas, tablas hash, colas y grafos**) implementadas **desde cero**, para optimizar la búsqueda, transferencia y gestión de libros entre bibliotecas, considerando tiempos y costos de traslado.

---

## ✨ Objetivos Específicos

* **Implementar y combinar estructuras de datos complejas** (Árbol AVL, Árbol B, Árbol B+, Tabla Hash, Colas y Grafos) **desde cero**.
* Permitir operaciones **eficientes** de búsqueda, inserción, eliminación y traslado de libros.
* Gestionar una **red de bibliotecas con conexiones ponderadas**.
* Calcular **rutas óptimas** de transferencia entre bibliotecas utilizando algoritmos de recorrido de grafos.
* Analizar y comparar el rendimiento entre diferentes estructuras y métodos de búsqueda.
* Evaluar tiempos de procesamiento y despacho bajo diferentes configuraciones.
* **Visualizar de forma gráfica** los árboles, la red de bibliotecas y las colas de despacho.

---

## 📜 Descripción del Sistema

La Biblioteca Mágica ha crecido más allá de sus fronteras, ahora forma parte de una **red nacional de bibliotecas encantadas**, donde cada una posee su propio catálogo, su propio ritmo para procesar y enviar libros, y **conexiones mágicas** que comunican sus estanterías a través del mundo.

Cada biblioteca puede enviar libros a otra, utilizando **portales temporales** (conexiones entre nodos del grafo), y el sistema debe determinar la mejor ruta según el **menor tiempo total** o el **menor costo de envío (Costo Mágico)**.

Durante los traslados, cada biblioteca actúa como centro de despacho con su propia **cola de envíos**: los libros se procesan con intervalos de tiempo definidos por el usuario, simulando la capacidad y velocidad de cada sede.

El sistema deberá registrar, buscar y administrar libros utilizando estructuras de datos avanzadas, garantizando **coherencia entre todas ellas** y ofreciendo una interfaz intuitiva que permita monitorear la red, las rutas, las colas de envío y el desempeño general del sistema.

---

## 🛠️ Estructuras y Funcionalidades Principales

| Operación                            | Estructura Utilizada             | Detalle                                                                                         |
|:------------------------------------ |:-------------------------------- |:----------------------------------------------------------------------------------------------- |
| **Agregar libro**                    | Todas las estructuras            | Inserta en **AVL** (por título), **Árbol B/B+** (por género o año) y **Hash Table** (por ISBN). |
| **Buscar por título**                | Árbol **AVL** + búsqueda binaria | Ordena por título y permite búsqueda rápida en nodos hoja.                                      |
| **Buscar por ISBN**                  | **Tabla Hash**                   | Clave única; manejo de colisiones mediante encadenamiento o sondeo.                             |
| **Buscar por género**                | **Árbol B+**                     | Clave secundaria: género. Permite recorrer libros por genero.                                   |
| **Buscar por rango de fechas**       | **Árbol B**                      | Filtrado eficiente por año de publicación.                                                      |
| **Eliminar libro**                   | Todas las estructuras            | Elimina de todas las estructuras (Que se visualice en que estructuras).                         |
| **Listar libros por título**         | Recorrido **in-order (AVL)**     | Muestra libros ordenados alfabéticamente.                                                       |
| **Comparar búsquedas**               | -                                | Mide el tiempo de **búsqueda secuencial vs. binaria y hash**.                                   |
| **Exportar libro entre bibliotecas** | **Grafo ponderado + Colas**      | Determina la ruta óptima y simula despacho según tiempos configurados.                          |

---

## 🏛️ Gestión de Bibliotecas (Nodos)

* Cada biblioteca tendrá un nombre, ubicación, y **parámetros configurables**:
  * **Tiempo de procesamiento** de ingreso de libros.
  * **Tiempo de traspaso o despacho** a otra biblioteca.
* La biblioteca puede enviar o recibir libros desde otras, siguiendo las rutas definidas en el grafo.
* Utilizar **árboles binarios o AVL** para organizar libros según ISBN o título
* Implementar al menos **cinco métodos de ordenamiento** (intercambio, selección directa, inserción directa, Shell y QuickSort) aplicados al catálogo de libros por título, autor, ISBN o año.

### 📝 Registro y Control de Libros

* Cada libro tendrá los siguientes atributos:
  * **Título, Autor, ISBN, Año de publicación, Género.**
  * **Estado** (disponible, prestado, **en tránsito**, agotado.)
* **Validación de ISBN:**
  * Si el ISBN ya existe en la misma colección, puede registrarse (Ediciones repetidas).
  * Si el ISBN pertenece a otra colección o libro diferente, se debe generar un error e impedir el registro.
* El almacenamiento principal de los libros se realizará mediante **listas enlazadas o listas doblemente enlazadas**, organizadas por colección.
* Se emplearán **arreglos multidimensionales** para representar el inventario total de libros de cada biblioteca, organizado por género.

---

## ➡️ Ingreso y Flujo de libros

Al ingresar un libro, se puede especificar que su destino final será otra biblioteca, es decir la biblioteca de entrada y destino, y si se dará prioridad a **tiempo de ruta o costo**.

* El sistema deberá:
  * Colocar el libro en la **cola de ingreso** de la biblioteca de origen.
  * Calcular su **ruta** hacia la biblioteca destino usando el criterio elegido por el usuario (tiempo o costo).
  * Si la ruta pasa por bibliotecas intermedias, gestionar las **colas de preparación de traspaso y de salida**.
  * Mantener el **estado del libro actualizado**: “En tránsito”, “Disponible”, “Agotado” u otro que considere necesario.

### 🔄 Procesamiento y Organización de Libros

* Los libros podrán visualizarse en diferentes modos:
  * Ordenados alfabéticamente, por año, género o autor.
* El sistema deberá permitir **ordenar el catálogo completo** o solo una colección específica, con distintas estrategias de organización seleccionables por el usuario.
* Los usuarios podrán **comparar la velocidad** de diferentes métodos de ordenamiento mediante métricas visibles o tiempos registrados.
* Utilizar **pilas** para el control de libros devueltos o para operaciones de **“deshacer” (rollback)** de registros erróneos.

### 🔍 Búsqueda Avanzada

* El usuario podrá realizar búsquedas por distintos criterios:
  * Título del libro.
  * Autor.
  * ISBN mágico.
  * Año o rango de fechas.
  * Colección.
* Se debe garantizar que las búsquedas sean **rápidas y eficientes**, incluso con catálogos grandes.
* En caso de que un libro no exista, el sistema deberá ofrecer opciones alternativas o mostrar coincidencias parciales.
* **Incluir**:
  * **Búsqueda secuencial** (lista enlazada).
  * **Búsqueda binaria** (en árbol AVL o arreglo ordenado).
  * **Búsqueda hash** (en tabla de dispersión).
* Además, se deberá registrar los **tiempos de transferencia** entre bibliotecas para distintos escenarios (por tiempo o costo).

---

## 🕸️ Red de Bibliotecas (Grafo)

Cada biblioteca será un **nodo** del grafo, y las conexiones entre ellas serán **aristas ponderadas** que representan el tiempo o costo de traslado.

### Propiedades Configurables del Nodo (Biblioteca)

* **Nombre de la biblioteca.**
* **Tiempo de ingreso:** tiempo en segundos que tarda en procesar la llegada de un libro.
* **Tiempo de traspaso:** tiempo en segundos necesario para preparar un libro antes de enviarlo.
* **Intervalo de despacho:** tiempo en segundos entre cada envío que la biblioteca puede realizar.
* **Cola de despacho:** lista de libros en espera de ser enviados a su siguiente destino.

### Propiedades de la Arista (Conexión)

* Biblioteca origen y destino.
* **Peso de conexión** (en tiempo o costo).
* Opción de conexión bidireccional o unidireccional.

---

## 📦 Sistema de Despacho y Colas

Cuando un libro debe trasladarse de una biblioteca a otra, el sistema determinará la **ruta más eficiente** según el criterio elegido (tiempo o costo). Cada biblioteca involucrada podrá gestionar los libros mediante **tres colas**:

1. **Cola de Ingreso:**
   * Aquí llegan los libros recién recibidos.
   * Si la biblioteca es el destino final, el libro permanece aquí después de ser procesado.
2. **Cola de Preparación de Traspaso:**
   * Aplica solo si la biblioteca es **intermedia**.
   * Los libros que deben continuar hacia otra biblioteca se colocan aquí mientras se preparan para el envío.
3. **Cola de Salida:**
   * Contiene todos los libros **listos para ser enviados** desde la biblioteca.
   * Incluye los que vienen de la cola de traspaso o los que se envían directamente desde esta biblioteca.
   * Se respeta un **intervalo de despacho** entre cada envío, simulando la capacidad y velocidad de salida.

### Cálculo de Envíos

Cada envío se calcula considerando:

* **Tiempo de ingreso:** Periodo que tarda una biblioteca en recibir y procesar un libro cuando llega.
* **Tiempo de preparación de traspaso:** Aplica cuando la biblioteca actúa únicamente como punto de paso.
* **Intervalo de despacho:** Tiempo entre cada libro que puede ser enviado.
* **Peso o costo de la conexión** entre bibliotecas (tiempo o costo).

El sistema podrá **simular o visualizar el flujo de envíos** y mostrar la **estimación de llegada (ETA)** de cada libro a su destino.

### 📤 Transferencia y Exportación de Libros

* El sistema debe determinar la **ruta más corta o más económica** para transferir un libro.
* El usuario podrá elegir el criterio de transferencia: **Tiempo mínimo de envío** o **Costo energético más bajo**.
* Las rutas deberán **visualizarse gráficamente**, mostrando los nodos intermedios y los tiempos estimados.

---

## 📊 Visualización

El sistema debe permitir generar **representaciones gráficas** de:

* **Árboles** (AVL, B, B+) con sus claves ordenadas.
* **Tabla Hash** (con colisiones y factor de carga).
* **Red de Bibliotecas** (nodos y conexiones).
* **Estado actual de colas de despacho** (por biblioteca).

### 🖥️ Interfaz Gráfica (GUI)

Desarrollar una interfaz visual intuitiva que permita:

* Crear, modificar o eliminar bibliotecas.
* Agregar y gestionar colecciones y libros.
* Control de libros devueltos (**Pilas**) o para operaciones de **“deshacer” (rollback)**.
* Visualizar el grafo de bibliotecas y las rutas disponibles.
* Observar en **tiempo real** el movimiento de libros entre bibliotecas en colas de envío y recepción.
* Mostrar los árboles, pilas y listas mediante **diagramas dinámicos** o representaciones gráficas.

---

## 📂 Carga de Archivos CSV

El sistema deberá permitir la carga de datos desde archivos externos para:

1. **Catálogo de Libros** 
   
   Formato:
   
   ```csv
   "Titulo","ISBN","Genero","Año","Autor","Estado","ID BibliotecaOrigen","ID BibliotecaDestino","Prioridad"
   "Cien años de soledad","978-8747417926","Realismo mágico","1967","Gabriel García Márquez","disponible","A-104","B-285","tiempo"
   "1984","978-8515242535","Ciencia Ficción/Distopía","1949","George Orwell","En tránsito","A-104","B-285","costo"
   "Orgullo y prejuicio","978-8748151955","Novela Romántica","1813","Jane Austen","Agotado","A-104","B-285","tiempo"
   "El Código Da Vinci","978-8747422978","Thriller/Misterio","2003","Dan Brown","Prestado","C-308","B-285","costo"
   ```

2. **Bibliotecas** 
   
   Formato:
   
   ```csv
   "ID","Nombre","Ubicación","t_ingreso","t_traspaso","dispatchInterval"
   "A-101","Almacén Principal","Madrid",28800,45000,3600
   "B-205","Centro de Distribución","Barcelona",32400,50400,1800
   "C-309","Plataforma Logística Sur","Valencia",39600,60300,2700
   "D-412","Depósito Temporal","Sevilla",27900,40500,5400
   ```

3. **Conexiones entre Bibliotecas** 
   
   Formato:
   
   ```csv
   "OrigenID","DestinoID","Tiempo","Costo"
   "A-101","B-205",12600,250.00
   "A-101","C-309",18000,400.00
   "C-309","B-205",9000,150.00
   "B-205","D-412",15120,320.00
   ```

**Validaciones:** Verificar existencia y formato de los archivos. Ignorar líneas mal formateadas sin detener la carga. Mostrar mensajes claros ante errores o rutas inexistentes.

---

## ⚙️ Consideraciones Técnicas

* **Todas las estructuras de datos deben ser implementadas desde cero.** (No se permite el uso de librerías estándar que implementen árboles, colas o tablas hash).
* La aplicación puede ser desarrollada en el lenguaje que los estudiantes prefieran, siempre que incluya una interfaz funcional (CLI o GUI).
* Las rutas, tiempos y operaciones deben poder **visualizarse o consultarse dinámicamente**.
* Se debe **documentar la complejidad** de cada estructura y justificar su uso (**Big O**).

---

## 🎁 Entrega Final

### Debe Incluir:

* **Código fuente completo**
* **Ejecutable compilado**
* **Manual técnico** con diagramas (Complejidad, Notación y TAD’s)
* **Manual de usuario**
* **Archivo README** con instrucciones de compilación.
