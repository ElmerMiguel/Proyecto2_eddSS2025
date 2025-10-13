
from objetos.libro import Libro


class TablaHash:


    def __init__(self):
        self.raiz: dict[str, Libro] = {}

    def destruir(self, nodo=None):
        """
        Limpia toda la tabla hash.
        """
        self.raiz.clear()

    def insertar(self, libro: Libro):
        """
        Inserta un libro usando ISBN como clave.
        """
        self.raiz[libro.isbn] = libro

    def buscar(self, isbn: str) -> Libro | None:
        """
        Busca un libro por ISBN.
        """
        return self.raiz.get(isbn, None)

    def eliminar(self, isbn: str) -> bool:
        """
        Elimina un libro por ISBN.
        """
        return self.raiz.pop(isbn, None) is not None

    def mostrar_inorder(self):
        """
        Muestra libros ordenados por ISBN (simula inorder).
        """
        print("Libros ordenados por ISBN:")
        for isbn in sorted(self.raiz.keys()):
            libro = self.raiz[isbn]
            print(f"ISBN: {libro.isbn} - {libro.titulo}")

    def listar_isbns(self):
        """
        Lista todos los libros en formato tabular, ordenados por ISBN.
        """
        libros = list(self.raiz.values())
        if not libros:
            print("No hay ISBNs disponibles.")
            return

        max_isbn = max(len(l.isbn) for l in libros)
        max_titulo = max(len(l.titulo) for l in libros)
        max_autor = max(len(l.autor) for l in libros)
        max_anio = max(len(str(l.anio)) for l in libros)

        print(f"\nTotal de ISBNs: {len(libros)}")
        print("=" * (max_isbn + max_titulo + max_autor + max_anio + 12))

        encabezado = f"{'ISBN'.ljust(max_isbn + 2)}" \
                     f"{'TITULO'.ljust(max_titulo + 2)}" \
                     f"{'AUTOR'.ljust(max_autor + 2)}" \
                     f"{'AÑO'.ljust(max_anio + 4)}"
        print(encabezado)
        print("=" * (max_isbn + max_titulo + max_autor + max_anio + 12))

        for libro in sorted(libros, key=lambda l: l.isbn):
            fila = f"{libro.isbn.ljust(max_isbn + 2)}" \
                   f"{libro.titulo.ljust(max_titulo + 2)}" \
                   f"{libro.autor.ljust(max_autor + 2)}" \
                   f"{str(libro.anio).ljust(max_anio + 4)}"
            print(fila)

        print("=" * (max_isbn + max_titulo + max_autor + max_anio + 12))

    def exportar_dot(self, archivo: str):
        
        with open(archivo, "w", encoding="utf-8") as out:
            out.write("digraph BST {\n")
            out.write('    node [shape=box, style="filled", fillcolor="lightblue"];\n')
            for libro in self.raiz.values():
                isbn_corto = libro.isbn[-4:] if len(libro.isbn) > 10 else libro.isbn
                out.write(f'    "{libro.isbn}" [label="{isbn_corto}"];\n')
            out.write("}\n")
