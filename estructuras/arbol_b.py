from objetos.libro import Libro
from estructuras.lista_libros import ListaLibros

class NodoB:
    def __init__(self, t: int, hoja: bool):
        if t < 2:
            raise ValueError("El grado mínimo del Árbol B debe ser >= 2")
        self.t = t
        self.hoja = hoja
        self.claves = []
        self.valores = []
        self.hijos = []

    def recorrer(self):
        for i in range(len(self.claves)):
            if not self.hoja:
                self.hijos[i].recorrer()
            print(f"{self.valores[i].titulo} ({self.claves[i]})")
        if not self.hoja:
            self.hijos[-1].recorrer()

    def buscar(self, k: int):
        i = 0
        while i < len(self.claves) and k > self.claves[i]:
            i += 1
        if i < len(self.claves) and self.claves[i] == k:
            return self
        if self.hoja:
            return None
        return self.hijos[i].buscar(k)

    def buscar_indice(self, k: int):
        for i, clave in enumerate(self.claves):
            if clave == k:
                return i
        return -1

    def insertar_no_lleno(self, libro: Libro):
        i = len(self.claves) - 1
        if self.hoja:
            # Insertar en hoja
            while i >= 0 and self.claves[i] > libro.anio:
                i -= 1
            self.claves.insert(i + 1, libro.anio)
            self.valores.insert(i + 1, libro)
        else:
            while i >= 0 and self.claves[i] > libro.anio:
                i -= 1
            i += 1
            if len(self.hijos[i].claves) == (2 * self.t - 1):
                self.dividir_hijo(i, self.hijos[i])
                if self.claves[i] < libro.anio:
                    i += 1
            self.hijos[i].insertar_no_lleno(libro)

    def dividir_hijo(self, i: int, y):
        t = self.t
        z = NodoB(t, y.hoja)

        # Copiar la mitad derecha a z
        z.claves = y.claves[t:]
        z.valores = y.valores[t:]
        y.claves = y.claves[:t - 1]
        y.valores = y.valores[:t - 1]

        # Si no es hoja, también mover hijos
        if not y.hoja:
            z.hijos = y.hijos[t:]
            y.hijos = y.hijos[:t]

        # Insertar nuevo hijo en este nodo
        self.hijos.insert(i + 1, z)
        self.claves.insert(i, y.claves.pop())
        self.valores.insert(i, y.valores.pop())

    def buscar_rango(self, inicio, fin, lista: ListaLibros):
        i = 0
        while i < len(self.claves) and self.claves[i] < inicio:
            if not self.hoja:
                self.hijos[i].buscar_rango(inicio, fin, lista)
            i += 1

        while i < len(self.claves) and self.claves[i] <= fin:
            if not self.hoja:
                self.hijos[i].buscar_rango(inicio, fin, lista)
            if inicio <= self.claves[i] <= fin:
                lista.insertar(self.valores[i])
            i += 1

        if not self.hoja and i < len(self.hijos):
            self.hijos[i].buscar_rango(inicio, fin, lista)


class ArbolB:
    def __init__(self, t: int):
        self.raiz = None
        self.t = t

    def insertar(self, libro: Libro):
        if not self.raiz:
            self.raiz = NodoB(self.t, True)
            self.raiz.claves = [libro.anio]
            self.raiz.valores = [libro]
        else:
            if len(self.raiz.claves) == (2 * self.t - 1):
                s = NodoB(self.t, False)
                s.hijos.append(self.raiz)
                s.dividir_hijo(0, self.raiz)
                i = 0
                if s.claves[0] < libro.anio:
                    i += 1
                s.hijos[i].insertar_no_lleno(libro)
                self.raiz = s
            else:
                self.raiz.insertar_no_lleno(libro)

    def recorrer(self):
        if self.raiz:
            self.raiz.recorrer()

    def buscar(self, k: int):
        if not self.raiz:
            return None
        nodo = self.raiz.buscar(k)
        if not nodo:
            return None
        indice = nodo.buscar_indice(k)
        return nodo.valores[indice] if indice >= 0 else None

    def buscar_por_rango_fechas(self, inicio, fin):
        lista = ListaLibros()
        if self.raiz:
            self.raiz.buscar_rango(inicio, fin, lista)
        return lista

    def exportar_dot(self, archivo: str):
        with open(archivo, "w", encoding="utf-8") as out:
            out.write("digraph BTree {\n")
            out.write("node [shape=record, style=filled, fillcolor=lightyellow];\n")
            id_ref = [0]
            self._exportar_dot_rec(self.raiz, out, id_ref)
            out.write("}\n")

    def _exportar_dot_rec(self, nodo, out, id_ref):
        if not nodo:
            return
        nodo_id = id_ref[0]
        id_ref[0] += 1

        label = "|".join(f"<f{i}> {k}" for i, k in enumerate(nodo.claves))
        out.write(f"n{nodo_id} [label=\"{label}\"];\n")

        if not nodo.hoja:
            for i, hijo in enumerate(nodo.hijos):
                child_id = id_ref[0]
                self._exportar_dot_rec(hijo, out, id_ref)
                out.write(f"\"n{nodo_id}\":f{i} -> \"n{child_id}\";\n")

    def listar_anios(self):
        if not self.raiz:
            print("No hay libros registrados.")
            return
        anios_conteo = {}
        self._listar_anios_rec(self.raiz, anios_conteo)
        if not anios_conteo:
            print("No hay años disponibles.")
            return

        print(f"Total de años disponibles: {len(anios_conteo)}")
        print("=" * 30)
        print(f"{'AÑO':<8} CANTIDAD DE LIBROS")
        print("=" * 30)
        for anio, conteo in sorted(anios_conteo.items()):
            print(f"{anio:<8} {conteo} libros")
        print("=" * 30)

    def _listar_anios_rec(self, nodo, conteo):
        if not nodo:
            return
        for i in range(len(nodo.claves)):
            if not nodo.hoja:
                self._listar_anios_rec(nodo.hijos[i], conteo)
            conteo[nodo.claves[i]] = conteo.get(nodo.claves[i], 0) + 1
        if not nodo.hoja:
            self._listar_anios_rec(nodo.hijos[-1], conteo)

    def eliminar(self, anio, isbn):
        if not self.raiz:
            return False
        self._eliminar_rec(self.raiz, anio, isbn)
        return True

    def _eliminar_rec(self, nodo, anio, isbn):
        if not nodo:
            return
        i = 0
        while i < len(nodo.claves):
            if not nodo.hoja:
                self._eliminar_rec(nodo.hijos[i], anio, isbn)
            if nodo.claves[i] == anio and nodo.valores[i].isbn == isbn:
                del nodo.claves[i]
                del nodo.valores[i]
                return
            i += 1
        if not nodo.hoja:
            self._eliminar_rec(nodo.hijos[-1], anio, isbn)

    def buscar_todos(self, k: int):
        resultados = []
        if self.raiz:
            self._buscar_todos_rec(self.raiz, k, resultados)
        return resultados

    def _buscar_todos_rec(self, nodo, k: int, resultados):
        if not nodo:
            return
        for i in range(len(nodo.claves)):
            if not nodo.hoja:
                self._buscar_todos_rec(nodo.hijos[i], k, resultados)
            if nodo.claves[i] == k:
                resultados.append(nodo.valores[i])
        if not nodo.hoja:
            self._buscar_todos_rec(nodo.hijos[-1], k, resultados)