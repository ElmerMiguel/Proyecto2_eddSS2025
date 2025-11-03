from objetos.libro import Libro


class NodoLista:
    def __init__(self, libro: Libro):
        self.data = libro
        self.siguiente = None


class ListaLibros:

    def __init__(self):
        self.cabeza = None
        self.tamanio = 0 

    def insertar(self, libro: Libro):
        nuevo = NodoLista(libro)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo
        self.tamanio += 1 
    
    def eliminar(self, isbn: str) -> bool:
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
        actual = self.cabeza
        while actual:
            if actual.data.titulo == titulo:
                return actual.data
            actual = actual.siguiente
        return None

    def buscar_por_isbn(self, isbn: str) -> Libro | None:
        actual = self.cabeza
        while actual:
            if actual.data.isbn == isbn:
                return actual.data
            actual = actual.siguiente
        return None

    def mostrar_todos(self):
        if not self.cabeza:
            print("No hay libros en el catálogo.")
            return []

        # Recopilar libros
        actual = self.cabeza
        libros = []
        while actual:
            libros.append(actual.data)
            actual = actual.siguiente

        # Calcular anchos para formato tabular
        if libros:
            max_titulo = max(len("TITULO"), max(len(l.titulo) for l in libros))
            max_autor = max(len("AUTOR"), max(len(l.autor) for l in libros))
            max_anio = max(len("AÑO"), max(len(str(l.anio)) for l in libros))
            max_isbn = max(len("ISBN"), max(len(l.isbn) for l in libros))

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
        
        return libros