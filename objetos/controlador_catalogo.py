from pathlib import Path
import csv
import subprocess
import time
from typing import List, Optional, Dict

from objetos.libro import Libro
from estructuras.lista_libros import ListaLibros
from estructuras.arbol_avl import ArbolAVL
from estructuras.arbol_b import ArbolB
from estructuras.tabla_hash import TablaHash
from estructuras.arbol_bplus import ArbolBPlus
from estructuras.pila import Pila


class Coleccion:
    """Agrupa libros por temática. Permite ISBN duplicados dentro de la misma colección."""
    def __init__(self, nombre: str, descripcion: str = ""):
        self.nombre = nombre
        self.descripcion = descripcion
        self.libros = ListaLibros()
        self.isbns_en_coleccion = set()


class ControladorCatalogo:
    """
    Controlador de catalogo de libros.
    Maneja las diferentes estructuras de datos para un conjunto de libros.
    """
    def __init__(self):
        self.lista_secuencial = ListaLibros()
        self.arbol_titulos = ArbolAVL()
        self.arbol_fechas = ArbolB(3)
        self.tabla_isbn = TablaHash()
        self.arbol_generos = ArbolBPlus()
        self.colecciones: Dict[str, Coleccion] = {}
        self.pila_operaciones = Pila()
        self.pila_devoluciones = Pila()

    # -----------------------
    # Accesores para GUI / Visualizaciones
    # -----------------------
    def obtener_estructura(self, clave: str):
        """Retorna la estructura solicitada para visualizacion."""
        mapa = {
            "avl": self.arbol_titulos,
            "b": self.arbol_fechas,
            "bplus": self.arbol_generos,
            "hash": self.tabla_isbn,
            "lista": self.lista_secuencial, # Opcional, pero util para mostrar
        }
        return mapa.get(clave.lower())

    def exportar_estructura_dot(self, clave: str, archivo_dot: str) -> None:
        """Genera un archivo DOT de la estructura solicitada."""
        estructura = self.obtener_estructura(clave)
        if not estructura or not hasattr(estructura, "exportar_dot"):
            raise ValueError(f"Estructura '{clave}' no soportada para exportacion DOT")
        estructura.exportar_dot(archivo_dot)

    # -----------------------
    # Operaciones CRUD
    # -----------------------
   
   
    def agregar_libro(self, libro: Libro, nombre_coleccion: str = "General") -> None:
        """Agrega un libro a todas las estructuras de datos"""
        
        if not libro.titulo or not libro.autor or not libro.genero:
            print("Error: Todos los campos son obligatorios.")
            return

        if libro.anio < 1000 or libro.anio > 2025:
            print("Error: Año debe estar entre 1000 y 2025.")
            return

        for col_nombre, col in self.colecciones.items():
            if col_nombre != nombre_coleccion and libro.isbn in col.isbns_en_coleccion:
                print(f"Error: ISBN {libro.isbn} ya existe en colección '{col_nombre}'")
                return

        # Crear colección si no existe
        if nombre_coleccion not in self.colecciones:
            self.colecciones[nombre_coleccion] = Coleccion(nombre_coleccion)
            print(f"Nueva colección creada: {nombre_coleccion}")

        # Agregar a colección
        self.colecciones[nombre_coleccion].libros.insertar(libro)
        self.colecciones[nombre_coleccion].isbns_en_coleccion.add(libro.isbn)

        # ✅ INSERTAR EN TODAS LAS ESTRUCTURAS GLOBALES
        self.lista_secuencial.insertar(libro)
        self.arbol_titulos.insertar(libro)
        self.arbol_fechas.insertar(libro)
        # FIX: REVERTIR - TablaHash solo necesita el libro
        self.tabla_isbn.insertar(libro)  # ✅ CORRECTO: solo libro
        self.arbol_generos.insertar(libro)
        
        # Guardar en pila de operaciones
        self.pila_operaciones.push(("agregar", libro))

        print(f"Libro agregado a colección '{nombre_coleccion}': {libro.titulo}")
   
   
   
    def eliminar_libro(self, isbn: str) -> None:
        libro = self.tabla_isbn.buscar(isbn)
        if not libro:
            print(f"Libro con ISBN {isbn} no encontrado.")
            return

        # Guardar en pila ANTES de eliminar
        self.pila_operaciones.push(("eliminar", libro))

        titulo = libro.titulo
        genero = libro.genero
        anio = libro.anio
        
        # Eliminar de colecciones 
        for col in self.colecciones.values():
            if isbn in col.isbns_en_coleccion:
                col.libros.eliminar(isbn) 
                col.isbns_en_coleccion.discard(isbn) 

        self.lista_secuencial.eliminar(isbn)
        self.arbol_titulos.eliminar(titulo)
        self.tabla_isbn.eliminar(isbn)
        
        try:
            self.arbol_fechas.eliminar(anio, isbn)
        except TypeError:
            self.arbol_fechas.eliminar(anio)
        try:
            self.arbol_generos.eliminar(genero, isbn)
        except TypeError:
            self.arbol_generos.eliminar(genero)

        print(f"Libro eliminado correctamente: {titulo}")

    # -----------------------
    # Búsquedas / Listados
    # -----------------------
    def buscar_por_titulo(self, titulo: str) -> Optional[Libro]:
        return self.arbol_titulos.buscar(titulo)

    def buscar_por_isbn(self, isbn: str) -> Optional[Libro]:
        return self.tabla_isbn.buscar(isbn)

    def buscar_por_fecha(self, anio: int) -> List[Libro]:
        if hasattr(self.arbol_fechas, "buscar_todos"):
            return self.arbol_fechas.buscar_todos(anio)
        resultado = self.arbol_fechas.buscar(anio)
        return resultado if resultado is not None else []

    def buscar_por_genero(self, genero: str) -> List[Libro]:
        return self.arbol_generos.buscar(genero)

    def buscar_por_rango_fechas(self, inicio: int, fin: int):
        if hasattr(self.arbol_fechas, "buscar_por_rango_fechas"):
            return self.arbol_fechas.buscar_por_rango_fechas(inicio, fin)
        resultados = []
        for anio in range(inicio, fin + 1):
            resultados.extend(self.buscar_por_fecha(anio))
        return resultados

    def listar_por_titulo_ordenado(self) -> List[Libro]:
        """Retorna lista de libros ordenados por título (usando AVL inorder)."""
        return self.arbol_titulos.inorder()

    def obtener_generos_unicos(self) -> List[str]:
        """Retorna lista de géneros únicos ordenados."""
        return self.arbol_generos.obtener_generos()

    # -----------------------
    # Operaciones con Pilas
    # -----------------------
    def deshacer_ultima_operacion(self) -> bool:
        """Deshace la última operación (agregar/eliminar)."""
        if self.pila_operaciones.esta_vacia():
            print("No hay operaciones para deshacer.")
            return False
        
        operacion, libro = self.pila_operaciones.pop()
        
        if operacion == "agregar":
            # Deshacer agregar = eliminar (sin guardar en pila)
            print(f"Deshaciendo agregado de: {libro.titulo}")
            
            # Eliminar de colecciones
            for col in self.colecciones.values():
                if libro.isbn in col.isbns_en_coleccion:
                    col.libros.eliminar(libro.isbn)
                    col.isbns_en_coleccion.discard(libro.isbn)
            
            # Eliminar de estructuras globales
            self.lista_secuencial.eliminar(libro.isbn)
            self.arbol_titulos.eliminar(libro.titulo)
            self.tabla_isbn.eliminar(libro.isbn)
            try:
                self.arbol_fechas.eliminar(libro.anio, libro.isbn)
            except TypeError:
                self.arbol_fechas.eliminar(libro.anio)
            try:
                self.arbol_generos.eliminar(libro.genero, libro.isbn)
            except TypeError:
                self.arbol_generos.eliminar(libro.genero)
        
        elif operacion == "eliminar":
            # Deshacer eliminar = agregar
            print(f"Deshaciendo eliminación de: {libro.titulo}")
            # Quitar el push automático temporalmente
            temp_push = self.pila_operaciones.push
            self.pila_operaciones.push = lambda x: None
            self.agregar_libro(libro, "General") # Asume que el libro original fue a General
            self.pila_operaciones.push = temp_push
        
        return True

    def apilar_devolucion(self, libro: Libro) -> None:
        """Apila un libro devuelto."""
        self.pila_devoluciones.push(libro)
        libro.estado = "disponible"
        print(f"Libro apilado en devoluciones: {libro.titulo}")

    def obtener_devoluciones(self) -> List[Libro]:
        """Retorna lista de libros en pila de devoluciones."""
        libros = []
        actual = self.pila_devoluciones.tope
        while actual:
            libros.append(actual.libro)
            actual = actual.siguiente
        return libros

    # -----------------------
    # Importación CSV (MODIFICADO para 9 campos)
    # -----------------------
    def cargar_desde_csv(self, ruta_archivo: str, nombre_coleccion: str = "General", red_bibliotecas=None) -> int:
        """
        Carga libros desde CSV con 9 campos según enunciado.
        """
        ruta = Path(ruta_archivo)
        if not ruta.exists():
            print(f"Error: El archivo {ruta_archivo} no existe.")
            return 0

        contador = 0

        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                reader = csv.reader(archivo)
                try:
                    encabezado = next(reader)  # ✅ SALTAR ENCABEZADO
                    # print(f"Encabezado libros: {encabezado}") # Se comenta para evitar comentarios
                except StopIteration:
                    print("Archivo vacío o sin encabezado.")
                    return 0
                
                for fila in reader:
                    if not fila or len(fila) < 9:
                        # print(f"Fila incompleta ignorada: {fila}") # Se comenta para evitar comentarios
                        continue
                        
                    try:
                        # ✅ USAR ÍNDICES DIRECTOS
                        titulo = fila[0].strip().strip('"')
                        isbn = fila[1].strip().strip('"')
                        genero = fila[2].strip().strip('"')
                        anio = int(fila[3].strip().strip('"'))
                        autor = fila[4].strip().strip('"')
                        estado = fila[5].strip().strip('"')
                        id_origen = fila[6].strip().strip('"')
                        id_destino = fila[7].strip().strip('"')
                        prioridad = fila[8].strip().strip('"')
                        
                        # Validar campos obligatorios
                        if not all([titulo, isbn, genero, autor]):
                            # print(f"Campos obligatorios faltantes: {fila}") # Se comenta para evitar comentarios
                            continue
                        
                        # Crear libro
                        libro = Libro(
                            titulo=titulo,
                            isbn=isbn,
                            genero=genero,
                            anio=anio,
                            autor=autor,
                            estado=estado,
                            biblioteca_origen=id_origen,
                            biblioteca_destino=id_destino,
                            prioridad=prioridad
                        )
                        
                        # ✅ DISTRIBUCIÓN CORRECTA POR BIBLIOTECA
                        if red_bibliotecas and id_origen in red_bibliotecas.bibliotecas:
                            # Agregar a la biblioteca correcta
                            red_bibliotecas.bibliotecas[id_origen].catalogo_local.agregar_libro(libro, nombre_coleccion)
                            # print(f"✅ Libro '{titulo}' agregado a biblioteca {id_origen}") # Se comenta para evitar comentarios
                            
                            # ✅ SI HAY DESTINO DIFERENTE, PROGRAMAR TRANSFERENCIA
                            if id_destino and id_destino != id_origen and id_destino in red_bibliotecas.bibliotecas:
                                red_bibliotecas.programar_transferencia(libro.isbn, id_origen, id_destino, prioridad)
                                # print(f"📦 Transferencia programada: {titulo} de {id_origen} a {id_destino}") # Se comenta para evitar comentarios
                        else:
                            # Agregar al catálogo actual (primera biblioteca)
                            self.agregar_libro(libro, nombre_coleccion)
                            # print(f"✅ Libro '{titulo}' agregado a catálogo actual") # Se comenta para evitar comentarios
                        
                        contador += 1
                        
                    except Exception: # Se elimina la impresión de la excepción para evitar comentarios
                        # print(f"❌ Error procesando fila {fila}: {e}") # Se comenta para evitar comentarios
                        continue

            print(f"\n✅ Carga completada: {contador} libros importados")
            return contador
            
        except Exception as e:
            print(f"Error al cargar libros: {e}")
            return 0

    # -----------------------
    # Exportar y generar gráficos (DOT -> PNG + SVG)
    # -----------------------
    def exportar_avl(self, archivo: str) -> None:
        self.exportar_estructura_dot("avl", archivo)
        self._generar_grafica_desde_dot(Path(archivo).with_suffix("").as_posix())

    def exportar_b(self, archivo: str) -> None:
        self.exportar_estructura_dot("b", archivo)
        self._generar_grafica_desde_dot(Path(archivo).with_suffix("").as_posix())

    def exportar_bplus(self, archivo: str) -> None:
        self.exportar_estructura_dot("bplus", archivo)
        self._generar_grafica_desde_dot(Path(archivo).with_suffix("").as_posix())

    def exportar_hash(self, archivo: str) -> None:
        self.exportar_estructura_dot("hash", archivo)
        self._generar_grafica_desde_dot(Path(archivo).with_suffix("").as_posix())

    def exportar_todos_los_dots(self) -> None:
        Path("graficos_arboles").mkdir(parents=True, exist_ok=True)
        print("Exportando todos los arboles a DOT y PNG/SVG...")
        print("=============================================")
        # Uso de la nueva función unificada
        self.exportar_estructura_dot("avl", "graficos_arboles/arbol_avl_titulos.dot")
        self.exportar_estructura_dot("b", "graficos_arboles/arbol_b_fechas.dot")
        self.exportar_estructura_dot("hash", "graficos_arboles/tabla_hash_isbn.dot")
        self.exportar_estructura_dot("bplus", "graficos_arboles/arbol_bplus_generos.dot")
        
        # Generación de gráficas (separado del DOT)
        self._generar_grafica_desde_dot("graficos_arboles/arbol_avl_titulos")
        self._generar_grafica_desde_dot("graficos_arboles/arbol_b_fechas")
        self._generar_grafica_desde_dot("graficos_arboles/tabla_hash_isbn")
        self._generar_grafica_desde_dot("graficos_arboles/arbol_bplus_generos")

        print("=============================================")
        print("Archivos generados en carpeta 'graficos_arboles/'")

    def _generar_grafica_desde_dot(self, archivo_base: str) -> None:
        """
        Ejecuta Graphviz 'dot' para generar PNG y SVG desde .dot.
        """
        dot_file = Path(f"{archivo_base}.dot")
        png_file = Path(f"{archivo_base}.png")
        svg_file = Path(f"{archivo_base}.svg")

        if not dot_file.exists():
            print(f"(X) Archivo DOT no encontrado: {dot_file}")
            return

        # Generar PNG
        try:
            subprocess.run(["dot", "-Tpng", str(dot_file), "-o", str(png_file)],
                        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if png_file.exists():
                print(f"(√) PNG generado: {png_file}")
            else:
                print(f"(X) Error generando PNG para: {archivo_base}")
        except Exception:
            print(f"(X) Error generando PNG para: {archivo_base}")

        # Generar SVG
        try:
            subprocess.run(["dot", "-Tsvg", str(dot_file), "-o", str(svg_file)],
                        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if svg_file.exists():
                print(f"(√) SVG generado: {svg_file}")
            else:
                print(f"(X) Error generando SVG para: {archivo_base}")
        except Exception:
            print(f"(X) Error generando SVG para: {archivo_base}")

    # -----------------------
    # Medición de tiempos (microsegundos)
    # -----------------------
    def medir_busqueda_titulo_secuencial(self, titulo: str) -> int:
        start = time.perf_counter()
        self.lista_secuencial.buscar_por_titulo(titulo)
        end = time.perf_counter()
        return int((end - start) * 1_000_000)

    def medir_busqueda_titulo_avl(self, titulo: str) -> int:
        start = time.perf_counter()
        self.arbol_titulos.buscar(titulo)
        end = time.perf_counter()
        return int((end - start) * 1_000_000)

    def medir_busqueda_isbn_hash(self, isbn: str) -> int:
        start = time.perf_counter()
        self.tabla_isbn.buscar(isbn)
        end = time.perf_counter()
        return int((end - start) * 1_000_000)

    def medir_busqueda_isbn_secuencial(self, isbn: str) -> int:
        start = time.perf_counter()
        self.lista_secuencial.buscar_por_isbn(isbn)
        end = time.perf_counter()
        return int((end - start) * 1_000_000)

    # -----------------------
    # Mostradores / listados
    # -----------------------
    def mostrar_resumen_libros(self) -> None:
        print("Libros en el sistema:")
        self.lista_secuencial.mostrar_todos()
        print()

    def mostrar_titulos_disponibles(self) -> None:
        self.arbol_titulos.listar_titulos()

    def mostrar_isbns_disponibles(self) -> None:
        self.tabla_isbn.listar_isbns()

    def mostrar_anios_disponibles(self) -> None:
        self.arbol_fechas.listar_anios()

    def mostrar_generos_disponibles(self) -> None:
        self.arbol_generos.listar_generos()
    
    # -----------------------
    # Operaciones de Colección
    # -----------------------
    def listar_colecciones(self) -> None:
        if not self.colecciones:
            print("No hay colecciones.")
            return
        print("\n=== COLECCIONES ===")
        for nombre, col in self.colecciones.items():
            print(f"- {nombre}: {col.libros.tamanio} libros")

    def listar_libros_coleccion(self, nombre_coleccion: str) -> None:
        if nombre_coleccion not in self.colecciones:
            print(f"Colección '{nombre_coleccion}' no existe.")
            return
        print(f"\n=== LIBROS EN '{nombre_coleccion}' ===")
        self.colecciones[nombre_coleccion].libros.mostrar_todos()