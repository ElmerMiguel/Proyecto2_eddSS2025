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