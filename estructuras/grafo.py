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

    def agregar_nodo(self, nombre: str):
        if nombre not in self.nodos:
            self.nodos[nombre] = []

    def agregar_arista(self, origen: str, destino: str, tiempo: int, costo: float, bidireccional: bool = True):
        self.agregar_nodo(origen)
        self.agregar_nodo(destino)
        self.nodos[origen].append(Arista(destino, tiempo, costo))
        if bidireccional:
            self.nodos[destino].append(Arista(origen, tiempo, costo))

    def dijkstra_tiempo(self, origen: str, destino: str) -> Tuple[int, List[str]]:
        return self._dijkstra(origen, destino, usar_tiempo=True)

    def dijkstra_costo(self, origen: str, destino: str) -> Tuple[float, List[str]]:
        return self._dijkstra(origen, destino, usar_tiempo=False)

    def _dijkstra(self, origen: str, destino: str, usar_tiempo: bool):
        if origen not in self.nodos or destino not in self.nodos:
            return (math.inf, [])

        distancias = {nodo: math.inf for nodo in self.nodos}
        previos = {nodo: None for nodo in self.nodos}
        distancias[origen] = 0
        visitados = set()

        while len(visitados) < len(self.nodos):
            nodo_actual = None
            distancia_minima = math.inf

            for nodo in self.nodos:
                if nodo not in visitados and distancias[nodo] < distancia_minima:
                    distancia_minima = distancias[nodo]
                    nodo_actual = nodo

            if nodo_actual is None or nodo_actual == destino:
                break

            visitados.add(nodo_actual)

            for arista in self.nodos[nodo_actual]:
                peso = arista.tiempo if usar_tiempo else arista.costo
                distancia = distancias[nodo_actual] + peso

                if distancia < distancias[arista.destino]:
                    distancias[arista.destino] = distancia
                    previos[arista.destino] = nodo_actual

        camino = []
        nodo = destino
        while nodo is not None:
            camino.insert(0, nodo)
            nodo = previos[nodo]

        if camino[0] != origen:
            return (math.inf, [])

        return (distancias[destino], camino)

    def exportar_dot(self, archivo: str):
        with open(archivo, "w", encoding="utf-8") as out:
            out.write("digraph RedBibliotecas {\n")
            out.write("    rankdir=LR;\n")
            out.write("    node [shape=circle, style=filled, fillcolor=lightblue];\n\n")

            for origen, aristas in self.nodos.items():
                for arista in aristas:
                    out.write(f'    "{origen}" -> "{arista.destino}" ')
                    out.write(f'[label="T:{arista.tiempo} C:{arista.costo}"];\n')

            out.write("}\n")
        print(f"Grafo exportado: {archivo}")