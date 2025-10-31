from pathlib import Path
import csv
import subprocess
import time
from typing import List, Optional, Dict

from objetos.libro import Libro  # Asumimos que esta clase ahora soporta 9 atributos
from estructuras.lista_libros import ListaLibros
from estructuras.arbol_avl import ArbolAVL
from estructuras.arbol_b import ArbolB
from estructuras.tabla_hash import TablaHash
from estructuras.arbol_bplus import ArbolBPlus
# from estructuras.grafo import Grafo  # ELIMINADO

# AGREGAR ESTA CLASE ANTES DE ControladorCatalogo
class Coleccion:
    """Agrupa libros por temática. Permite ISBN duplicados dentro de la misma colección."""
    def __init__(self, nombre: str, descripcion: str = ""):
        self.nombre = nombre
        self.descripcion = descripcion
        self.libros = ListaLibros()
        self.isbns_en_coleccion = set()  # Para validación rápida


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
        # self.grafo_red = Grafo()  # ELIMINADO
        self.colecciones: Dict[str, Coleccion] = {}  # AGREGADO

    # -----------------------
    # Operaciones CRUD
    # -----------------------
    # REEMPLAZO COMPLETO DE agregar_libro
    def agregar_libro(self, libro: Libro, nombre_coleccion: str = "General") -> None:
        if not self.validar_isbn(libro.isbn):
            print("Error: ISBN invalido. Debe tener 13 dígitos numéricos.")
            return

        # Validar si ISBN existe en OTRA colección
        for col_nombre, col in self.colecciones.items():
            if col_nombre != nombre_coleccion and libro.isbn in col.isbns_en_coleccion:
                print(f"Error: ISBN {libro.isbn} ya existe en colección '{col_nombre}'. No se puede agregar a '{nombre_coleccion}'.")
                return

        if not libro.titulo or not libro.autor or not libro.genero:
            print("Error: Todos los campos son obligatorios.")
            return

        if libro.anio < 1000 or libro.anio > 2025:
            print("Error: Año debe estar entre 1000 y 2025.")
            return

        # Crear colección si no existe
        if nombre_coleccion not in self.colecciones:
            self.colecciones[nombre_coleccion] = Coleccion(nombre_coleccion)
            print(f"Nueva colección creada: {nombre_coleccion}")

        # Agregar a colección
        self.colecciones[nombre_coleccion].libros.insertar(libro)
        self.colecciones[nombre_coleccion].isbns_en_coleccion.add(libro.isbn)

        # Insertar en estructuras globales
        self.lista_secuencial.insertar(libro)
        self.arbol_titulos.insertar(libro)
        self.arbol_fechas.insertar(libro)
        self.tabla_isbn.insertar(libro)
        self.arbol_generos.insertar(libro)

        print(f"Libro agregado a colección '{nombre_coleccion}': {libro.titulo}")

    def eliminar_libro(self, isbn: str) -> None:
        libro = self.tabla_isbn.buscar(isbn)
        if not libro:
            print(f"Libro con ISBN {isbn} no encontrado.")
            return

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

    # -----------------------
    # Importación CSV (MODIFICADO para 9 campos)
    # -----------------------
    def cargar_desde_csv(self, ruta_archivo: str = "") -> None:
        base_dir = Path(".")
        if not ruta_archivo:
            carpeta = base_dir / "csv"
            archivos_csv = []
            if carpeta.exists() and carpeta.is_dir():
                for entry in carpeta.iterdir():
                    if entry.is_file() and entry.suffix.lower() == ".csv":
                        archivos_csv.append(entry.name)

            if archivos_csv:
                print("\n=== ARCHIVOS CSV DISPONIBLES EN ./csv ===")
                for i, nombre in enumerate(archivos_csv, start=1):
                    print(f"{i}. {nombre}")
                print("0. Ingresar ruta manual")
                opcion = input("Seleccione una opcion: ").strip()
                try:
                    opcion_i = int(opcion)
                except ValueError:
                    print("Opción inválida. Cancelando importación.")
                    return

                if opcion_i == 0:
                    ruta_archivo = input("Ingrese la ruta del archivo CSV: ").strip()
                elif 1 <= opcion_i <= len(archivos_csv):
                    ruta_archivo = str(carpeta / archivos_csv[opcion_i - 1])
                else:
                    print("Opción inválida. Cancelando importación.")
                    return
            else:
                ruta_archivo = input("No se encontraron archivos en ./csv.\nIngrese la ruta manual del archivo CSV: ").strip()

        ruta = Path(ruta_archivo)
        if not ruta.exists() or not ruta.is_file():
            print(f"Error: no se pudo abrir el archivo {ruta_archivo}")
            return

        libros_importados = 0
        libros_ignorados = 0

        with ruta.open(newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            try:
                encabezado = next(reader)  # leer cabecera
            except StopIteration:
                print("Archivo vacio o sin cabecera.")
                return

            for fila in reader:
                if not fila:
                    continue
                
                # ESPERAMOS AHORA 9 COLUMNAS PARA EL NUEVO FORMATO
                # "Titulo","ISBN","Genero","Año","Autor","Estado","ID BibliotecaOrigen","ID BibliotecaDestino","Prioridad"
                if len(fila) < 9: 
                    print(f"(X) Línea ignorada (formato inesperado, se esperaban 9 campos): {fila}")
                    libros_ignorados += 1
                    continue

                # Extraer los 9 campos
                titulo, isbn, genero, anio_str, autor, estado, id_origen, id_destino, prioridad = \
                    fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7], fila[8]

                # Limpieza de datos
                titulo = titulo.strip().strip('"')
                isbn = isbn.strip().strip('"')
                genero = genero.strip().strip('"')
                anio_str = anio_str.strip().strip('"')
                autor = autor.strip().strip('"')
                estado = estado.strip().strip('"') # Nuevo campo
                id_origen = id_origen.strip().strip('"') # Nuevo campo
                id_destino = id_destino.strip().strip('"') # Nuevo campo
                prioridad = prioridad.strip().strip('"') # Nuevo campo

                if not self.validar_isbn(isbn):
                    print(f"(X) ISBN invalido ignorado: {isbn} - {titulo}")
                    libros_ignorados += 1
                    continue

                try:
                    anio = int(anio_str)
                except Exception:
                    print(f"(X) Linea ignorada - anio invalido: {titulo}")
                    libros_ignorados += 1
                    continue
                
                # Validacion de Prioridad
                if prioridad.lower() not in ["tiempo", "costo"]:
                    print(f"(X) Prioridad invalida ignorada: {prioridad} - {titulo}")
                    libros_ignorados += 1
                    continue


                if self.tabla_isbn.buscar(isbn) is not None:
                    # NOTA: Esto evita duplicados globales. Si desea que los libros importados
                    # se agreguen a colecciones, debe llamar a self.agregar_libro(libro, "General")
                    # en lugar de insertar directamente.
                    print(f"(X) ISBN duplicado ignorado: {isbn} - {titulo}")
                    libros_ignorados += 1
                    continue

                # Creacion del objeto Libro con los 9 atributos
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
                
                # Insertar en estructuras globales (Asume que es parte del catálogo global)
                self.lista_secuencial.insertar(libro)
                self.arbol_titulos.insertar(libro)
                self.arbol_fechas.insertar(libro)
                self.tabla_isbn.insertar(libro)
                self.arbol_generos.insertar(libro)

                print(f"(√) Importado: {titulo}")
                libros_importados += 1

        print("\n=== RESUMEN IMPORTACION ===")
        print(f"Libros importados correctamente: {libros_importados}")
        print(f"Libros ignorados por duplicados/errores: {libros_ignorados}")
        print("Carga desde CSV completada.")

    # -----------------------
    # Exportar y generar gráficos (DOT -> PNG + SVG)
    # -----------------------
    def exportar_avl(self, archivo: str) -> None:
        self.arbol_titulos.exportar_dot(archivo)
        self._generar_grafica_desde_dot(Path(archivo).with_suffix("").as_posix())

    def exportar_b(self, archivo: str) -> None:
        self.arbol_fechas.exportar_dot(archivo)
        self._generar_grafica_desde_dot(Path(archivo).with_suffix("").as_posix())

    def exportar_bplus(self, archivo: str) -> None:
        self.arbol_generos.exportar_dot(archivo)
        self._generar_grafica_desde_dot(Path(archivo).with_suffix("").as_posix())

    def exportar_hash(self, archivo: str) -> None:
        self.tabla_isbn.exportar_dot(archivo)
        self._generar_grafica_desde_dot(Path(archivo).with_suffix("").as_posix())

    def exportar_todos_los_dots(self) -> None:
        Path("graficos_arboles").mkdir(parents=True, exist_ok=True)
        print("Exportando todos los arboles a DOT y PNG/SVG...")
        print("=============================================")
        self.exportar_avl("graficos_arboles/arbol_avl_titulos.dot")
        self.exportar_b("graficos_arboles/arbol_b_fechas.dot")
        self.exportar_hash("graficos_arboles/tabla_hash_isbn.dot")
        self.exportar_bplus("graficos_arboles/arbol_bplus_generos.dot")
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
    # Operaciones de Colección (Nuevas)
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

    # -----------------------
    # Validaciones
    # -----------------------
    @staticmethod
    def validar_isbn(isbn: str) -> bool:
        isbn_limpio = "".join(ch for ch in isbn if ch.isdigit())
        if len(isbn_limpio) != 13:
            return False
        return isbn_limpio.isdigit()