from objetos.libro import Libro

class NodoAVL:
    def __init__(self, libro: Libro):
        self.data = libro
        self.izq: "NodoAVL | None" = None
        self.der: "NodoAVL | None" = None
        self.altura = 1

class ArbolAVL:
    def __init__(self):
        self.raiz: NodoAVL | None = None

    # ---------------- Utilidades internas ----------------
    def _altura(self, nodo: NodoAVL | None) -> int:
        return nodo.altura if nodo else 0

    def _actualizar_altura(self, nodo: NodoAVL) -> None:
        nodo.altura = 1 + max(self._altura(nodo.izq), self._altura(nodo.der))

    def _balance(self, nodo: NodoAVL | None) -> int:
        return self._altura(nodo.izq) - self._altura(nodo.der) if nodo else 0

    def _rotar_derecha(self, y: NodoAVL) -> NodoAVL:
        x = y.izq
        T2 = x.der if x else None
        x.der = y
        y.izq = T2
        self._actualizar_altura(y)
        self._actualizar_altura(x)
        return x

    def _rotar_izquierda(self, x: NodoAVL) -> NodoAVL:
        y = x.der
        T2 = y.izq if y else None
        y.izq = x
        x.der = T2
        self._actualizar_altura(x)
        self._actualizar_altura(y)
        return y

    # ---------------- Inserción ----------------
    def insertar(self, libro: Libro) -> None:
        self.raiz = self._insertar(self.raiz, libro)

    def _insertar(self, nodo: NodoAVL | None, libro: Libro) -> NodoAVL:
        if not nodo:
            return NodoAVL(libro)
        if libro.titulo < nodo.data.titulo:
            nodo.izq = self._insertar(nodo.izq, libro)
        elif libro.titulo > nodo.data.titulo:
            nodo.der = self._insertar(nodo.der, libro)
        else:
            nodo.data = libro
            return nodo

        self._actualizar_altura(nodo)
        balance = self._balance(nodo)

        if balance > 1 and libro.titulo < nodo.izq.data.titulo:
            return self._rotar_derecha(nodo)
        if balance < -1 and libro.titulo > nodo.der.data.titulo:
            return self._rotar_izquierda(nodo)
        if balance > 1 and libro.titulo > nodo.izq.data.titulo:
            nodo.izq = self._rotar_izquierda(nodo.izq)
            return self._rotar_derecha(nodo)
        if balance < -1 and libro.titulo < nodo.der.data.titulo:
            nodo.der = self._rotar_derecha(nodo.der)
            return self._rotar_izquierda(nodo)
        return nodo

    # ---------------- Búsqueda ----------------
    def buscar(self, titulo: str) -> Libro | None:
        actual = self.raiz
        while actual:
            if titulo == actual.data.titulo:
                return actual.data
            actual = actual.izq if titulo < actual.data.titulo else actual.der
        return None

    # ---------------- Eliminación ----------------
    def eliminar(self, titulo: str) -> None:
        self.raiz = self._eliminar(self.raiz, titulo)

    def _eliminar(self, nodo: NodoAVL | None, titulo: str) -> NodoAVL | None:
        if not nodo:
            return None
        if titulo < nodo.data.titulo:
            nodo.izq = self._eliminar(nodo.izq, titulo)
        elif titulo > nodo.data.titulo:
            nodo.der = self._eliminar(nodo.der, titulo)
        else:
            if not nodo.izq or not nodo.der:
                nodo = nodo.izq or nodo.der
            else:
                sucesor = self._minimo(nodo.der)
                nodo.data = sucesor.data
                nodo.der = self._eliminar(nodo.der, sucesor.data.titulo)
        if not nodo:
            return None

        self._actualizar_altura(nodo)
        balance = self._balance(nodo)

        if balance > 1 and self._balance(nodo.izq) >= 0:
            return self._rotar_derecha(nodo)
        if balance > 1 and self._balance(nodo.izq) < 0:
            nodo.izq = self._rotar_izquierda(nodo.izq)
            return self._rotar_derecha(nodo)
        if balance < -1 and self._balance(nodo.der) <= 0:
            return self._rotar_izquierda(nodo)
        if balance < -1 and self._balance(nodo.der) > 0:
            nodo.der = self._rotar_derecha(nodo.der)
            return self._rotar_izquierda(nodo)
        return nodo

    def _minimo(self, nodo: NodoAVL) -> NodoAVL:
        while nodo.izq:
            nodo = nodo.izq
        return nodo

    # ---------------- Recorridos y utilidades existentes ----------------
    def _inorder(self, nodo):
        if nodo:
            self._inorder(nodo.izq)
            print(nodo.data.titulo)
            self._inorder(nodo.der)

    def mostrar_inorder(self):
        self._inorder(self.raiz)

    def inorder(self):
        libros = []
        self._recopilar_libros(self.raiz, libros)
        return libros

    def _recopilar_libros(self, nodo, libros):
        if nodo:
            self._recopilar_libros(nodo.izq, libros)
            libros.append(nodo.data)
            self._recopilar_libros(nodo.der, libros)
            
    def exportar_dot(self, archivo_dot: str) -> None:
        
        with open(archivo_dot, 'w') as f:
            f.write('digraph ArbolAVL {\n')
            f.write('    node [shape=circle, style=filled, fillcolor=lightblue];\n')
            f.write('    edge [color=black];\n')
            
            if self.raiz:
                self._escribir_nodo_dot(f, self.raiz)
            else:
                f.write('    empty [label="Arbol vacio", shape=box, fillcolor=lightgray];\n')
                
            f.write('}\n')

    def _escribir_nodo_dot(self, f, nodo: NodoAVL) -> None:
        
        if not nodo:
            return
            
        label = f"{nodo.data.titulo}\\n(h:{nodo.altura})"
        f.write(f'    "{id(nodo)}" [label="{label}"];\n')
        
        if nodo.izq:
            f.write(f'    "{id(nodo)}" -> "{id(nodo.izq)}" [label="L"];\n')
            self._escribir_nodo_dot(f, nodo.izq)
        
        if nodo.der:
            f.write(f'    "{id(nodo)}" -> "{id(nodo.der)}" [label="R"];\n')
            self._escribir_nodo_dot(f, nodo.der)