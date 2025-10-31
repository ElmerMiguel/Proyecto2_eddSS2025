from objetos.libro import Libro


class NodoLista:
    """
    Nodo individual de la lista enlazada de libros.
    """
    def __init__(self, libro: Libro):
        self.data = libro
        self.siguiente = None


class ListaLibros:
    """
    Lista enlazada simple que almacena objetos de tipo Libro.
    Permite insertar, eliminar, buscar y mostrar libros.
    """

    def __init__(self):
        self.cabeza = None
        self.tamanio = 0 

    def insertar(self, libro: Libro):
        """
        Inserta un nuevo libro al inicio de la lista.
        """
        nuevo = NodoLista(libro)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo
        self.tamanio += 1 

    def eliminar(self, isbn: str) -> bool:
        """
        Elimina un libro de la lista por su ISBN.
        Retorna True si fue eliminado, False si no se encontró.
        """
        actual = self.cabeza
        anterior = None

        while actual:
            if actual.data.isbn == isbn:
                if anterior:
                    anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente
                
                self.tamanio -= 1
                return True 
            
            anterior = actual
            actual = actual.siguiente

        return False
    
    
    def buscar_por_titulo(self, titulo: str) -> Libro | None:
        """
        Busca un libro por su título.
        Retorna el libro si lo encuentra, None si no.
        """
        actual = self.cabeza
        while actual:
            if actual.data.titulo == titulo:
                return actual.data
            actual = actual.siguiente
        return None

    def buscar_por_isbn(self, isbn: str) -> Libro | None:
        """
        Busca un libro por su ISBN.
        Retorna el libro si lo encuentra, None si no.
        """
        actual = self.cabeza
        while actual:
            if actual.data.isbn == isbn:
                return actual.data
            actual = actual.siguiente
        return None

    def mostrar_todos(self):
        """
        Muestra todos los libros en formato tabular.
        """
        if not self.cabeza:
            print("No hay libros en el rango especificado.")
            return

        # Calcular anchos máximos de columnas
        max_titulo = 6
        max_autor = 5
        max_anio = 3
        max_isbn = 4

        actual = self.cabeza
        libros = []

        while actual:
            libro = actual.data
            libros.append(libro)
            max_titulo = max(max_titulo, len(libro.titulo))
            max_autor = max(max_autor, len(libro.autor))
            max_anio = max(max_anio, len(str(libro.anio)))
            max_isbn = max(max_isbn, len(libro.isbn))
            actual = actual.siguiente

        print(f"\nTotal de libros encontrados: {len(libros)}")
        print("=" * (max_titulo + max_autor + max_anio + max_isbn + 12))

        encabezado = f"{'TITULO'.ljust(max_titulo + 2)}" \
                     f"{'AUTOR'.ljust(max_autor + 2)}" \
                     f"{'AÑO'.ljust(max_anio + 4)}" \
                     f"{'ISBN'.ljust(max_isbn + 2)}"
        print(encabezado)
        print("=" * (max_titulo + max_autor + max_anio + max_isbn + 12))

        for libro in libros:
            fila = f"{libro.titulo.ljust(max_titulo + 2)}" \
                   f"{libro.autor.ljust(max_autor + 2)}" \
                   f"{str(libro.anio).ljust(max_anio + 4)}" \
                   f"{libro.isbn.ljust(max_isbn + 2)}"
            print(fila)

        print("=" * (max_titulo + max_autor + max_anio + max_isbn + 12))