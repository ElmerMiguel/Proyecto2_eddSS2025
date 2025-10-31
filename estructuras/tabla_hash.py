from objetos.libro import Libro
from typing import Optional, List


class NodoHash:
    def __init__(self, libro: Libro):
        self.libro = libro
        self.siguiente: Optional['NodoHash'] = None


class TablaHash:
    def __init__(self, capacidad_inicial: int = 17):
        self.capacidad = self._siguiente_primo(capacidad_inicial)
        self.tabla: List[Optional[NodoHash]] = [None] * self.capacidad
        self.cantidad = 0
        self.factor_carga_maximo = 0.75

    # -------------------------------------------------
    # Función hash
    # -------------------------------------------------
    def _hash(self, isbn: str) -> int:
        hash_val = 0
        A = 0.6180339887  # Constante de Knuth (proporción áurea)
        
        for i, char in enumerate(isbn):
            hash_val += ord(char) * (31 ** i)
        
        hash_val = int(self.capacidad * ((hash_val * A) % 1))
        return hash_val % self.capacidad

    # -------------------------------------------------
    # Utilidades
    # -------------------------------------------------
    def _es_primo(self, n: int) -> bool:
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n ** 0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    def _siguiente_primo(self, n: int) -> int:
        while not self._es_primo(n):
            n += 1
        return n

    def _factor_carga(self) -> float:
        return self.cantidad / self.capacidad

    def _rehash(self):
        print(f"Rehashing: {self.capacidad} -> ", end="")
        
        tabla_vieja = self.tabla
        
        self.capacidad = self._siguiente_primo(self.capacidad * 2)
        self.tabla = [None] * self.capacidad
        self.cantidad = 0
        
        print(f"{self.capacidad}")
        
        for bucket in tabla_vieja:
            actual = bucket
            while actual:
                self.insertar(actual.libro)
                actual = actual.siguiente

    # -------------------------------------------------
    # Operaciones CRUD
    # -------------------------------------------------
    def insertar(self, libro: Libro) -> bool:
        indice = self._hash(libro.isbn)
        actual = self.tabla[indice]
        
        while actual:
            if actual.libro.isbn == libro.isbn:
                print(f"El ISBN {libro.isbn} ya existe en la tabla")
                return False
            actual = actual.siguiente
        
        nuevo_nodo = NodoHash(libro)
        nuevo_nodo.siguiente = self.tabla[indice]
        self.tabla[indice] = nuevo_nodo
        self.cantidad += 1
        
        if self._factor_carga() > self.factor_carga_maximo:
            self._rehash()
        
        return True

    def buscar(self, isbn: str) -> Optional[Libro]:
        indice = self._hash(isbn)
        actual = self.tabla[indice]
        
        while actual:
            if actual.libro.isbn == isbn:
                return actual.libro
            actual = actual.siguiente
        
        return None

    def eliminar(self, isbn: str) -> bool:
        indice = self._hash(isbn)
        actual = self.tabla[indice]
        anterior = None
        
        while actual:
            if actual.libro.isbn == isbn:
                if anterior:
                    anterior.siguiente = actual.siguiente
                else:
                    self.tabla[indice] = actual.siguiente
                self.cantidad -= 1
                return True
            anterior = actual
            actual = actual.siguiente
        
        return False

    def destruir(self):
        self.tabla = [None] * self.capacidad
        self.cantidad = 0

    # -------------------------------------------------
    # Mostrar y listar
    # -------------------------------------------------
    def mostrar_inorder(self):
        libros = []
        for bucket in self.tabla:
            actual = bucket
            while actual:
                libros.append(actual.libro)
                actual = actual.siguiente
        
        libros.sort(key=lambda l: l.isbn)
        
        print("\nLibros ordenados por ISBN:")
        print("=" * 80)
        for libro in libros:
            print(f"ISBN: {libro.isbn} - {libro.titulo}")
        print("=" * 80)

    def listar_isbns(self):
        libros = []
        for bucket in self.tabla:
            actual = bucket
            while actual:
                libros.append(actual.libro)
                actual = actual.siguiente
        
        if not libros:
            print("No hay ISBNs disponibles.")
            return
        
        libros.sort(key=lambda l: l.isbn)
        
        max_isbn = max(len(l.isbn) for l in libros)
        max_titulo = max(len(l.titulo) for l in libros)
        max_autor = max(len(l.autor) for l in libros)
        max_anio = max(len(str(l.anio)) for l in libros)
        
        ancho_total = max_isbn + max_titulo + max_autor + max_anio + 12
        
        print(f"\nTotal de ISBNs: {self.cantidad}")
        print(f"Factor de carga: {self._factor_carga():.2%}")
        print(f"Capacidad de la tabla: {self.capacidad}")
        print("=" * ancho_total)
        
        encabezado = (f"{'ISBN'.ljust(max_isbn + 2)}"
                      f"{'TITULO'.ljust(max_titulo + 2)}"
                      f"{'AUTOR'.ljust(max_autor + 2)}"
                      f"{'AÑO'.ljust(max_anio + 4)}")
        print(encabezado)
        print("=" * ancho_total)
        
        for libro in libros:
            fila = (f"{libro.isbn.ljust(max_isbn + 2)}"
                    f"{libro.titulo.ljust(max_titulo + 2)}"
                    f"{libro.autor.ljust(max_autor + 2)}"
                    f"{str(libro.anio).ljust(max_anio + 4)}")
            print(fila)
        
        print("=" * ancho_total)

    def mostrar_estadisticas(self):
        colisiones = 0
        max_cadena = 0
        buckets_usados = 0
        
        for bucket in self.tabla:
            if bucket:
                buckets_usados += 1
                longitud = 0
                actual = bucket
                while actual:
                    longitud += 1
                    actual = actual.siguiente
                if longitud > 1:
                    colisiones += longitud - 1
                max_cadena = max(max_cadena, longitud)
        
        print("\nESTADÍSTICAS DE LA TABLA HASH")
        print("=" * 50)
        print(f"Capacidad total:         {self.capacidad}")
        print(f"Elementos almacenados:   {self.cantidad}")
        print(f"Buckets utilizados:      {buckets_usados}")
        print(f"Buckets vacíos:          {self.capacidad - buckets_usados}")
        print(f"Factor de carga:         {self._factor_carga():.2%}")
        print(f"Total de colisiones:     {colisiones}")
        print(f"Cadena más larga:        {max_cadena} elementos")
        print("=" * 50)

    # -------------------------------------------------
    # Exportar a DOT
    # -------------------------------------------------
    def exportar_dot(self, archivo: str):
        with open(archivo, "w", encoding="utf-8") as out:
            out.write("digraph TablaHash {\n")
            out.write('    rankdir=LR;\n')
            out.write('    node [shape=record];\n\n')
            
            # Crear nodo de la tabla (arreglo)
            out.write('    tabla [label="')
            labels = []
            for i in range(self.capacidad):
                labels.append(f'<f{i}> {i}')
            out.write('|'.join(labels))
            out.write('", shape=record, style=filled, fillcolor=lightgray];\n\n')
            
            # Crear nodos para las cadenas
            for i in range(self.capacidad):
                actual = self.tabla[i]
                if actual:
                    j = 0
                    while actual:
                        nodo_id = f"n{i}_{j}"
                        isbn_corto = actual.libro.isbn[-6:]
                        out.write(f'    {nodo_id} [label="{isbn_corto}\\n{actual.libro.titulo[:15]}...", ')
                        out.write('style=filled, fillcolor=lightblue];\n')
                        
                        if j == 0:
                            out.write(f'    tabla:f{i} -> {nodo_id};\n')
                        else:
                            out.write(f'    n{i}_{j-1} -> {nodo_id};\n')
                        
                        actual = actual.siguiente
                        j += 1
                    out.write('\n')
            
            out.write("}\n")
            
        print(f"Archivo DOT generado: {archivo}")