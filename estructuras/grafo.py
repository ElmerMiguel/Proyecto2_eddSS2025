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
        
        
    
    
    def exportar_dot_con_ruta(self, archivo: str, ruta: List[str] = None, color_ruta: str = "#ff4444"):
        """
        Exporta el grafo resaltando una ruta específica.
        
        Args:
            archivo: Archivo DOT de salida
            ruta: Lista de nodos que forman la ruta a resaltar
            color_ruta: Color para resaltar la ruta (por defecto rojo)
        """
        with open(archivo, "w", encoding="utf-8") as out:
            out.write("digraph RedBibliotecas {\n    rankdir=LR;\n")
            out.write("    node [shape=ellipse, style=filled, fillcolor=\"#cfe2ff\"];\n")
            out.write("    edge [color=\"#4a90e2\", fontcolor=\"#1f3d7a\", fontsize=10];\n\n")
            
            # Nodos - resaltar los de la ruta
            for nodo in self.nodos:
                etiqueta = self.etiquetas.get(nodo, nodo)
                if ruta and nodo in ruta:
                    # Nodo en la ruta - color destacado
                    out.write(f'    "{nodo}" [label="{etiqueta}\\n({nodo})", fillcolor="#ffeb3b", penwidth=3];\n')
                else:
                    # Nodo normal
                    out.write(f'    "{nodo}" [label="{etiqueta}\\n({nodo})"];\n')
            
            out.write("\n")
            
            # Aristas - resaltar las de la ruta
            aristas_ruta = set()
            if ruta and len(ruta) > 1:
                for i in range(len(ruta) - 1):
                    aristas_ruta.add((ruta[i], ruta[i + 1]))
            
            for origen, aristas in self.nodos.items():
                for arista in aristas:
                    if (origen, arista.destino) in aristas_ruta:
                        # Arista en la ruta - color y grosor destacado
                        out.write(
                            f'    "{origen}" -> "{arista.destino}" '
                            f'[label="t={arista.tiempo}s\\nc={arista.costo:.2f}", '
                            f'color="{color_ruta}", penwidth=4, fontcolor="{color_ruta}"];\n'
                        )
                    else:
                        # Arista normal
                        out.write(
                            f'    "{origen}" -> "{arista.destino}" '
                            f'[label="t={arista.tiempo}s\\nc={arista.costo:.2f}"];\n'
                        )
            
            out.write("}\n")
    

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