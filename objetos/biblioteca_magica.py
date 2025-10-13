# archivo: objetos/biblioteca_magica.py

from pathlib import Path
import csv
import subprocess
import time
from typing import List, Optional

from objetos.libro import Libro
from estructuras.lista_libros import ListaLibros
from estructuras.arbol_avl import ArbolAVL
from estructuras.arbol_b import ArbolB
from estructuras.tabla_hash import TablaHash
from estructuras.arbol_bplus import ArbolBPlus


class BibliotecaMagica:
    """
    Controlador principal de la biblioteca. Maneja las diferentes estructuras
    (lista secuencial, AVL por títulos, B por fechas, BST por ISBN, B+ por géneros).
    """

    def __init__(self):
        # Inicialización: los parámetros (orden, grado) están dejados
        # para que las implementaciones de las estructuras los manejen.
        self.lista_secuencial = ListaLibros()
        self.arbol_titulos = ArbolAVL()
        self.arbol_fechas = ArbolB(3)      # asume constructor por defecto o ajustable internamente
        self.tabla_isbn = TablaHash()
        self.arbol_generos = ArbolBPlus()

    # -----------------------
    # Operaciones CRUD
    # -----------------------
    def agregar_libro(self, libro: Libro) -> None:
        if not self.validar_isbn(libro.isbn):
            print("Error: ISBN invalido. Debe tener 13 dígitos numéricos.")
            return

        if self.tabla_isbn.buscar(libro.isbn) is not None:
            print(f"Error: Ya existe un libro con ISBN {libro.isbn}. No se puede agregar duplicado.")
            return

        if not libro.titulo or not libro.autor or not libro.genero:
            print("Error: Todos los campos son obligatorios.")
            return

        if libro.anio < 1000 or libro.anio > 2025:
            print("Error: Año debe estar entre 1000 y 2025.")
            return

        # Insertar en todas las estructuras
        self.lista_secuencial.insertar(libro)
        self.arbol_titulos.insertar(libro)
        self.arbol_fechas.insertar(libro)
        self.tabla_isbn.insertar(libro)
        self.arbol_generos.insertar(libro)

        print(f"Libro agregado correctamente: {libro.titulo}")

    def eliminar_libro(self, isbn: str) -> None:
        libro = self.tabla_isbn.buscar(isbn)
        if not libro:
            print(f"Libro con ISBN {isbn} no encontrado.")
            return

        titulo = libro.titulo
        genero = libro.genero
        anio = libro.anio

        self.lista_secuencial.eliminar(isbn)
        # Aquí asumimos que arbol_titulos.eliminar recibe el título
        self.arbol_titulos.eliminar(titulo)
        self.tabla_isbn.eliminar(isbn)
        # Para arbol_fechas y arbol_generos asumimos API que acepta (anio, isbn) o (genero, isbn)
        try:
            self.arbol_fechas.eliminar(anio, isbn)
        except TypeError:
            # si la implementación espera solo anio, ajustar más tarde
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
        # Asume que arbol_fechas.buscar_todos(anio) retorna lista de Libro
        if hasattr(self.arbol_fechas, "buscar_todos"):
            return self.arbol_fechas.buscar_todos(anio)
        # alternativa: buscar(anio)
        resultado = self.arbol_fechas.buscar(anio)
        return resultado if resultado is not None else []

    def buscar_por_genero(self, genero: str) -> List[Libro]:
        return self.arbol_generos.buscar(genero)

    def buscar_por_rango_fechas(self, inicio: int, fin: int):
        # Retorna lo que la estructura devuelva (en C++ devolvía ListaLibros)
        if hasattr(self.arbol_fechas, "buscar_por_rango_fechas"):
            return self.arbol_fechas.buscar_por_rango_fechas(inicio, fin)
        # si no existe, construimos una lista combinando años (poco eficiente)
        resultados = []
        for anio in range(inicio, fin + 1):
            resultados.extend(self.buscar_por_fecha(anio))
        return resultados

    # -----------------------
    # Importación CSV
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
                # intentamos manejar filas con comillas / separadores
                # Esperamos al menos 5 columnas: titulo,isbn,genero,anio,autor
                if len(fila) < 5:
                    # intentar unir columnas finales si el título contenía comas (básico)
                    print("(X) Línea ignorada (formato inesperado):", fila)
                    libros_ignorados += 1
                    continue

                titulo, isbn, genero, anio_str, autor = fila[0], fila[1], fila[2], fila[3], fila[4]

                titulo = titulo.strip().strip('"')
                isbn = isbn.strip().strip('"')
                genero = genero.strip().strip('"')
                anio_str = anio_str.strip().strip('"')
                autor = autor.strip().strip('"')

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

                if self.tabla_isbn.buscar(isbn) is not None:
                    print(f"(X) ISBN duplicado ignorado: {isbn} - {titulo}")
                    libros_ignorados += 1
                    continue

                libro = Libro(titulo=titulo, isbn=isbn, genero=genero, anio=anio, autor=autor)
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

    def exportar_bst(self, archivo: str) -> None:
        self.tabla_isbn.exportar_dot(archivo)
        self._generar_grafica_desde_dot(Path(archivo).with_suffix("").as_posix())

    def exportar_todos_los_dots(self) -> None:
        Path("graficos_arboles").mkdir(parents=True, exist_ok=True)
        print("Exportando todos los arboles a DOT y PNG/SVG...")
        print("=============================================")
        self.exportar_avl("graficos_arboles/arbol_avl_titulos.dot")
        self.exportar_b("graficos_arboles/arbol_b_fechas.dot")
        self.exportar_bst("graficos_arboles/tabla_hash_isbn.dot")
        self.exportar_bplus("graficos_arboles/arbol_bplus_generos.dot")
        print("=============================================")
        print("Archivos generados en carpeta 'graficos_arboles/'")

    def _generar_grafica_desde_dot(self, archivo_base: str) -> None:
        """
        Ejecuta Graphviz 'dot' para generar PNG y SVG desde .dot.
        archivo_base: ruta sin extensión (ejemplo: 'graficos/arbol')
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

    def medir_busqueda_isbn_bst(self, isbn: str) -> int:
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
    # Validaciones
    # -----------------------
    @staticmethod
    def validar_isbn(isbn: str) -> bool:
        isbn_limpio = "".join(ch for ch in isbn if ch.isdigit())
        if len(isbn_limpio) != 13:
            return False
        return isbn_limpio.isdigit()
