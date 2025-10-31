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

    def agregar_nodo(self, nombre: str, etiqueta: str = None):
        """
        Agrega un nodo al grafo.
        nombre: ID único del nodo
        etiqueta: Nombre legible para visualización (opcional)
        """
        if nombre not in self.nodos:
            self.nodos[nombre] = []
            # Guardar etiqueta para exportación DOT
            if etiqueta and not hasattr(self, 'etiquetas'):
                self.etiquetas = {}
            if etiqueta:
                self.etiquetas[nombre] = etiqueta

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
        
        return len(self.nodos[origen]) < cantidad_inicial

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
        
        rutas_prohibidas = set()
        
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
                                     rutas_prohibidas: set) -> Tuple[float, List[str]]:
        """
        Dijkstra modificado que evita rutas ya encontradas.
        """
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

        if not camino or camino[0] != origen:
            return (math.inf, [])
        
        if tuple(camino) in rutas_prohibidas:
            return (math.inf, [])

        return (distancias[destino], camino)

    def calcular_eta(self, origen: str, destino: str, prioridad: str = "tiempo") -> int:
        """
        Calcula tiempo estimado de llegada (ETA) en segundos.
        """
        if prioridad == "tiempo":
            tiempo_total, _ = self.dijkstra_tiempo(origen, destino)
            return int(tiempo_total) if tiempo_total != math.inf else 0
        else:
            costo_total, camino = self.dijkstra_costo(origen, destino)
            if costo_total == math.inf:
                return 0
            
            tiempo_total = 0
            for i in range(len(camino) - 1):
                for arista in self.nodos[camino[i]]:
                    if arista.destino == camino[i + 1]:
                        tiempo_total += arista.tiempo
                        break
            
            return tiempo_total

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
        
        max_conexiones = 0
        nodo_mas_conectado = None
        
        suma_tiempos = 0
        suma_costos = 0
        
        for nodo, aristas in self.nodos.items():
            conexiones = len(aristas)
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
            "max_conexiones": max_conexiones,
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
        """
        with open(archivo, "w", encoding="utf-8") as out:
            out.write("digraph RedBibliotecas {\n")
            out.write("    rankdir=LR;\n")
            out.write("    node [shape=circle, style=filled, fillcolor=lightblue];\n")
            out.write("    edge [fontsize=10];\n\n")

            aristas_procesadas = set()

            for origen, aristas in self.nodos.items():
                for arista in aristas:
                    par = (origen, arista.destino)
                    par_inverso = (arista.destino, origen)
                    
                    if par in aristas_procesadas:
                        continue
                    
                    es_bidireccional = False
                    if arista.destino in self.nodos:
                        for arista_vuelta in self.nodos[arista.destino]:
                            if arista_vuelta.destino == origen:
                                es_bidireccional = True
                                break
                    
                    flecha = " [dir=both]" if es_bidireccional else ""
                    
                    out.write(f'    "{origen}" -> "{arista.destino}" ')
                    out.write(f'[label="T:{arista.tiempo}s | C:{arista.costo:.1f}"{flecha}];\n')
                    
                    aristas_procesadas.add(par)
                    if es_bidireccional:
                        aristas_procesadas.add(par_inverso)

            out.write("}\n")
        
        print(f"Grafo exportado: {archivo}")