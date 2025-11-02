# Logica - backend

**Archivo:** main.py  
**Ruta:** main.py  
**Tamaño:** 216 bytes  

```py
import sys
from gui_app import iniciar_gui

def main():
    try:
        iniciar_gui()
    except Exception as e:
        print(f"Error al iniciar GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

### Carpeta: estructuras

**Archivo:** arbol_avl.py  
**Ruta:** estructuras/arbol_avl.py  
**Tamaño:** 4867 bytes  

```py
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
```

**Archivo:** arbol_b.py  
**Ruta:** estructuras/arbol_b.py  
**Tamaño:** 7275 bytes  

```py
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
```

**Archivo:** arbol_bplus.py  
**Ruta:** estructuras/arbol_bplus.py  
**Tamaño:** 8865 bytes  

```py
from typing import List, Dict, Optional
from objetos.libro import Libro


class NodoBPlus:
    def __init__(self, hoja: bool):
        self.hoja: bool = hoja
        self.claves: List[str] = []
        self.hijos: List['NodoBPlus'] = []
        self.valores: List[List[Libro]] = []
        self.siguiente: Optional['NodoBPlus'] = None


class ArbolBPlus:
    def __init__(self, t: int = 2):
        self.t = max(2, t)
        self.raiz = NodoBPlus(True)

    # -------------------------------------------------
    # Inserción
    # -------------------------------------------------
    def insertar(self, libro: Libro):
        if len(self.raiz.claves) == 2 * self.t - 1:
            nueva_raiz = NodoBPlus(False)
            nueva_raiz.hijos.append(self.raiz)
            self._dividir_nodo(nueva_raiz, 0, self.raiz)
            self.raiz = nueva_raiz
        self._insertar_interno(self.raiz, libro, libro.genero)

    def _insertar_interno(self, nodo: NodoBPlus, libro: Libro, genero: str):
        if nodo.hoja:
            # Verificar si el género ya existe
            for i, clave in enumerate(nodo.claves):
                if clave == genero:
                    # Evitar duplicados exactos (ISBN)
                    if not any(l.isbn == libro.isbn for l in nodo.valores[i]):
                        nodo.valores[i].append(libro)
                    return

            # Si el género no existe, insertarlo
            nodo.claves.append(genero)
            nodo.valores.append([libro])

            # Ordenar por clave
            for i in range(len(nodo.claves) - 1, 0, -1):
                if nodo.claves[i] < nodo.claves[i - 1]:
                    nodo.claves[i], nodo.claves[i - 1] = nodo.claves[i - 1], nodo.claves[i]
                    nodo.valores[i], nodo.valores[i - 1] = nodo.valores[i - 1], nodo.valores[i]
        else:
            i = 0
            while i < len(nodo.claves) and genero > nodo.claves[i]:
                i += 1
            self._insertar_interno(nodo.hijos[i], libro, genero)

            # Dividir si está lleno
            if len(nodo.hijos[i].claves) >= 2 * self.t:
                self._dividir_nodo(nodo, i, nodo.hijos[i])

    def _dividir_nodo(self, padre: NodoBPlus, i: int, hijo: NodoBPlus):
        nuevo = NodoBPlus(hijo.hoja)
        mitad = self.t

        if hijo.hoja:
            nuevo.claves = hijo.claves[mitad:]
            nuevo.valores = hijo.valores[mitad:]
            hijo.claves = hijo.claves[:mitad]
            hijo.valores = hijo.valores[:mitad]

            nuevo.siguiente = hijo.siguiente
            hijo.siguiente = nuevo

            padre.claves.insert(i, nuevo.claves[0])
            padre.hijos.insert(i + 1, nuevo)
        else:
            nuevo.claves = hijo.claves[mitad + 1:]
            nuevo.hijos = hijo.hijos[mitad + 1:]
            clave_promocion = hijo.claves[mitad]

            hijo.claves = hijo.claves[:mitad]
            hijo.hijos = hijo.hijos[:mitad + 1]

            padre.claves.insert(i, clave_promocion)
            padre.hijos.insert(i + 1, nuevo)

    # -------------------------------------------------
    # Búsqueda
    # -------------------------------------------------
    def buscar(self, genero: str) -> List[Libro]:
        resultado: List[Libro] = []
        if not self.raiz:
            return resultado

        actual = self.raiz
        while not actual.hoja:
            i = 0
            while i < len(actual.claves) and genero > actual.claves[i]:
                i += 1
            actual = actual.hijos[i]

        while actual:
            for i, clave in enumerate(actual.claves):
                if clave == genero:
                    resultado.extend(actual.valores[i])
            actual = actual.siguiente

        return resultado

    # -------------------------------------------------
    # Eliminación
    # -------------------------------------------------
    def eliminar(self, genero: str, isbn: str) -> bool:
        if not self.raiz:
            return False

        actual = self.raiz
        while not actual.hoja:
            actual = actual.hijos[0]

        while actual:
            for i, clave in enumerate(actual.claves):
                if clave == genero:
                    for j, l in enumerate(actual.valores[i]):
                        if l.isbn == isbn:
                            del actual.valores[i][j]
                            if not actual.valores[i]:
                                del actual.valores[i]
                                del actual.claves[i]
                            return True
            actual = actual.siguiente
        return False

    # -------------------------------------------------
    # Mostrar
    # -------------------------------------------------
    def mostrar_todos(self):
        if not self.raiz:
            print("No hay libros registrados por género.")
            return

        actual = self.raiz
        while not actual.hoja:
            actual = actual.hijos[0]

        while actual:
            for i, genero in enumerate(actual.claves):
                libros = actual.valores[i]
                if not libros:
                    continue

                print(f"\nGénero: {genero} ({len(libros)} libros)")
                print("=" * 80)
                print(f"{'TITULO':<30}{'AUTOR':<25}{'AÑO':<8}{'ISBN'}")
                print("=" * 80)

                for l in libros:
                    print(f"{l.titulo:<30}{l.autor:<25}{l.anio:<8}{l.isbn}")

                print("=" * 80)
            actual = actual.siguiente

    # -------------------------------------------------
    # Listar géneros
    # -------------------------------------------------
    def listar_generos(self):
        if not self.raiz:
            print("No hay géneros disponibles.")
            return

        generos_consolidados: Dict[str, int] = {}

        actual = self.raiz
        while not actual.hoja:
            actual = actual.hijos[0]

        while actual:
            for i, clave in enumerate(actual.claves):
                generos_consolidados[clave] = generos_consolidados.get(clave, 0) + len(actual.valores[i])
            actual = actual.siguiente

        if not generos_consolidados:
            print("No hay géneros disponibles.")
            return

        print("\nGéneros disponibles:")
        print("=" * 40)
        print(f"{'GÉNERO':<25}{'CANTIDAD'}")
        print("=" * 40)
        for genero, cantidad in generos_consolidados.items():
            print(f"{genero:<25}{cantidad} libros")
        print("=" * 40)

    # -------------------------------------------------
    # Exportar a DOT
    # -------------------------------------------------
    def exportar_dot(self, archivo: str):
        with open(archivo, "w", encoding="utf-8") as out:
            out.write("digraph BPlusTree {\n")
            out.write("node [shape=record, style=filled, fillcolor=lightblue];\nrankdir=TB;\n")

            if not self.raiz:
                out.write("vacio [label=\"Árbol vacío\"];\n")
            else:
                id_counter = [0]
                self._exportar_dot_rec(self.raiz, out, id_counter)

            out.write("}\n")

        print(f"Archivo DOT generado: {archivo}")

    def _exportar_dot_rec(self, nodo: NodoBPlus, out, id_counter):
        if not nodo:
            return
        nodo_id = id_counter[0]
        id_counter[0] += 1

        label_parts = []
        if nodo.hoja:
            for i, clave in enumerate(nodo.claves):
                label_parts.append(f"<f{i}> {clave} ({len(nodo.valores[i])})")
        else:
            for i, clave in enumerate(nodo.claves):
                label_parts.append(f"<f{i}> |{clave}| ")
            label_parts.append(f"<f{len(nodo.claves)}>")

        fillcolor = "palegreen" if nodo.hoja else "lightskyblue"
        out.write(f"n{nodo_id} [label=\"{'|'.join(label_parts)}\", fillcolor={fillcolor}];\n")

        if not nodo.hoja:
            for i, hijo in enumerate(nodo.hijos):
                child_id = id_counter[0]
                self._exportar_dot_rec(hijo, out, id_counter)
                out.write(f"\"n{nodo_id}\":f{i} -> \"n{child_id}\";\n")
        # -------------------------------------------------
    # Obtener géneros únicos (para GUI)
    # -------------------------------------------------
    def obtener_generos(self) -> List[str]:
        """Retorna lista de géneros únicos ordenados alfabéticamente."""
        if not self.raiz:
            return []

        generos = set()
        actual = self.raiz

        # Ir a la primera hoja
        while not actual.hoja:
            actual = actual.hijos[0]

        # Recorrer todas las hojas
        while actual:
            generos.update(actual.claves)
            actual = actual.siguiente

        return sorted(list(generos))
```

**Archivo:** cola.py  
**Ruta:** estructuras/cola.py  
**Tamaño:** 2439 bytes  

```py
from objetos.libro import Libro
from typing import Optional

class NodoCola:
    def __init__(self, libro: Libro):
        self.libro = libro
        self.siguiente: Optional['NodoCola'] = None

class Cola:
    def __init__(self, tipo="general"):
        self.frente: Optional[NodoCola] = None
        self.final: Optional[NodoCola] = None
        self.tamanio = 0
        self.tipo = tipo  # "ingreso", "traspaso", "salida"

    def encolar(self, libro: Libro):
        nuevo = NodoCola(libro)
        if not self.final:
            self.frente = self.final = nuevo
        else:
            self.final.siguiente = nuevo
            self.final = nuevo
        self.tamanio += 1

    def desencolar(self) -> Optional[Libro]:
        if not self.frente:
            return None
        libro = self.frente.libro
        self.frente = self.frente.siguiente
        if not self.frente:
            self.final = None
        self.tamanio -= 1
        return libro

    def esta_vacia(self) -> bool:
        return self.frente is None

    def ver_frente(self) -> Optional[Libro]:
        return self.frente.libro if self.frente else None

    def listar(self):
        if self.esta_vacia():
            print(f"Cola de {self.tipo} vacia")
            return
        actual = self.frente
        print(f"\nCola de {self.tipo} ({self.tamanio} elementos):")
        print("=" * 80)
        while actual:
            print(f"-> {actual.libro.titulo} ({actual.libro.isbn}) - Estado: {actual.libro.estado}")
            actual = actual.siguiente
        print("=" * 80)

    def exportar_dot(self, archivo: str):
        with open(archivo, "w", encoding="utf-8") as out:
            out.write(f"digraph Cola_{self.tipo} {{\n")
            out.write("    rankdir=LR;\n")
            out.write("    node [shape=box];\n\n")

            if self.esta_vacia():
                out.write("    vacio [label=\"Cola vacia\"];\n")
            else:
                actual = self.frente
                contador = 0
                while actual:
                    out.write(f'    n{contador} [label="{actual.libro.titulo}\\n{actual.libro.isbn}"];\n')
                    if actual.siguiente:
                        out.write(f"    n{contador} -> n{contador+1};\n")
                    actual = actual.siguiente
                    contador += 1

            out.write("}\n")
        print(f"Cola de {self.tipo} exportada: {archivo}")
```

**Archivo:** grafo.py  
**Ruta:** estructuras/grafo.py  
**Tamaño:** 14552 bytes  

```py
from typing import Dict, List, Tuple, Optional
import math

class Arista:
    def __init__(self, destino: str, tiempo: int, costo: float):
        self.destino = destino
        self.tiempo = tiempo
        self.costo = costo

class Grafo:
    def __init__(self):
        self.nodos: Dict[str, List[Arista]] = {}
        self.etiquetas: Dict[str, str] = {} # Inicialización de etiquetas

    def agregar_nodo(self, nombre: str, etiqueta: str = None):
        """
        Agrega un nodo al grafo.
        nombre: ID único del nodo
        etiqueta: Nombre legible para visualización (opcional)
        """
        if nombre not in self.nodos:
            self.nodos[nombre] = []
        if etiqueta:
            self.etiquetas[nombre] = etiqueta # Almacenar etiqueta

    def agregar_arista(self, origen: str, destino: str, tiempo: int, costo: float, bidireccional: bool = True):
        self.agregar_nodo(origen)
        self.agregar_nodo(destino)
        self.nodos[origen].append(Arista(destino, tiempo, costo))
        if bidireccional:
            self.nodos[destino].append(Arista(origen, tiempo, costo))

    def eliminar_nodo(self, nombre: str) -> bool:
        """
        Elimina un nodo y todas sus aristas asociadas.
        Retorna True si fue eliminado, False si no existia.
        """
        if nombre not in self.nodos:
            return False

        del self.nodos[nombre]

        # Eliminar etiqueta si existe
        if nombre in self.etiquetas:
            del self.etiquetas[nombre]

        for nodo_origen in self.nodos:
            self.nodos[nodo_origen] = [
                arista for arista in self.nodos[nodo_origen]
                if arista.destino != nombre
            ]

        return True

    def eliminar_arista(self, origen: str, destino: str, bidireccional: bool = True) -> bool:
        """
        Elimina una arista entre dos nodos.
        Retorna True si fue eliminada, False si no existia.
        """
        if origen not in self.nodos:
            return False

        aristas_origen = self.nodos[origen]
        cantidad_inicial = len(aristas_origen)
        self.nodos[origen] = [a for a in aristas_origen if a.destino != destino]

        if bidireccional and destino in self.nodos:
            aristas_destino = self.nodos[destino]
            self.nodos[destino] = [a for a in aristas_destino if a.destino != origen]

        # Se asume que el grafo es dirigido en el almacenamiento, por lo que basta con revisar el origen.
        return len(self.nodos[origen]) < cantidad_inicial

    def dijkstra_tiempo(self, origen: str, destino: str) -> Tuple[int, List[str]]:
        # La distancia es float, se convierte a int al final si la ruta es válida
        distancia, ruta = self._dijkstra(origen, destino, usar_tiempo=True)
        return (int(distancia), ruta) if ruta else (math.inf, [])

    def dijkstra_costo(self, origen: str, destino: str) -> Tuple[float, List[str]]:
        return self._dijkstra(origen, destino, usar_tiempo=False)

    def _dijkstra(self, origen: str, destino: str, usar_tiempo: bool) -> Tuple[float, List[str]]:
        if origen not in self.nodos or destino not in self.nodos:
            return (math.inf, [])

        distancias: Dict[str, float] = {nodo: math.inf for nodo in self.nodos}
        previos: Dict[str, Optional[str]] = {nodo: None for nodo in self.nodos}
        distancias[origen] = 0.0
        visitados = set()

        while len(visitados) < len(self.nodos):
            nodo_actual = None
            distancia_minima = math.inf

            # Encontrar el nodo no visitado con la menor distancia
            for nodo in self.nodos:
                if nodo not in visitados and distancias[nodo] < distancia_minima:
                    distancia_minima = distancias[nodo]
                    nodo_actual = nodo

            if nodo_actual is None or nodo_actual == destino:
                break

            visitados.add(nodo_actual)

            # Relajación de aristas
            for arista in self.nodos[nodo_actual]:
                peso = arista.tiempo if usar_tiempo else arista.costo
                distancia = distancias[nodo_actual] + peso

                if distancia < distancias[arista.destino]:
                    distancias[arista.destino] = distancia
                    previos[arista.destino] = nodo_actual

        # Reconstruir el camino
        camino: List[str] = []
        nodo = destino
        while nodo is not None:
            camino.insert(0, nodo)
            nodo = previos[nodo]

        if not camino or camino[0] != origen:
            return (math.inf, [])

        return (distancias[destino], camino)

    def obtener_rutas_alternativas(self, origen: str, destino: str, criterio: str = "tiempo") -> List[Tuple[float, List[str]]]:
        """
        Retorna hasta 3 rutas alternativas ordenadas por costo/tiempo.
        Usa variante de Dijkstra con k caminos mas cortos.
        """
        usar_tiempo = (criterio == "tiempo")
        rutas = []

        rutas_prohibidas: set[Tuple[str, ...]] = set()

        for _ in range(3):
            distancia, camino = self._dijkstra_con_prohibiciones(
                origen, destino, usar_tiempo, rutas_prohibidas
            )

            if distancia == math.inf or not camino:
                break

            rutas.append((distancia, camino))
            rutas_prohibidas.add(tuple(camino))

        return rutas

    def _dijkstra_con_prohibiciones(self, origen: str, destino: str, usar_tiempo: bool, 
                                     rutas_prohibidas: set[Tuple[str, ...]]) -> Tuple[float, List[str]]:
        """
        Dijkstra modificado que evita rutas ya encontradas.
        """
        if origen not in self.nodos or destino not in self.nodos:
            return (math.inf, [])

        distancias: Dict[str, float] = {nodo: math.inf for nodo in self.nodos}
        previos: Dict[str, Optional[str]] = {nodo: None for nodo in self.nodos}
        distancias[origen] = 0.0
        visitados = set()

        while len(visitados) < len(self.nodos):
            nodo_actual = None
            distancia_minima = math.inf

            for nodo in self.nodos:
                if nodo not in visitados and distancias[nodo] < distancia_minima:
                    distancia_minima = distancias[nodo]
                    nodo_actual = nodo

            if nodo_actual is None:
                break

            # Si el nodo actual es el destino, verificamos si el camino es una ruta prohibida
            if nodo_actual == destino:
                camino_temporal = []
                nodo = destino
                while nodo is not None:
                    camino_temporal.insert(0, nodo)
                    nodo = previos[nodo]

                if tuple(camino_temporal) in rutas_prohibidas:
                    visitados.add(nodo_actual) # Marcar como visitado y seguir buscando
                    continue

            visitados.add(nodo_actual)

            for arista in self.nodos[nodo_actual]:
                peso = arista.tiempo if usar_tiempo else arista.costo
                distancia = distancias[nodo_actual] + peso

                if distancia < distancias[arista.destino]:
                    distancias[arista.destino] = distancia
                    previos[arista.destino] = nodo_actual

        camino: List[str] = []
        nodo = destino
        while nodo is not None:
            camino.insert(0, nodo)
            nodo = previos[nodo]

        if not camino or camino[0] != origen:
            return (math.inf, [])

        # Última verificación para asegurar que el camino encontrado no sea una ruta prohibida
        if tuple(camino) in rutas_prohibidas:
             return (math.inf, [])

        return (distancias[destino], camino)

    def obtener_pesos_arista(self, origen: str, destino: str) -> Optional[Tuple[int, float]]:
        """Devuelve (tiempo, costo) si existe la arista origen→destino."""
        if origen not in self.nodos:
            return None
        for arista in self.nodos[origen]:
            if arista.destino == destino:
                return arista.tiempo, arista.costo
        return None

    def calcular_tiempo_ruta(self, ruta: List[str]) -> float:
        """Suma tiempos en segundos para la ruta dada."""
        if not ruta or len(ruta) < 2:
            return 0.0
        total = 0.0
        for i in range(len(ruta) - 1):
            pesos = self.obtener_pesos_arista(ruta[i], ruta[i + 1])
            if not pesos:
                return math.inf
            total += pesos[0]
        return total

    def calcular_costo_ruta(self, ruta: List[str]) -> float:
        """Suma costos monetarios para la ruta dada."""
        if not ruta or len(ruta) < 2:
            return 0.0
        total = 0.0
        for i in range(len(ruta) - 1):
            pesos = self.obtener_pesos_arista(ruta[i], ruta[i + 1])
            if not pesos:
                return math.inf
            total += pesos[1]
        return total

    def calcular_eta(self, origen: str, destino: str, prioridad: str = "tiempo") -> int:
        """
        Calcula tiempo estimado de llegada (ETA) en segundos.
        """
        if prioridad == "tiempo":
            tiempo_total, ruta = self.dijkstra_tiempo(origen, destino)
            # dijkstra_tiempo ya retorna el tiempo total como int si es posible
            return int(tiempo_total) if ruta and tiempo_total != math.inf else 0
        else:
            costo_total, ruta = self.dijkstra_costo(origen, destino)
            if not ruta or costo_total == math.inf:
                return 0
            tiempo_total = self.calcular_tiempo_ruta(ruta)
            return int(tiempo_total) if tiempo_total != math.inf else 0

    def listar_nodos(self) -> List[str]:
        """Retorna lista de IDs de nodos (bibliotecas)"""
        return list(self.nodos.keys())

    def obtener_aristas(self, nodo: str) -> List[Arista]:
        """Retorna lista de aristas salientes de un nodo"""
        return self.nodos.get(nodo, [])

    def existe_nodo(self, nombre: str) -> bool:
        """Verifica si existe un nodo en el grafo"""
        return nombre in self.nodos

    def obtener_grado_entrada(self, nodo: str) -> int:
        """Calcula el grado de entrada de un nodo (cuantas aristas llegan a el)"""
        if nodo not in self.nodos:
            return 0

        grado = 0
        for origen in self.nodos:
            for arista in self.nodos[origen]:
                if arista.destino == nodo:
                    grado += 1
        return grado

    def obtener_grado_salida(self, nodo: str) -> int:
        """Calcula el grado de salida de un nodo (cuantas aristas salen de el)"""
        return len(self.nodos.get(nodo, []))

    def obtener_estadisticas(self) -> dict:
        """
        Retorna estadisticas del grafo:
        - Numero de nodos
        - Numero de aristas
        - Nodo con mas conexiones
        - Tiempo promedio de aristas
        - Costo promedio de aristas
        """
        total_nodos = len(self.nodos)
        total_aristas = sum(len(aristas) for aristas in self.nodos.values())

        if total_nodos == 0:
            return {
                "nodos": 0,
                "aristas": 0,
                "nodo_mas_conectado": None,
                "tiempo_promedio": 0,
                "costo_promedio": 0
            }

        max_conexiones = -1
        nodo_mas_conectado = None

        suma_tiempos = 0
        suma_costos = 0

        for nodo, aristas in self.nodos.items():
            conexiones = len(aristas)
            # Solo consideramos las aristas salientes para 'max_conexiones'
            if conexiones > max_conexiones:
                max_conexiones = conexiones
                nodo_mas_conectado = nodo

            for arista in aristas:
                suma_tiempos += arista.tiempo
                suma_costos += arista.costo

        return {
            "nodos": total_nodos,
            "aristas": total_aristas,
            "nodo_mas_conectado": nodo_mas_conectado,
            "max_conexiones": max_conexiones if max_conexiones > -1 else 0,
            "tiempo_promedio": suma_tiempos / total_aristas if total_aristas > 0 else 0,
            "costo_promedio": suma_costos / total_aristas if total_aristas > 0 else 0
        }

    def mostrar_estadisticas(self):
        """Imprime estadisticas del grafo en formato tabular"""
        stats = self.obtener_estadisticas()

        print("\n" + "=" * 60)
        print("ESTADISTICAS DEL GRAFO DE RED DE BIBLIOTECAS")
        print("=" * 60)
        print(f"Total de nodos (bibliotecas):     {stats['nodos']}")
        print(f"Total de conexiones (aristas):    {stats['aristas']}")
        print(f"Nodo mas conectado:               {stats['nodo_mas_conectado']}")
        print(f"Numero de conexiones:             {stats['max_conexiones']}")
        print(f"Tiempo promedio de traslado:      {stats['tiempo_promedio']:.2f} segundos")
        print(f"Costo promedio de traslado:       {stats['costo_promedio']:.2f} unidades")
        print("=" * 60)

    def exportar_dot(self, archivo: str):
        """
        Exporta el grafo a formato DOT para visualizacion con Graphviz.
        Aplica los estilos mejorados de la revisión.
        """
        with open(archivo, "w", encoding="utf-8") as out:
            out.write("digraph RedBibliotecas {\n    rankdir=LR;\n")
            out.write("    node [shape=ellipse, style=filled, fillcolor=\"#cfe2ff\"];\n")
            out.write("    edge [color=\"#4a90e2\", fontcolor=\"#1f3d7a\", fontsize=10];\n\n")

            # Escribir nodos con etiquetas
            for nodo in self.nodos:
                etiqueta = self.etiquetas.get(nodo, nodo)
                out.write(f'    "{nodo}" [label="{etiqueta}\\n({nodo})"];\n')

            out.write("\n")

            # Escribir aristas (solo dirigidas, sin lógica bidireccional compleja)
            for origen, aristas in self.nodos.items():
                for arista in aristas:
                    out.write(
                        f'    "{origen}" -> "{arista.destino}" '
                        f'[label="t={arista.tiempo}s\\nc={arista.costo:.2f}"];\n'
                    )

            out.write("}\n")

        print(f"Grafo exportado: {archivo}")
```

**Archivo:** lista_libros.py  
**Ruta:** estructuras/lista_libros.py  
**Tamaño:** 3824 bytes  

```py
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
        Muestra todos los libros en formato tabular y RETORNA la lista.
        """
        if not self.cabeza:
            print("No hay libros en el catálogo.")
            return []  # ✅ RETORNAR LISTA VACÍA EN LUGAR DE None

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
```

**Archivo:** metodos_ordenamiento.py  
**Ruta:** estructuras/metodos_ordenamiento.py  
**Tamaño:** 3447 bytes  

```py
from typing import List, Tuple
from objetos.libro import Libro
import time

def medir_tiempo(func, libros: List[Libro], clave: str) -> Tuple[List[Libro], float]:
    """Mide el tiempo de ejecucion de una funcion de ordenamiento."""
    inicio = time.perf_counter()
    resultado = func(libros.copy(), clave)
    fin = time.perf_counter()
    return resultado, fin - inicio

def burbuja(libros: List[Libro], clave="titulo") -> List[Libro]:
    """Algoritmo de ordenamiento Burbuja."""
    n = len(libros)
    for i in range(n):
        for j in range(0, n - i - 1):
            if getattr(libros[j], clave) > getattr(libros[j + 1], clave):
                libros[j], libros[j + 1] = libros[j + 1], libros[j]
    return libros

def seleccion(libros: List[Libro], clave="titulo") -> List[Libro]:
    """Algoritmo de ordenamiento por Seleccion."""
    n = len(libros)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if getattr(libros[j], clave) < getattr(libros[min_idx], clave):
                min_idx = j
        libros[i], libros[min_idx] = libros[min_idx], libros[i]
    return libros

def insercion(libros: List[Libro], clave="titulo") -> List[Libro]:
    """Algoritmo de ordenamiento por Insercion."""
    for i in range(1, len(libros)):
        key = libros[i]
        j = i - 1
        while j >= 0 and getattr(libros[j], clave) > getattr(key, clave):
            libros[j + 1] = libros[j]
            j -= 1
        libros[j + 1] = key
    return libros

def shell_sort(libros: List[Libro], clave="titulo") -> List[Libro]:
    """Algoritmo de ordenamiento Shell Sort."""
    n = len(libros)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = libros[i]
            j = i
            while j >= gap and getattr(libros[j - gap], clave) > getattr(temp, clave):
                libros[j] = libros[j - gap]
                j -= gap
            libros[j] = temp
        gap //= 2
    return libros

def quick_sort(libros: List[Libro], clave="titulo") -> List[Libro]:
    """Algoritmo de ordenamiento QuickSort."""
    if len(libros) <= 1:
        return libros
    # Elegir el pivote
    pivote = libros[len(libros) // 2]

    # Particionar la lista
    izq = [x for x in libros if getattr(x, clave) < getattr(pivote, clave)]
    centro = [x for x in libros if getattr(x, clave) == getattr(pivote, clave)]
    der = [x for x in libros if getattr(x, clave) > getattr(pivote, clave)]

    # Llamada recursiva
    return quick_sort(izq, clave) + centro + quick_sort(der, clave)

def comparar_metodos(libros: List[Libro], clave="titulo") -> str:
    """
    Compara el tiempo de ejecucion de varios metodos de ordenamiento 
    y retorna el reporte en formato string.
    """
    metodos = {
        "Burbuja": burbuja,
        "Seleccion": seleccion,
        "Insercion": insercion,
        "Shell Sort": shell_sort,
        "QuickSort": quick_sort
    }

    lineas = []
    lineas.append(f"\nComparacion de metodos de ordenamiento por **{clave}**")
    lineas.append("=" * 60)
    lineas.append(f"{'METODO':<20}{'TIEMPO (segundos)':<25}{'ELEMENTOS'}")
    lineas.append("=" * 60)

    for nombre, metodo in metodos.items():
        _, tiempo = medir_tiempo(metodo, libros, clave)
        lineas.append(f"{nombre:<20}{tiempo:<25.6f}{len(libros)}")

    lineas.append("=" * 60)

    reporte = "\n".join(lineas)
    print(reporte) 
    return reporte 
```

**Archivo:** pila.py  
**Ruta:** estructuras/pila.py  
**Tamaño:** 1276 bytes  

```py
from objetos.libro import Libro
from typing import Optional

class NodoPila:
    def __init__(self, libro: Libro):
        self.libro = libro
        self.siguiente: Optional["NodoPila"] = None

class Pila:
    def __init__(self):
        self.tope: Optional[NodoPila] = None
        self.tamanio = 0

    def apilar(self, libro: Libro):
        nuevo = NodoPila(libro)
        nuevo.siguiente = self.tope
        self.tope = nuevo
        self.tamanio += 1

    def desapilar(self) -> Optional[Libro]:
        if not self.tope:
            return None
        libro = self.tope.libro
        self.tope = self.tope.siguiente
        self.tamanio -= 1
        return libro

    def push(self, libro: Libro):
        """Alias de apilar para compatibilidad."""
        self.apilar(libro)

    def pop(self) -> Optional[Libro]:
        """Alias de desapilar para compatibilidad."""
        return self.desapilar()

    def esta_vacia(self) -> bool:
        return self.tope is None

    def ver_tope(self) -> Optional[Libro]:
        return self.tope.libro if self.tope else None

    def listar(self):
        elementos = []
        actual = self.tope
        while actual:
            elementos.append(actual.libro)
            actual = actual.siguiente
        return elementos
```

**Archivo:** tabla_hash.py  
**Ruta:** estructuras/tabla_hash.py  
**Tamaño:** 8691 bytes  

```py
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
```

---

### Carpeta: objetos

**Archivo:** biblioteca.py  
**Ruta:** objetos/biblioteca.py  
**Tamaño:** 10859 bytes  

```py
from objetos.controlador_catalogo import ControladorCatalogo
from objetos.libro import Libro
from objetos.inventario import Inventario
from estructuras.cola import Cola
from estructuras.pila import Pila
from estructuras.metodos_ordenamiento import comparar_metodos
from typing import Optional, List
import time


class Biblioteca:
    """
    Representa un nodo del grafo (biblioteca individual).
    Cada biblioteca tiene su propio catalogo y 3 colas de procesamiento.
    """

    def __init__(self, id_biblioteca: str, nombre: str, ubicacion: str, 
                 tiempo_ingreso: int = 10, tiempo_traspaso: int = 5, intervalo_despacho: int = 3,
                 inventario: Optional[Inventario] = None):
        self.id = id_biblioteca
        self.nombre = nombre
        self.ubicacion = ubicacion

        self.tiempo_ingreso = tiempo_ingreso
        self.tiempo_traspaso = tiempo_traspaso
        self.intervalo_despacho = intervalo_despacho

        self.cola_ingreso = Cola(tipo="ingreso")
        self.cola_traspaso = Cola(tipo="traspaso")
        self.cola_salida = Cola(tipo="salida")

        self.catalogo_local = ControladorCatalogo()
        self.inventario = inventario

        self.pila_rollback = Pila()

        self.ultimo_despacho = time.time()

        self.estadisticas = {
            "libros_ingresados": 0,
            "libros_enviados": 0,
            "libros_recibidos": 0,
            "tiempo_total_procesamiento": 0.0
        }

    def set_inventario(self, inventario: Inventario) -> None:
        self.inventario = inventario

    def _actualizar_inventario(self, libro: Libro, delta: int) -> None:
        if not self.inventario:
            return
        genero = libro.genero if libro.genero else "SinGenero"
        if delta > 0:
            self.inventario.incrementar(self.id, genero, delta)
        elif delta < 0:
            self.inventario.decrementar(self.id, genero, abs(delta))

    def agregar_libro_catalogo(self, libro: Libro, registrar_rollback: bool = True, contar_ingreso: bool = True) -> None:
        libro.biblioteca_origen = libro.biblioteca_origen or self.id
        if not libro.biblioteca_destino:
            libro.biblioteca_destino = self.id
        libro.cambiar_estado("disponible")
        self.catalogo_local.agregar_libro(libro)
        self._actualizar_inventario(libro, 1)
        if registrar_rollback:
            self.pila_rollback.apilar(libro)
        if contar_ingreso:
            self.estadisticas["libros_ingresados"] += 1

    def agregar_libro_ingreso(self, libro: Libro) -> None:
        """Agrega un libro a la cola de ingreso."""
        libro.cambiar_estado("en_transito")
        self.cola_ingreso.encolar(libro)
        print(f"Libro '{libro.titulo}' agregado a cola de ingreso de {self.nombre}")

    def procesar_ingreso(self) -> bool:
        """
        Procesa un libro de la cola de ingreso.
        Decide si va al catalogo local o a la cola de traspaso.
        Retorna True si proceso algo, False si la cola estaba vacia.
        """
        if self.cola_ingreso.esta_vacia():
            return False

        inicio = time.perf_counter()
        libro = self.cola_ingreso.desencolar()

        if libro.biblioteca_destino == self.id or not libro.biblioteca_destino:
            self.agregar_libro_catalogo(libro)
            print(f"Libro '{libro.titulo}' agregado al catalogo de {self.nombre}")
        else:
            libro.cambiar_estado("en_transito")
            self.cola_traspaso.encolar(libro)
            print(f"Libro '{libro.titulo}' movido a cola de traspaso en {self.nombre}")

        fin = time.perf_counter()
        self.estadisticas["tiempo_total_procesamiento"] += fin - inicio
        return True

    def procesar_traspaso(self) -> bool:
        """
        Prepara un libro para ser enviado (cola traspaso -> cola salida).
        Retorna True si proceso algo, False si la cola estaba vacia.
        """
        if self.cola_traspaso.esta_vacia():
            return False

        inicio = time.perf_counter()
        libro = self.cola_traspaso.desencolar()
        self.cola_salida.encolar(libro)
        fin = time.perf_counter()
        self.estadisticas["tiempo_total_procesamiento"] += fin - inicio

        print(f"Libro '{libro.titulo}' preparado para envio desde {self.nombre}")

        return True

    def procesar_salida(self) -> Optional[Libro]:
        """
        Despacha un libro si ha pasado el intervalo de despacho.
        Retorna el libro despachado o None si no se puede despachar.
        """
        tiempo_actual = time.time()

        if (tiempo_actual - self.ultimo_despacho) < self.intervalo_despacho:
            return None

        if self.cola_salida.esta_vacia():
            return None

        inicio = time.perf_counter()
        libro = self.cola_salida.desencolar()
        libro.cambiar_estado("en_transito")
        self.ultimo_despacho = tiempo_actual
        self.estadisticas["libros_enviados"] += 1
        fin = time.perf_counter()
        self.estadisticas["tiempo_total_procesamiento"] += fin - inicio

        print(f"Libro '{libro.titulo}' despachado desde {self.nombre}")
        return libro

    def registrar_recepcion(self, libro: Libro) -> None:
        """
        Registra la llegada de un libro proveniente de otra biblioteca.
        """
        libro.biblioteca_destino = self.id
        self.agregar_libro_catalogo(libro, registrar_rollback=True, contar_ingreso=False)
        self.estadisticas["libros_recibidos"] += 1
        print(f"Libro '{libro.titulo}' recibido en {self.nombre}")

    def obtener_libro_por_isbn(self, isbn: str) -> Optional[Libro]:
        """Busca un libro en el catalogo local por ISBN."""
        return self.catalogo_local.buscar_por_isbn(isbn)

    def eliminar_libro_catalogo(self, isbn: str) -> bool:
        """Elimina un libro del catalogo local."""
        libro = self.obtener_libro_por_isbn(isbn)
        if libro:
            self.catalogo_local.eliminar_libro(isbn)
            self._actualizar_inventario(libro, -1)
            return True
        return False

    def rollback_ultimo_ingreso(self) -> Optional[Libro]:
        """Deshace el ultimo libro ingresado al catalogo."""
        if self.pila_rollback.esta_vacia():
            print("No hay operaciones para deshacer")
            return None

        libro = self.pila_rollback.desapilar()
        self.catalogo_local.eliminar_libro(libro.isbn)
        self._actualizar_inventario(libro, -1)
        print(f"Se deshizo el ingreso de '{libro.titulo}'")
        return libro

    def ordenar_catalogo(self, metodo: str = "quick_sort", clave: str = "titulo") -> None:
        """
        Ordena el catalogo local usando uno de los 5 metodos.
        metodo: "burbuja", "seleccion", "insercion", "shell_sort", "quick_sort"
        """
        from estructuras.metodos_ordenamiento import burbuja, seleccion, insercion, shell_sort, quick_sort

        metodos = {
            "burbuja": burbuja,
            "seleccion": seleccion,
            "insercion": insercion,
            "shell_sort": shell_sort,
            "quick_sort": quick_sort
        }

        if metodo not in metodos:
            print(f"Metodo invalido: {metodo}")
            return

        libros_lista = []
        actual = self.catalogo_local.lista_secuencial.cabeza
        while actual:
            libros_lista.append(actual.data)
            actual = actual.siguiente

        libros_ordenados = metodos[metodo](libros_lista, clave)

        print(f"Catalogo de {self.nombre} ordenado por {clave} usando {metodo}")
        for libro in libros_ordenados:
            print(f"  - {getattr(libro, clave)}: {libro.titulo}")

    def comparar_metodos_ordenamiento(self, clave: str = "titulo") -> None:
        """Compara los 5 metodos de ordenamiento en el catalogo local."""
        libros_lista = []
        actual = self.catalogo_local.lista_secuencial.cabeza
        while actual:
            libros_lista.append(actual.data)
            actual = actual.siguiente

        if not libros_lista:
            print(f"El catalogo de {self.nombre} esta vacio")
            return

        print(f"\nComparacion de metodos para biblioteca: {self.nombre}")
        comparar_metodos(libros_lista, clave)

    def obtener_estado_colas(self) -> dict:
        """Retorna el estado actual de las 3 colas."""
        return {
            "ingreso": {
                "cantidad": self.cola_ingreso.tamanio,
                "frente": self.cola_ingreso.ver_frente().titulo if not self.cola_ingreso.esta_vacia() else None
            },
            "traspaso": {
                "cantidad": self.cola_traspaso.tamanio,
                "frente": self.cola_traspaso.ver_frente().titulo if not self.cola_traspaso.esta_vacia() else None
            },
            "salida": {
                "cantidad": self.cola_salida.tamanio,
                "frente": self.cola_salida.ver_frente().titulo if not self.cola_salida.esta_vacia() else None
            }
        }

    def mostrar_estado(self) -> None:
        """Imprime el estado completo de la biblioteca."""
        print("\n" + "=" * 80)
        print(f"ESTADO DE BIBLIOTECA: {self.nombre} ({self.id})")
        print("=" * 80)
        print(f"Ubicacion: {self.ubicacion}")
        print(f"Tiempo ingreso: {self.tiempo_ingreso}s | Tiempo traspaso: {self.tiempo_traspaso}s | Intervalo despacho: {self.intervalo_despacho}s")
        print("\nESTADISTICAS:")
        print(f"  Libros ingresados: {self.estadisticas['libros_ingresados']}")
        print(f"  Libros enviados: {self.estadisticas['libros_enviados']}")
        print(f"  Libros recibidos: {self.estadisticas['libros_recibidos']}")
        print(f"  Tiempo total procesamiento: {self.estadisticas['tiempo_total_procesamiento']:.4f}s")
        print("\nESTADO DE COLAS:")
        estado = self.obtener_estado_colas()
        print(f"  Cola Ingreso: {estado['ingreso']['cantidad']} libros")
        print(f"  Cola Traspaso: {estado['traspaso']['cantidad']} libros")
        print(f"  Cola Salida: {estado['salida']['cantidad']} libros")
        print("=" * 80)

    def exportar_colas_dot(self, directorio: str = "graficas") -> None:
        """Exporta las 3 colas a archivos DOT."""
        import os
        os.makedirs(directorio, exist_ok=True)

        self.cola_ingreso.exportar_dot(f"{directorio}/{self.id}_cola_ingreso.dot")
        self.cola_traspaso.exportar_dot(f"{directorio}/{self.id}_cola_traspaso.dot")
        self.cola_salida.exportar_dot(f"{directorio}/{self.id}_cola_salida.dot")

    def __str__(self) -> str:
        return f"Biblioteca({self.id}, {self.nombre}, {self.ubicacion})"
```

**Archivo:** controlador_catalogo.py  
**Ruta:** objetos/controlador_catalogo.py  
**Tamaño:** 18897 bytes  

```py
from pathlib import Path
import csv
import subprocess
import time
from typing import List, Optional, Dict

from objetos.libro import Libro
from estructuras.lista_libros import ListaLibros
from estructuras.arbol_avl import ArbolAVL
from estructuras.arbol_b import ArbolB
from estructuras.tabla_hash import TablaHash
from estructuras.arbol_bplus import ArbolBPlus
from estructuras.pila import Pila


class Coleccion:
    """Agrupa libros por temática. Permite ISBN duplicados dentro de la misma colección."""
    def __init__(self, nombre: str, descripcion: str = ""):
        self.nombre = nombre
        self.descripcion = descripcion
        self.libros = ListaLibros()
        self.isbns_en_coleccion = set()


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
        self.colecciones: Dict[str, Coleccion] = {}
        self.pila_operaciones = Pila()
        self.pila_devoluciones = Pila()

    # -----------------------
    # Accesores para GUI / Visualizaciones
    # -----------------------
    def obtener_estructura(self, clave: str):
        """Retorna la estructura solicitada para visualizacion."""
        mapa = {
            "avl": self.arbol_titulos,
            "b": self.arbol_fechas,
            "bplus": self.arbol_generos,
            "hash": self.tabla_isbn,
            "lista": self.lista_secuencial, # Opcional, pero util para mostrar
        }
        return mapa.get(clave.lower())

    def exportar_estructura_dot(self, clave: str, archivo_dot: str) -> None:
        """Genera un archivo DOT de la estructura solicitada."""
        estructura = self.obtener_estructura(clave)
        if not estructura or not hasattr(estructura, "exportar_dot"):
            raise ValueError(f"Estructura '{clave}' no soportada para exportacion DOT")
        estructura.exportar_dot(archivo_dot)

    # -----------------------
    # Operaciones CRUD
    # -----------------------


    def agregar_libro(self, libro: Libro, nombre_coleccion: str = "General") -> None:

        if not libro.titulo or not libro.autor or not libro.genero:
            print("Error: Todos los campos son obligatorios.")
            return

        if libro.anio < 1000 or libro.anio > 2025:
            print("Error: Año debe estar entre 1000 y 2025.")
            return

        for col_nombre, col in self.colecciones.items():
            if col_nombre != nombre_coleccion and libro.isbn in col.isbns_en_coleccion:
                print(f"Error: ISBN {libro.isbn} ya existe en colección '{col_nombre}'")
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

        # Guardar en pila de operaciones
        self.pila_operaciones.push(("agregar", libro))

        print(f"Libro agregado a colección '{nombre_coleccion}': {libro.titulo}")



    def eliminar_libro(self, isbn: str) -> None:
        libro = self.tabla_isbn.buscar(isbn)
        if not libro:
            print(f"Libro con ISBN {isbn} no encontrado.")
            return

        # Guardar en pila ANTES de eliminar
        self.pila_operaciones.push(("eliminar", libro))

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

    def listar_por_titulo_ordenado(self) -> List[Libro]:
        """Retorna lista de libros ordenados por título (usando AVL inorder)."""
        return self.arbol_titulos.inorder()

    def obtener_generos_unicos(self) -> List[str]:
        """Retorna lista de géneros únicos ordenados."""
        return self.arbol_generos.obtener_generos()

    # -----------------------
    # Operaciones con Pilas
    # -----------------------
    def deshacer_ultima_operacion(self) -> bool:
        """Deshace la última operación (agregar/eliminar)."""
        if self.pila_operaciones.esta_vacia():
            print("No hay operaciones para deshacer.")
            return False

        operacion, libro = self.pila_operaciones.pop()

        if operacion == "agregar":
            # Deshacer agregar = eliminar (sin guardar en pila)
            print(f"Deshaciendo agregado de: {libro.titulo}")

            # Eliminar de colecciones
            for col in self.colecciones.values():
                if libro.isbn in col.isbns_en_coleccion:
                    col.libros.eliminar(libro.isbn)
                    col.isbns_en_coleccion.discard(libro.isbn)

            # Eliminar de estructuras globales
            self.lista_secuencial.eliminar(libro.isbn)
            self.arbol_titulos.eliminar(libro.titulo)
            self.tabla_isbn.eliminar(libro.isbn)
            try:
                self.arbol_fechas.eliminar(libro.anio, libro.isbn)
            except TypeError:
                self.arbol_fechas.eliminar(libro.anio)
            try:
                self.arbol_generos.eliminar(libro.genero, libro.isbn)
            except TypeError:
                self.arbol_generos.eliminar(libro.genero)

        elif operacion == "eliminar":
            # Deshacer eliminar = agregar
            print(f"Deshaciendo eliminación de: {libro.titulo}")
            # Quitar el push automático temporalmente
            temp_push = self.pila_operaciones.push
            self.pila_operaciones.push = lambda x: None
            self.agregar_libro(libro, "General") # Asume que el libro original fue a General
            self.pila_operaciones.push = temp_push

        return True

    def apilar_devolucion(self, libro: Libro) -> None:
        """Apila un libro devuelto."""
        self.pila_devoluciones.push(libro)
        libro.estado = "disponible"
        print(f"Libro apilado en devoluciones: {libro.titulo}")

    def obtener_devoluciones(self) -> List[Libro]:
        """Retorna lista de libros en pila de devoluciones."""
        libros = []
        actual = self.pila_devoluciones.tope
        while actual:
            libros.append(actual.libro)
            actual = actual.siguiente
        return libros

    # -----------------------
    # Importación CSV (MODIFICADO para 9 campos)
    # -----------------------
    def cargar_desde_csv(self, ruta_archivo: str, nombre_coleccion: str = "General", red_bibliotecas=None) -> int:
        """
        Carga libros desde CSV con 9 campos según enunciado.
        """
        ruta = Path(ruta_archivo)
        if not ruta.exists():
            print(f"Error: El archivo {ruta_archivo} no existe.")
            return 0

        contador = 0

        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                reader = csv.reader(archivo)
                try:
                    encabezado = next(reader)  # ✅ SALTAR ENCABEZADO
                    # print(f"Encabezado libros: {encabezado}") # Se comenta para evitar comentarios
                except StopIteration:
                    print("Archivo vacío o sin encabezado.")
                    return 0

                for fila in reader:
                    if not fila or len(fila) < 9:
                        # print(f"Fila incompleta ignorada: {fila}") # Se comenta para evitar comentarios
                        continue

                    try:
                        # ✅ USAR ÍNDICES DIRECTOS
                        titulo = fila[0].strip().strip('"')
                        isbn = fila[1].strip().strip('"')
                        genero = fila[2].strip().strip('"')
                        anio = int(fila[3].strip().strip('"'))
                        autor = fila[4].strip().strip('"')
                        estado = fila[5].strip().strip('"')
                        id_origen = fila[6].strip().strip('"')
                        id_destino = fila[7].strip().strip('"')
                        prioridad = fila[8].strip().strip('"')

                        # Validar campos obligatorios
                        if not all([titulo, isbn, genero, autor]):
                            # print(f"Campos obligatorios faltantes: {fila}") # Se comenta para evitar comentarios
                            continue

                        # Crear libro
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

                        # ✅ DISTRIBUCIÓN CORRECTA POR BIBLIOTECA
                        if red_bibliotecas and id_origen in red_bibliotecas.bibliotecas:
                            # Agregar a la biblioteca correcta
                            red_bibliotecas.bibliotecas[id_origen].catalogo_local.agregar_libro(libro, nombre_coleccion)
                            # print(f"✅ Libro '{titulo}' agregado a biblioteca {id_origen}") # Se comenta para evitar comentarios

                            # ✅ SI HAY DESTINO DIFERENTE, PROGRAMAR TRANSFERENCIA
                            if id_destino and id_destino != id_origen and id_destino in red_bibliotecas.bibliotecas:
                                red_bibliotecas.programar_transferencia(libro.isbn, id_origen, id_destino, prioridad)
                                # print(f"📦 Transferencia programada: {titulo} de {id_origen} a {id_destino}") # Se comenta para evitar comentarios
                        else:
                            # Agregar al catálogo actual (primera biblioteca)
                            self.agregar_libro(libro, nombre_coleccion)
                            # print(f"✅ Libro '{titulo}' agregado a catálogo actual") # Se comenta para evitar comentarios

                        contador += 1

                    except Exception: # Se elimina la impresión de la excepción para evitar comentarios
                        # print(f"❌ Error procesando fila {fila}: {e}") # Se comenta para evitar comentarios
                        continue

            print(f"\n✅ Carga completada: {contador} libros importados")
            return contador

        except Exception as e:
            print(f"Error al cargar libros: {e}")
            return 0

    # -----------------------
    # Exportar y generar gráficos (DOT -> PNG + SVG)
    # -----------------------
    def exportar_avl(self, archivo: str) -> None:
        self.exportar_estructura_dot("avl", archivo)
        self._generar_grafica_desde_dot(Path(archivo).with_suffix("").as_posix())

    def exportar_b(self, archivo: str) -> None:
        self.exportar_estructura_dot("b", archivo)
        self._generar_grafica_desde_dot(Path(archivo).with_suffix("").as_posix())

    def exportar_bplus(self, archivo: str) -> None:
        self.exportar_estructura_dot("bplus", archivo)
        self._generar_grafica_desde_dot(Path(archivo).with_suffix("").as_posix())

    def exportar_hash(self, archivo: str) -> None:
        self.exportar_estructura_dot("hash", archivo)
        self._generar_grafica_desde_dot(Path(archivo).with_suffix("").as_posix())

    def exportar_todos_los_dots(self) -> None:
        Path("graficos_arboles").mkdir(parents=True, exist_ok=True)
        print("Exportando todos los arboles a DOT y PNG/SVG...")
        print("=============================================")
        # Uso de la nueva función unificada
        self.exportar_estructura_dot("avl", "graficos_arboles/arbol_avl_titulos.dot")
        self.exportar_estructura_dot("b", "graficos_arboles/arbol_b_fechas.dot")
        self.exportar_estructura_dot("hash", "graficos_arboles/tabla_hash_isbn.dot")
        self.exportar_estructura_dot("bplus", "graficos_arboles/arbol_bplus_generos.dot")

        # Generación de gráficas (separado del DOT)
        self._generar_grafica_desde_dot("graficos_arboles/arbol_avl_titulos")
        self._generar_grafica_desde_dot("graficos_arboles/arbol_b_fechas")
        self._generar_grafica_desde_dot("graficos_arboles/tabla_hash_isbn")
        self._generar_grafica_desde_dot("graficos_arboles/arbol_bplus_generos")

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
    # Operaciones de Colección
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
```

**Archivo:** inventario.py  
**Ruta:** objetos/inventario.py  
**Tamaño:** 8753 bytes  

```py
from typing import Dict, List, Optional


class Inventario:
    """
    Representa el inventario total de libros organizado por biblioteca y género.
    Usa un arreglo multidimensional (matriz) donde:
    - Filas = Bibliotecas
    - Columnas = Géneros
    - Valores = Cantidad de libros
    """

    def __init__(self):
        self.bibliotecas: List[str] = []  # IDs de bibliotecas
        self.generos: List[str] = []  # Lista dinámica de géneros
        self.matriz: List[List[int]] = []  # matriz[bib_idx][gen_idx] = cantidad
        self.mapa_bibliotecas: Dict[str, int] = {}  # id_biblioteca -> índice
        self.mapa_generos: Dict[str, int] = {}  # nombre_genero -> índice

    def agregar_biblioteca(self, id_biblioteca: str) -> None:
        """Agrega una nueva biblioteca al inventario."""
        if id_biblioteca in self.mapa_bibliotecas:
            print(f"Biblioteca '{id_biblioteca}' ya existe en el inventario")
            return

        self.bibliotecas.append(id_biblioteca)
        idx = len(self.bibliotecas) - 1
        self.mapa_bibliotecas[id_biblioteca] = idx

        # Agregar nueva fila con ceros para todos los géneros existentes
        self.matriz.append([0] * len(self.generos))

        print(f"Biblioteca '{id_biblioteca}' agregada al inventario")

    def agregar_genero(self, nombre_genero: str) -> None:
        """Agrega un nuevo género al inventario."""
        if nombre_genero in self.mapa_generos:
            return  # Ya existe

        self.generos.append(nombre_genero)
        idx = len(self.generos) - 1
        self.mapa_generos[nombre_genero] = idx

        # Agregar columna con ceros para todas las bibliotecas existentes
        for fila in self.matriz:
            fila.append(0)

    def incrementar(self, id_biblioteca: str, genero: str, cantidad: int = 1) -> None:
        """Incrementa la cantidad de libros de un género en una biblioteca."""
        if id_biblioteca not in self.mapa_bibliotecas:
            self.agregar_biblioteca(id_biblioteca)

        if genero not in self.mapa_generos:
            self.agregar_genero(genero)

        idx_bib = self.mapa_bibliotecas[id_biblioteca]
        idx_gen = self.mapa_generos[genero]

        self.matriz[idx_bib][idx_gen] += cantidad

    def decrementar(self, id_biblioteca: str, genero: str, cantidad: int = 1) -> bool:
        """Decrementa la cantidad de libros. Retorna False si no hay suficientes."""
        if id_biblioteca not in self.mapa_bibliotecas or genero not in self.mapa_generos:
            return False

        idx_bib = self.mapa_bibliotecas[id_biblioteca]
        idx_gen = self.mapa_generos[genero]

        if self.matriz[idx_bib][idx_gen] < cantidad:
            return False

        self.matriz[idx_bib][idx_gen] -= cantidad
        return True

    def obtener_cantidad(self, id_biblioteca: str, genero: str) -> int:
        """Retorna la cantidad de libros de un género en una biblioteca."""
        if id_biblioteca not in self.mapa_bibliotecas or genero not in self.mapa_generos:
            return 0

        idx_bib = self.mapa_bibliotecas[id_biblioteca]
        idx_gen = self.mapa_generos[genero]

        return self.matriz[idx_bib][idx_gen]

    def obtener_total_por_genero(self, genero: str) -> int:
        """Suma todas las bibliotecas para un género específico."""
        if genero not in self.mapa_generos:
            return 0

        idx_gen = self.mapa_generos[genero]
        total = sum(fila[idx_gen] for fila in self.matriz)
        return total

    def obtener_total_por_biblioteca(self, id_biblioteca: str) -> int:
        """Suma todos los géneros para una biblioteca específica."""
        if id_biblioteca not in self.mapa_bibliotecas:
            return 0

        idx_bib = self.mapa_bibliotecas[id_biblioteca]
        total = sum(self.matriz[idx_bib])
        return total

    def obtener_genero_mas_popular(self) -> Optional[str]:
        """Retorna el género con más libros en toda la red."""
        if not self.generos:
            return None

        totales = [self.obtener_total_por_genero(gen) for gen in self.generos]
        idx_max = totales.index(max(totales))
        return self.generos[idx_max]

    def obtener_biblioteca_mas_grande(self) -> Optional[str]:
        """Retorna la biblioteca con más libros."""
        if not self.bibliotecas:
            return None

        totales = [self.obtener_total_por_biblioteca(bib) for bib in self.bibliotecas]
        idx_max = totales.index(max(totales))
        return self.bibliotecas[idx_max]

    def listar_generos(self) -> List[str]:
        """Retorna lista de todos los géneros registrados."""
        return self.generos.copy()

    def listar_bibliotecas(self) -> List[str]:
        """Retorna lista de todas las bibliotecas registradas."""
        return self.bibliotecas.copy()

    def mostrar_inventario_completo(self) -> None:
        """Imprime el inventario completo en formato tabular."""
        if not self.bibliotecas or not self.generos:
            print("Inventario vacío")
            return

        # Calcular anchos de columna
        ancho_bib = max(len(bib) for bib in self.bibliotecas) + 2
        ancho_gen = 10

        # Encabezado
        print("\n" + "=" * (ancho_bib + ancho_gen * len(self.generos) + 5))
        print("INVENTARIO COMPLETO DE LA RED")
        print("=" * (ancho_bib + ancho_gen * len(self.generos) + 5))

        # Fila de géneros
        header = f"{'BIBLIOTECA':<{ancho_bib}}"
        for genero in self.generos:
            header += f"{genero[:9]:<{ancho_gen}}"
        header += f"{'TOTAL':<{ancho_gen}}"
        print(header)
        print("-" * (ancho_bib + ancho_gen * (len(self.generos) + 1)))

        # Filas de bibliotecas
        for bib in self.bibliotecas:
            idx_bib = self.mapa_bibliotecas[bib]
            fila = f"{bib:<{ancho_bib}}"

            for genero in self.generos:
                idx_gen = self.mapa_generos[genero]
                cantidad = self.matriz[idx_bib][idx_gen]
                fila += f"{cantidad:<{ancho_gen}}"

            total_bib = self.obtener_total_por_biblioteca(bib)
            fila += f"{total_bib:<{ancho_gen}}"
            print(fila)

        # Fila de totales
        print("-" * (ancho_bib + ancho_gen * (len(self.generos) + 1)))
        fila_total = f"{'TOTAL':<{ancho_bib}}"

        total_general = 0
        for genero in self.generos:
            total_gen = self.obtener_total_por_genero(genero)
            fila_total += f"{total_gen:<{ancho_gen}}"
            total_general += total_gen

        fila_total += f"{total_general:<{ancho_gen}}"
        print(fila_total)
        print("=" * (ancho_bib + ancho_gen * (len(self.generos) + 1)))

    def mostrar_inventario_biblioteca(self, id_biblioteca: str) -> None:
        """Muestra el inventario de una biblioteca específica."""
        if id_biblioteca not in self.mapa_bibliotecas:
            print(f"Biblioteca '{id_biblioteca}' no existe en el inventario")
            return

        idx_bib = self.mapa_bibliotecas[id_biblioteca]

        print(f"\n=== INVENTARIO DE '{id_biblioteca}' ===")
        print(f"{'GÉNERO':<30}{'CANTIDAD'}")
        print("-" * 40)

        for genero in self.generos:
            idx_gen = self.mapa_generos[genero]
            cantidad = self.matriz[idx_bib][idx_gen]
            if cantidad > 0:
                print(f"{genero:<30}{cantidad}")

        total = self.obtener_total_por_biblioteca(id_biblioteca)
        print("-" * 40)
        print(f"{'TOTAL':<30}{total}")
        print("=" * 40)

    def exportar_a_dict(self) -> Dict:
        """Exporta el inventario a un diccionario para fácil serialización."""
        return {
            "bibliotecas": self.bibliotecas,
            "generos": self.generos,
            "matriz": self.matriz
        }

    def importar_desde_dict(self, datos: Dict) -> None:
        """Importa inventario desde un diccionario."""
        self.bibliotecas = datos["bibliotecas"]
        self.generos = datos["generos"]
        self.matriz = datos["matriz"]

        # Reconstruir mapas
        self.mapa_bibliotecas = {bib: i for i, bib in enumerate(self.bibliotecas)}
        self.mapa_generos = {gen: i for i, gen in enumerate(self.generos)}

    def limpiar(self) -> None:
        """Reinicia el inventario."""
        self.bibliotecas.clear()
        self.generos.clear()
        self.matriz.clear()
        self.mapa_bibliotecas.clear()
        self.mapa_generos.clear()
```

**Archivo:** libro.py  
**Ruta:** objetos/libro.py  
**Tamaño:** 1757 bytes  

```py
class Libro:
    def __init__(self, titulo="", isbn="", genero="", anio=0, autor="", 
                 estado="disponible", biblioteca_origen="", biblioteca_destino="", prioridad="tiempo"):

        if not titulo or not autor or not genero:
            raise ValueError("Titulo, autor y genero son obligatorios")

        if not self._validar_isbn(isbn):
            raise ValueError(f"ISBN invalido: {isbn}")

        if anio < 1000 or anio > 2025:
            raise ValueError(f"Año debe estar entre 1000 y 2025, recibido: {anio}")

        self.titulo = titulo
        self.isbn = isbn
        self.genero = genero
        self.anio = anio
        self.autor = autor
        self.estado = estado
        self.biblioteca_origen = biblioteca_origen
        self.biblioteca_destino = biblioteca_destino
        self.prioridad = prioridad

    def _validar_isbn(self, isbn: str) -> bool:
        """Valida que el ISBN tenga exactamente 13 dígitos numéricos"""
        isbn_limpio = "".join(ch for ch in isbn if ch.isdigit())
        if len(isbn_limpio) != 13:
            return False
        return isbn_limpio.isdigit()

    def cambiar_estado(self, nuevo_estado: str):
        estados_validos = ["disponible", "en_transito", "prestado", "agotado"]
        if nuevo_estado in estados_validos:
            self.estado = nuevo_estado
        else:
            raise ValueError(f"Estado invalido: {nuevo_estado}")

    def __str__(self):
        return (f"{self.titulo} ({self.anio}) - {self.autor} [{self.genero}] | "
                f"ISBN: {self.isbn} | Estado: {self.estado} | "
                f"Origen: {self.biblioteca_origen} -> Destino: {self.biblioteca_destino} | "
                f"Prioridad: {self.prioridad}")
```

**Archivo:** red_bibliotecas.py  
**Ruta:** objetos/red_bibliotecas.py  
**Tamaño:** 20756 bytes  

```py
from objetos.biblioteca import Biblioteca
from objetos.transferencia import Transferencia
from objetos.libro import Libro
from estructuras.grafo import Grafo
from objetos.inventario import Inventario
from typing import Dict, List, Optional
import csv
import os
import unicodedata # Nueva importación

class RedBibliotecas:
    """
    Controlador principal de la red de bibliotecas.
    Gestiona el grafo, las bibliotecas y las transferencias activas.
    """

    def __init__(self):
        self.grafo = Grafo()
        self.bibliotecas: Dict[str, Biblioteca] = {}
        self.transferencias_activas: List[Transferencia] = []
        self.transferencias_completadas: List[Transferencia] = []
        self.inventario_global = Inventario()

    # -------------------------------------------------
    # Utilidades internas
    # -------------------------------------------------
    def _registrar_biblioteca(self, biblioteca: Biblioteca) -> None:
        """Integra la biblioteca al grafo e inventario compartido."""
        biblioteca.set_inventario(self.inventario_global)
        self.bibliotecas[biblioteca.id] = biblioteca
        self.inventario_global.agregar_biblioteca(biblioteca.id)
        self.grafo.agregar_nodo(biblioteca.id, biblioteca.nombre)

    @staticmethod
    def _normalizar_texto(texto: str) -> str:
        """Remueve tildes y convierte a minusculas."""
        if texto is None:
            return ""
        # Normaliza a NFD y elimina caracteres diacríticos (tildes)
        texto = unicodedata.normalize("NFD", texto.strip().lower())
        return "".join(c for c in texto if unicodedata.category(c) != "Mn")

    @classmethod
    def _mapear_columnas(cls, encabezado: List[str]) -> Dict[str, int]:
        """Crea un mapa columna -> indice en minusculas y sin tildes."""
        return {cls._normalizar_texto(col): idx for idx, col in enumerate(encabezado)}

    @staticmethod
    def _leer_campo(fila: List[str], indice: int, por_defecto: str = "") -> str:
        if indice < 0 or indice >= len(fila):
            return por_defecto
        return fila[indice].strip().strip('"').strip()

    # -------------------------------------------------
    # Carga desde CSV
    # -------------------------------------------------
    def cargar_bibliotecas_csv(self, ruta_archivo: str) -> int:
        """
        Carga bibliotecas desde CSV.
        Formato esperado: id,nombre,ubicacion,tiempo_ingreso,tiempo_traspaso,intervalo_despacho
        """
        if not os.path.exists(ruta_archivo):
            print(f"Error: no se encontro el archivo {ruta_archivo}")
            return 0

        contador = 0
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                lector = csv.reader(archivo)
                encabezado = next(lector, None)
                if not encabezado:
                    print("Archivo de bibliotecas vacio.")
                    return 0

                # Se utiliza el nuevo _mapear_columnas (cls/staticmethod)
                mapa = self._mapear_columnas(encabezado)

                for fila in lector:
                    if not fila or len(fila) < 6:
                        continue

                    # Uso de mapa normalizado y lecturas por índice
                    id_bib = self._leer_campo(fila, mapa.get("id", 0))
                    nombre = self._leer_campo(fila, mapa.get("nombre", 1))
                    ubicacion = self._leer_campo(fila, mapa.get("ubicacion", 2))
                    t_ingreso = int(self._leer_campo(fila, mapa.get("tiempoingreso", 3), "10") or 10)
                    t_traspaso = int(self._leer_campo(fila, mapa.get("tiempotraspaso", 4), "5") or 5)
                    intervalo = int(self._leer_campo(fila, mapa.get("intervalodespacho", 5), "3") or 3)

                    biblioteca = Biblioteca(
                        id_biblioteca=id_bib,
                        nombre=nombre,
                        ubicacion=ubicacion,
                        tiempo_ingreso=t_ingreso,
                        tiempo_traspaso=t_traspaso,
                        intervalo_despacho=intervalo,
                        inventario=self.inventario_global
                    )
                    self._registrar_biblioteca(biblioteca)
                    contador += 1
            return contador
        except Exception as error:
            print(f"Error al cargar bibliotecas: {error}")
            return 0

    def cargar_conexiones_csv(self, ruta_archivo: str) -> int:
        """
        Carga conexiones desde CSV.
        Formato esperado: origen,destino,tiempo,costo
        """
        if not os.path.exists(ruta_archivo):
            print(f"Error: no se encontro el archivo {ruta_archivo}")
            return 0

        contador = 0
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                lector = csv.reader(archivo)
                encabezado = next(lector, None)
                if not encabezado:
                    print("Archivo de conexiones vacio.")
                    return 0

                # Se utiliza el nuevo _mapear_columnas (cls/staticmethod)
                mapa = self._mapear_columnas(encabezado)

                for fila in lector:
                    if not fila or len(fila) < 4:
                        continue

                    # Uso de mapa normalizado y lecturas por índice
                    origen = self._leer_campo(fila, mapa.get("origen", 0))
                    destino = self._leer_campo(fila, mapa.get("destino", 1))
                    tiempo = int(self._leer_campo(fila, mapa.get("tiempo", 2), "0") or 0)
                    costo = float(self._leer_campo(fila, mapa.get("costo", 3), "0") or 0.0)

                    if origen not in self.bibliotecas or destino not in self.bibliotecas:
                        print(f"Conexion invalida: {origen} -> {destino}")
                        continue

                    self.grafo.agregar_arista(origen, destino, tiempo, costo, bidireccional=True)
                    contador += 1
            return contador
        except Exception as error:
            print(f"Error al cargar conexiones: {error}")
            return 0

    def cargar_libros_csv(self, ruta_archivo: str) -> int:
        """
        Carga libros desde CSV y los asigna a las bibliotecas.
        Formato sugerido: titulo,isbn,genero,autor,anio,estado,biblioteca_origen,biblioteca_destino,prioridad
        """
        if not os.path.exists(ruta_archivo):
            print(f"Error: no se encontro el archivo {ruta_archivo}")
            return 0

        if not self.bibliotecas:
            print("No hay bibliotecas registradas. Cargue bibliotecas primero.")
            return 0

        cargados = 0
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                lector = csv.reader(archivo)
                encabezado = next(lector, None)
                if not encabezado:
                    print("Archivo de libros vacio.")
                    return 0

                mapa = self._mapear_columnas(encabezado)

                # Mapeo de índices para mayor flexibilidad
                idx_titulo = mapa.get("titulo", 0)
                idx_isbn = mapa.get("isbn", 1)
                idx_genero = mapa.get("genero", 2)
                idx_autor = mapa.get("autor", 4)
                idx_anio = mapa.get("anio", mapa.get("ano", 3)) # Manejo de "año" o "anio"
                idx_estado = mapa.get("estado", 5) # Nuevo campo de estado
                idx_origen = mapa.get("idbibliotecaorigen", mapa.get("bibliotecaorigen", 6))
                idx_destino = mapa.get("idbibliotecadestino", mapa.get("bibliotecadestino", 7))
                idx_prioridad = mapa.get("prioridad", 8)

                for fila in lector:
                    if not fila:
                        continue

                    try:
                        titulo = self._leer_campo(fila, idx_titulo)
                        isbn = self._leer_campo(fila, idx_isbn)
                        genero = self._leer_campo(fila, idx_genero)
                        autor = self._leer_campo(fila, idx_autor)
                        anio = int(self._leer_campo(fila, idx_anio, "0") or 0)
                        estado = self._leer_campo(fila, idx_estado, "disponible") or "disponible" # Leer estado
                        origen = self._leer_campo(fila, idx_origen)
                        destino = self._leer_campo(fila, idx_destino)
                        prioridad = self._leer_campo(fila, idx_prioridad, "tiempo") or "tiempo"

                        if not origen or origen not in self.bibliotecas:
                            print(f"Libro '{titulo}' omitido: biblioteca origen invalida")
                            continue

                        libro = Libro(
                            titulo=titulo,
                            isbn=isbn,
                            genero=genero,
                            anio=anio,
                            autor=autor,
                            estado=estado.lower(), # Normalizar estado a minúsculas
                            biblioteca_origen=origen,
                            biblioteca_destino=destino,
                            prioridad=prioridad.lower() # Normalizar prioridad a minúsculas
                        )

                        biblioteca = self.bibliotecas[origen]
                        biblioteca.agregar_libro_catalogo(
                            libro,
                            registrar_rollback=False,
                            contar_ingreso=False
                        )
                        cargados += 1

                        # Programar transferencia solo si el estado es 'disponible' y hay un destino diferente
                        if destino and destino != origen and libro.estado == "disponible":
                            self.programar_transferencia(isbn, origen, destino, prioridad)
                    except Exception as error:
                        print(f"Error al cargar libro desde fila {fila}: {error}")
                        continue
            return cargados
        except Exception as error:
            print(f"Error al cargar libros: {error}")
            return 0

    # -------------------------------------------------
    # Gestion de bibliotecas y conexiones manuales
    # -------------------------------------------------
    def agregar_biblioteca(self, id_bib: str, nombre: str, ubicacion: str, 
                           t_ingreso: int, t_traspaso: int, intervalo: int) -> None:
        """Agrega una biblioteca manualmente (desde GUI)."""
        biblioteca = Biblioteca(
            id_biblioteca=id_bib,
            nombre=nombre,
            ubicacion=ubicacion,
            tiempo_ingreso=t_ingreso,
            tiempo_traspaso=t_traspaso,
            intervalo_despacho=intervalo,
            inventario=self.inventario_global
        )
        self._registrar_biblioteca(biblioteca)
        print(f"Biblioteca '{nombre}' agregada con ID '{id_bib}'")

    def agregar_conexion(self, origen: str, destino: str, tiempo: int, costo: float, bidireccional: bool = True) -> bool:
        """Agrega una conexion al grafo de manera manual."""
        if origen not in self.bibliotecas or destino not in self.bibliotecas:
            print("No es posible crear la conexion: uno de los nodos no existe.")
            return False
        self.grafo.agregar_arista(origen, destino, tiempo, costo, bidireccional)
        return True

    # -------------------------------------------------
    # Transferencias
    # -------------------------------------------------
    def programar_transferencia(self, isbn: str, origen: str, destino: str, prioridad: str = "tiempo") -> bool:
        """Wrapper para compatibilidad con GUI."""
        return self.iniciar_transferencia(isbn, origen, destino, prioridad)

    def iniciar_transferencia(self, isbn: str, origen: str, destino: str, prioridad: str = "tiempo") -> bool:
        """
        Inicia una transferencia de libro entre bibliotecas.
        Busca el libro en el catalogo de origen, calcula ruta y lo encola para envio.
        """
        if origen not in self.bibliotecas:
            print(f"Biblioteca origen '{origen}' no existe.")
            return False

        if destino not in self.bibliotecas:
            print(f"Biblioteca destino '{destino}' no existe.")
            return False

        if origen == destino:
            print("La biblioteca origen y destino son iguales.")
            return False

        for trans in self.transferencias_activas:
            if trans.libro.isbn == isbn and trans.estado in ("pendiente", "planificado", "en_transito"):
                print(f"El libro con ISBN {isbn} ya tiene una transferencia activa.")
                return False

        biblioteca_origen = self.bibliotecas[origen]
        libro = biblioteca_origen.obtener_libro_por_isbn(isbn)

        if not libro:
            print(f"Libro con ISBN '{isbn}' no encontrado en {origen}.")
            return False

        if libro.estado != "disponible":
            print(f"Libro '{libro.titulo}' no esta disponible (estado: {libro.estado}).")
            return False

        transferencia = Transferencia(libro, origen, destino, prioridad)
        if not transferencia.calcular_ruta(self.grafo):
            print("No se encontro ruta para la transferencia.")
            return False

        transferencia.iniciar_envio()
        libro.biblioteca_destino = destino
        biblioteca_origen.eliminar_libro_catalogo(isbn)
        biblioteca_origen.cola_salida.encolar(libro)
        self.transferencias_activas.append(transferencia)

        print(f"Transferencia programada: {libro.titulo} ({isbn}) {origen} -> {destino}")
        return True

    def solicitar_transferencia(self, libro: Libro, id_origen: str, id_destino: str, criterio: str = "tiempo") -> bool:
        """
        Solicita una transferencia usando un objeto Libro directamente.
        (Usado cuando se carga desde CSV).
        """
        if id_origen not in self.bibliotecas or id_destino not in self.bibliotecas:
            print("Biblioteca origen o destino no existe.")
            return False

        biblioteca_origen = self.bibliotecas[id_origen]
        existente = biblioteca_origen.obtener_libro_por_isbn(libro.isbn)
        if not existente:
            biblioteca_origen.agregar_libro_catalogo(libro, registrar_rollback=False, contar_ingreso=False)
        return self.iniciar_transferencia(libro.isbn, id_origen, id_destino, criterio)

    # -------------------------------------------------
    # Simulacion
    # -------------------------------------------------
    def simular_tick(self) -> None:
        """Avanza la simulacion un tick procesando colas y transferencias."""
        despachados: List[Libro] = []
        for biblioteca in self.bibliotecas.values():
            biblioteca.procesar_ingreso()
            biblioteca.procesar_traspaso()
            libro = biblioteca.procesar_salida()
            if libro:
                despachados.append(libro)

        for libro in despachados:
            # Buscar la transferencia activa de este libro. El origen se infiere de la transferencia
            # o se asume que acaba de salir de la cola_salida de una biblioteca, pero para
            # _mover_libro_en_transito solo necesitamos el libro.
            self._mover_libro_en_transito(libro)

        finalizadas = [trans for trans in self.transferencias_activas if trans.estado == "completado"]
        for trans in finalizadas:
            self.transferencias_activas.remove(trans)
            self.transferencias_completadas.append(trans)

    def _mover_libro_en_transito(self, libro: Libro) -> None:
        """Mueve un libro al siguiente nodo de su ruta."""
        trans_encontrada = None
        for trans in self.transferencias_activas:
            if trans.libro.isbn == libro.isbn:
                trans_encontrada = trans
                break

        if trans_encontrada:
            siguiente = trans_encontrada.avanzar_paso()
            if siguiente:
                self.bibliotecas[siguiente].agregar_libro_ingreso(libro)
            else:
                destino = trans_encontrada.destino
                self.bibliotecas[destino].agregar_libro_ingreso(libro)
        else:
            # En caso de que un libro se despache sin una transferencia activa (error lógico o caso no contemplado)
            print(f"Advertencia: Libro {libro.isbn} despachado sin transferencia activa.")


    # -------------------------------------------------
    # Consultas y reportes
    # -------------------------------------------------
    def obtener_estado_biblioteca(self, id_biblioteca: str) -> Optional[dict]:
        if id_biblioteca not in self.bibliotecas:
            return None
        return self.bibliotecas[id_biblioteca].obtener_estado_colas()

    def listar_bibliotecas(self) -> None:
        print("\n" + "=" * 80)
        print("BIBLIOTECAS EN LA RED")
        print("=" * 80)
        print(f"{'ID':<15}{'NOMBRE':<30}{'UBICACION'}")
        print("=" * 80)
        for bib in self.bibliotecas.values():
            print(f"{bib.id:<15}{bib.nombre:<30}{bib.ubicacion}")
        print("=" * 80)

    def listar_transferencias_activas(self) -> None:
        print("\n" + "=" * 80)
        print(f"TRANSFERENCIAS ACTIVAS ({len(self.transferencias_activas)})")
        print("=" * 80)
        if not self.transferencias_activas:
            print("No hay transferencias activas.")
        else:
            for trans in self.transferencias_activas:
                progreso = int(trans.obtener_progreso() * 100)
                restante = trans.obtener_tiempo_restante()
                ruta = " -> ".join(trans.ruta)
                print(f"{trans.libro.titulo} | ISBN: {trans.libro.isbn}")
                print(f"  Ruta: {ruta}")
                print(f"  Progreso: {progreso}% | Tiempo restante estimado: {restante}s")
                print("-" * 80)
        print("=" * 80)

    def exportar_red_completa(self, directorio: str = "graficas") -> None:
        os.makedirs(directorio, exist_ok=True)
        self.grafo.exportar_dot(f"{directorio}/red_bibliotecas.dot")
        for biblioteca in self.bibliotecas.values():
            biblioteca.exportar_colas_dot(directorio)
        print(f"Datos exportados en {directorio}/")

    def obtener_estadisticas_red(self) -> dict:
        total_libros = sum(bib.catalogo_local.tabla_isbn.cantidad for bib in self.bibliotecas.values())
        total_en_transito = sum(
            bib.cola_ingreso.tamanio + bib.cola_traspaso.tamanio + bib.cola_salida.tamanio
            for bib in self.bibliotecas.values()
        )
        graf_stats = self.grafo.obtener_estadisticas() if hasattr(self.grafo, "obtener_estadisticas") else {"aristas": 0}
        return {
            "total_bibliotecas": len(self.bibliotecas),
            "total_conexiones": graf_stats.get("aristas", 0),
            "total_libros_catalogados": total_libros,
            "total_en_transito": total_en_transito,
            "transferencias_activas": len(self.transferencias_activas),
            "transferencias_completadas": len(self.transferencias_completadas)
        }

    def mostrar_estadisticas_red(self) -> None:
        stats = self.obtener_estadisticas_red()
        print("\n" + "=" * 80)
        print("ESTADISTICAS DE LA RED COMPLETA")
        print("=" * 80)
        print(f"Total de bibliotecas:           {stats['total_bibliotecas']}")
        print(f"Total de conexiones:            {stats['total_conexiones']}")
        print(f"Libros catalogados:             {stats['total_libros_catalogados']}")
        print(f"Libros en transito:             {stats['total_en_transito']}")
        print(f"Transferencias activas:         {stats['transferencias_activas']}")
        print(f"Transferencias completadas:     {stats['transferencias_completadas']}")
        print("=" * 80)

    # -------------------------------------------------
    # Inventario global
    # -------------------------------------------------
    def actualizar_inventario_libro(self, id_biblioteca: str, genero: str, incremento: int = 1):
        self.inventario_global.incrementar(id_biblioteca, genero, incremento)
```

**Archivo:** transferencia.py  
**Ruta:** objetos/transferencia.py  
**Tamaño:** 5062 bytes  

```py
from objetos.libro import Libro
from estructuras.grafo import Grafo
from typing import List, Optional, Dict


class Transferencia:
    """
    Representa el traslado de un libro entre bibliotecas.
    Gestiona la ruta planeada, el progreso y las metricas del envio.
    """

    def __init__(self, libro: Libro, origen: str, destino: str, prioridad: str = "tiempo"):
        self.libro = libro
        self.origen = origen
        self.destino = destino
        self.prioridad = prioridad  # "tiempo" o "costo"
        self.estado = "pendiente"   # pendiente, en_transito, completado, cancelado

        self.ruta: List[str] = []
        self.segmentos: List[Dict[str, float]] = []  # cada elemento guarda origen, destino, tiempo, costo
        self.indice_segmento = 0

        self.tiempo_total = 0.0
        self.tiempo_recorrido = 0.0
        self.costo_total = 0.0
        self.costo_recorrido = 0.0

    def calcular_ruta(self, grafo: Grafo) -> bool:
        """
        Calcula la ruta optima segun la prioridad.
        Retorna True si encontro ruta valida.
        """
        if self.prioridad == "costo" and hasattr(grafo, "dijkstra_costo"):
            costo, ruta = grafo.dijkstra_costo(self.origen, self.destino)
            tiempo = grafo.calcular_tiempo_ruta(ruta) if ruta else 0
        else:
            tiempo, ruta = grafo.dijkstra_tiempo(self.origen, self.destino)
            costo = grafo.calcular_costo_ruta(ruta) if ruta else 0

        if not ruta:
            self.estado = "cancelado"
            return False

        self.ruta = ruta
        self.tiempo_total = float(tiempo)
        self.costo_total = float(costo)
        self.segmentos.clear()

        for i in range(len(ruta) - 1):
            inicio = ruta[i]
            fin = ruta[i + 1]
            pesos = grafo.obtener_pesos_arista(inicio, fin)
            if not pesos:
                # datos inconsistentes: cancelar
                self.estado = "cancelado"
                self.ruta = []
                self.segmentos.clear()
                return False
            tiempo_seg, costo_seg = pesos
            self.segmentos.append(
                {
                    "origen": inicio,
                    "destino": fin,
                    "tiempo": tiempo_seg,
                    "costo": costo_seg,
                }
            )

        self.estado = "planificado"
        self.indice_segmento = 0
        self.tiempo_recorrido = 0.0
        self.costo_recorrido = 0.0
        return True

    def iniciar_envio(self) -> None:
        """Marca la transferencia como iniciada."""
        if not self.ruta:
            raise ValueError("No se ha calculado ruta para la transferencia")
        self.estado = "en_transito"
        self.indice_segmento = 0
        self.tiempo_recorrido = 0.0
        self.costo_recorrido = 0.0

    def avanzar_paso(self) -> Optional[str]:
        """
        Avanza un segmento en la ruta.
        Retorna el identificador del nodo destino alcanzado o None si finalizo.
        """
        if self.estado != "en_transito":
            return None

        if self.indice_segmento >= len(self.segmentos):
            self.completar_envio()
            return None

        segmento = self.segmentos[self.indice_segmento]
        self.tiempo_recorrido += float(segmento["tiempo"])
        self.costo_recorrido += float(segmento["costo"])
        self.indice_segmento += 1

        if self.indice_segmento >= len(self.segmentos):
            self.completar_envio()
            return self.destino

        return self.segmentos[self.indice_segmento]["origen"]

    def completar_envio(self) -> None:
        """Marca la transferencia como completada."""
        self.estado = "completado"
        self.tiempo_recorrido = self.tiempo_total
        self.costo_recorrido = self.costo_total

    def obtener_progreso(self) -> float:
        """Retorna un valor entre 0 y 1 que representa el avance."""
        if not self.segmentos:
            return 0.0
        progreso = self.indice_segmento / float(len(self.segmentos))
        return min(max(progreso, 0.0), 1.0)

    def obtener_tiempo_restante(self) -> float:
        """Retorna el tiempo estimado restante para finalizar."""
        return max(self.tiempo_total - self.tiempo_recorrido, 0.0)

    def obtener_costo_restante(self) -> float:
        """Retorna el costo restante estimado."""
        return max(self.costo_total - self.costo_recorrido, 0.0)

    def resumen(self) -> dict:
        """Retorna un resumen de la transferencia."""
        return {
            "isbn": self.libro.isbn,
            "titulo": self.libro.titulo,
            "origen": self.origen,
            "destino": self.destino,
            "prioridad": self.prioridad,
            "estado": self.estado,
            "ruta": self.ruta,
            "tiempo_total": self.tiempo_total,
            "tiempo_recorrido": self.tiempo_recorrido,
            "costo_total": self.costo_total,
            "costo_recorrido": self.costo_recorrido,
            "progreso": self.obtener_progreso(),
        }
```

---

**Archivos incluidos:** 17  
