from typing import List, Dict, Optional
from dataclasses import dataclass
import os

@dataclass
class Libro:
    titulo: str
    isbn: str
    genero: str
    anio: int
    autor: str


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
