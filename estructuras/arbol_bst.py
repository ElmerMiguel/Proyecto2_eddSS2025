# archivo: estructuras/arbol_bst.py

from objetos.libro import Libro


class NodoBST:
    """
    Nodo de un Árbol Binario de Búsqueda.
    """
    def __init__(self, libro: Libro):
        self.data = libro
        self.izq: NodoBST | None = None
        self.der: NodoBST | None = None


class ArbolBST:
    """
    Implementación de un Árbol Binario de Búsqueda (BST) para libros.
    Permite insertar, buscar, eliminar y exportar a formato DOT.
    """

    def __init__(self):
        self.raiz: NodoBST | None = None

    def destruir(self, nodo: NodoBST | None):
        """
        Libera todos los nodos del árbol (manejado automáticamente en Python).
        """
        if nodo:
            self.destruir(nodo.izq)
            self.destruir(nodo.der)
            nodo.izq = nodo.der = None

    def insertar(self, libro: Libro):
        """
        Inserta un nuevo libro en el árbol según su ISBN.
        """
        self.raiz = self._insertar_rec(self.raiz, libro)

    def _insertar_rec(self, nodo: NodoBST | None, libro: Libro) -> NodoBST:
        if nodo is None:
            return NodoBST(libro)

        if libro.isbn < nodo.data.isbn:
            nodo.izq = self._insertar_rec(nodo.izq, libro)
        elif libro.isbn > nodo.data.isbn:
            nodo.der = self._insertar_rec(nodo.der, libro)
        return nodo

    def buscar(self, isbn: str) -> Libro | None:
        """
        Busca un libro por ISBN. Retorna el objeto Libro o None.
        """
        nodo = self._buscar_rec(self.raiz, isbn)
        return nodo.data if nodo else None

    def _buscar_rec(self, nodo: NodoBST | None, isbn: str) -> NodoBST | None:
        if not nodo or nodo.data.isbn == isbn:
            return nodo
        if isbn < nodo.data.isbn:
            return self._buscar_rec(nodo.izq, isbn)
        return self._buscar_rec(nodo.der, isbn)

    def _encontrar_min(self, nodo: NodoBST) -> NodoBST:
        while nodo.izq:
            nodo = nodo.izq
        return nodo

    def eliminar(self, isbn: str) -> bool:
        """
        Elimina un libro por ISBN. Retorna True si fue eliminado.
        """
        nodo_inicial = self.raiz
        self.raiz = self._eliminar_rec(self.raiz, isbn)
        return self.raiz != nodo_inicial or not self.buscar(isbn)

    def _eliminar_rec(self, nodo: NodoBST | None, isbn: str) -> NodoBST | None:
        if not nodo:
            return None

        if isbn < nodo.data.isbn:
            nodo.izq = self._eliminar_rec(nodo.izq, isbn)
        elif isbn > nodo.data.isbn:
            nodo.der = self._eliminar_rec(nodo.der, isbn)
        else:
            if not nodo.izq:
                return nodo.der
            elif not nodo.der:
                return nodo.izq
            temp = self._encontrar_min(nodo.der)
            nodo.data = temp.data
            nodo.der = self._eliminar_rec(nodo.der, temp.data.isbn)
        return nodo

    def mostrar_inorder(self):
        """
        Muestra los libros ordenados por ISBN.
        """
        print("Libros ordenados por ISBN:")
        self._inorder_rec(self.raiz)

    def _inorder_rec(self, nodo: NodoBST | None):
        if nodo:
            self._inorder_rec(nodo.izq)
            print(f"ISBN: {nodo.data.isbn} - {nodo.data.titulo}")
            self._inorder_rec(nodo.der)

    def listar_isbns(self):
        """
        Lista todos los libros en formato tabular, ordenados por ISBN.
        """
        libros = []
        self._recopilar_libros(self.raiz, libros)

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

        for libro in libros:
            fila = f"{libro.isbn.ljust(max_isbn + 2)}" \
                   f"{libro.titulo.ljust(max_titulo + 2)}" \
                   f"{libro.autor.ljust(max_autor + 2)}" \
                   f"{str(libro.anio).ljust(max_anio + 4)}"
            print(fila)

        print("=" * (max_isbn + max_titulo + max_autor + max_anio + 12))

    def _recopilar_libros(self, nodo: NodoBST | None, libros: list[Libro]):
        if nodo:
            self._recopilar_libros(nodo.izq, libros)
            libros.append(nodo.data)
            self._recopilar_libros(nodo.der, libros)

    def exportar_dot(self, archivo: str):
        """
        Exporta el árbol en formato Graphviz DOT.
        """
        with open(archivo, "w", encoding="utf-8") as out:
            out.write("digraph BST {\n")
            out.write('    node [shape=box, style="filled", fillcolor="lightblue"];\n')
            if self.raiz:
                self._exportar_dot_rec(self.raiz, out)
            out.write("}\n")

    def _exportar_dot_rec(self, nodo: NodoBST | None, out):
        if not nodo:
            return

        isbn_corto = nodo.data.isbn[-4:] if len(nodo.data.isbn) > 10 else nodo.data.isbn
        out.write(f'    "{nodo.data.isbn}" [label="{isbn_corto}"];\n')

        if nodo.izq:
            out.write(f'    "{nodo.data.isbn}" -> "{nodo.izq.data.isbn}";\n')
            self._exportar_dot_rec(nodo.izq, out)
        if nodo.der:
            out.write(f'    "{nodo.data.isbn}" -> "{nodo.der.data.isbn}";\n')
            self._exportar_dot_rec(nodo.der, out)
