from objetos.libro import Libro

class NodoAVL:
    def __init__(self, libro: Libro):
        self.data = libro
        self.izq = None
        self.der = None
        self.altura = 1


class ArbolAVL:
    def __init__(self):
        self.raiz = None

    # --- Utilidades internas ---
    def _altura(self, nodo):
        return nodo.altura if nodo else 0

    def _balance(self, nodo):
        return self._altura(nodo.izq) - self._altura(nodo.der) if nodo else 0

    def _rotacion_derecha(self, y):
        x = y.izq
        T2 = x.der
        x.der = y
        y.izq = T2

        y.altura = 1 + max(self._altura(y.izq), self._altura(y.der))
        x.altura = 1 + max(self._altura(x.izq), self._altura(x.der))
        return x

    def _rotacion_izquierda(self, x):
        y = x.der
        T2 = y.izq
        y.izq = x
        x.der = T2

        x.altura = 1 + max(self._altura(x.izq), self._altura(x.der))
        y.altura = 1 + max(self._altura(y.izq), self._altura(y.der))
        return y

    # --- Inserción ---
    def _insertar(self, nodo, libro):
        if not nodo:
            return NodoAVL(libro)

        if libro.titulo < nodo.data.titulo:
            nodo.izq = self._insertar(nodo.izq, libro)
        elif libro.titulo > nodo.data.titulo:
            nodo.der = self._insertar(nodo.der, libro)
        else:
            return nodo  # duplicado

        nodo.altura = 1 + max(self._altura(nodo.izq), self._altura(nodo.der))
        balance = self._balance(nodo)

        # Casos de rotación
        if balance > 1 and libro.titulo < nodo.izq.data.titulo:
            return self._rotacion_derecha(nodo)
        if balance < -1 and libro.titulo > nodo.der.data.titulo:
            return self._rotacion_izquierda(nodo)
        if balance > 1 and libro.titulo > nodo.izq.data.titulo:
            nodo.izq = self._rotacion_izquierda(nodo.izq)
            return self._rotacion_derecha(nodo)
        if balance < -1 and libro.titulo < nodo.der.data.titulo:
            nodo.der = self._rotacion_derecha(nodo.der)
            return self._rotacion_izquierda(nodo)

        return nodo

    def insertar(self, libro: Libro):
        self.raiz = self._insertar(self.raiz, libro)

    # --- Búsqueda ---
    def _buscar(self, nodo, titulo: str):
        if not nodo:
            return None
        if titulo == nodo.data.titulo:
            return nodo
        elif titulo < nodo.data.titulo:
            return self._buscar(nodo.izq, titulo)
        else:
            return self._buscar(nodo.der, titulo)

    def buscar(self, titulo: str):
        nodo = self._buscar(self.raiz, titulo)
        return nodo.data if nodo else None

    # --- Eliminación ---
    def _encontrar_min(self, nodo):
        actual = nodo
        while actual and actual.izq:
            actual = actual.izq
        return actual

    def _eliminar(self, nodo, titulo):
        if not nodo:
            return nodo

        if titulo < nodo.data.titulo:
            nodo.izq = self._eliminar(nodo.izq, titulo)
        elif titulo > nodo.data.titulo:
            nodo.der = self._eliminar(nodo.der, titulo)
        else:
            # Nodo con 1 o 0 hijos
            if not nodo.izq or not nodo.der:
                nodo = nodo.izq if nodo.izq else nodo.der
            else:
                temp = self._encontrar_min(nodo.der)
                nodo.data = temp.data
                nodo.der = self._eliminar(nodo.der, temp.data.titulo)

        if not nodo:
            return nodo

        nodo.altura = 1 + max(self._altura(nodo.izq), self._altura(nodo.der))
        balance = self._balance(nodo)

        # Rotaciones de equilibrio
        if balance > 1 and self._balance(nodo.izq) >= 0:
            return self._rotacion_derecha(nodo)
        if balance < -1 and self._balance(nodo.der) <= 0:
            return self._rotacion_izquierda(nodo)
        if balance > 1 and self._balance(nodo.izq) < 0:
            nodo.izq = self._rotacion_izquierda(nodo.izq)
            return self._rotacion_derecha(nodo)
        if balance < -1 and self._balance(nodo.der) > 0:
            nodo.der = self._rotacion_derecha(nodo.der)
            return self._rotacion_izquierda(nodo)

        return nodo

    def eliminar(self, titulo: str):
        self.raiz = self._eliminar(self.raiz, titulo)

    # --- Recorridos ---
    def _inorder(self, nodo):
        if nodo:
            self._inorder(nodo.izq)
            print(nodo.data.titulo)
            self._inorder(nodo.der)

    def mostrar_inorder(self):
        self._inorder(self.raiz)
    
    def inorder(self):
        """Retorna lista de libros ordenados por título (recorrido in-order)."""
        libros = []
        self._recopilar_libros(self.raiz, libros)
        return libros
    

    # --- Exportar DOT ---
    def _exportar_dot_rec(self, nodo, out):
        if not nodo:
            return
        if nodo.izq:
            out.write(f"\"{nodo.data.titulo}\" -> \"{nodo.izq.data.titulo}\" [label=\"L\"];\n")
            self._exportar_dot_rec(nodo.izq, out)
        if nodo.der:
            out.write(f"\"{nodo.data.titulo}\" -> \"{nodo.der.data.titulo}\" [label=\"R\"];\n")
            self._exportar_dot_rec(nodo.der, out)

    def exportar_dot(self, archivo: str):
        with open(archivo, "w", encoding="utf-8") as out:
            out.write("digraph AVL {\n")
            out.write("node [shape=circle, style=filled, fillcolor=lightblue];\n")
            out.write("rankdir=TB;\nordering=out;\n")
            if self.raiz:
                self._exportar_dot_rec(self.raiz, out)
            else:
                out.write("empty [label=\"Arbol Vacio\"];\n")
            out.write("}\n")

    # --- Listar títulos ---
    def _recopilar_libros(self, nodo, libros):
        if nodo:
            self._recopilar_libros(nodo.izq, libros)
            libros.append(nodo.data)
            self._recopilar_libros(nodo.der, libros)

    def listar_titulos(self):
        libros = []
        self._recopilar_libros(self.raiz, libros)
        if not libros:
            print("No hay títulos disponibles.")
            return

        ancho_titulo = max(len("TITULO"), max(len(l.titulo) for l in libros))
        ancho_autor = max(len("AUTOR"), max(len(l.autor) for l in libros))
        ancho_anio = len("AÑO")
        ancho_isbn = max(len("ISBN"), max(len(l.isbn) for l in libros))

        print(f"{'TITULO':<{ancho_titulo}}  {'AUTOR':<{ancho_autor}}  {'AÑO':<{ancho_anio}}  {'ISBN':<{ancho_isbn}}")
        print("=" * (ancho_titulo + ancho_autor + ancho_anio + ancho_isbn + 6))
        for l in libros:
            print(f"{l.titulo:<{ancho_titulo}}  {l.autor:<{ancho_autor}}  {l.anio:<{ancho_anio}}  {l.isbn:<{ancho_isbn}}")
