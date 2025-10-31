from objetos.libro import Libro
from estructuras.grafo import Grafo
from typing import List, Optional
import time


class Transferencia:
    """
    Representa una transferencia de libro entre bibliotecas.
    Gestiona la ruta calculada y el estado del envio.
    """
    
    def __init__(self, libro: Libro, origen: str, destino: str, prioridad: str = "tiempo"):
        self.libro = libro
        self.origen = origen
        self.destino = destino
        self.prioridad = prioridad
        
        self.ruta: List[str] = []
        self.peso_total: float = 0.0
        self.indice_actual = 0
        
        self.estado = "pendiente"
        self.tiempo_inicio: Optional[float] = None
        self.tiempo_fin: Optional[float] = None
        
        self.eta_segundos = 0

    def calcular_ruta(self, grafo: Grafo) -> bool:
        """
        Calcula la ruta optima usando Dijkstra segun la prioridad.
        Retorna True si encontro ruta, False si no hay camino.
        """
        if self.prioridad == "tiempo":
            peso, ruta = grafo.dijkstra_tiempo(self.origen, self.destino)
        else:
            peso, ruta = grafo.dijkstra_costo(self.origen, self.destino)
        
        if not ruta or peso == float('inf'):
            print(f"No existe ruta entre {self.origen} y {self.destino}")
            return False
        
        self.ruta = ruta
        self.peso_total = peso
        self.eta_segundos = grafo.calcular_eta(self.origen, self.destino, self.prioridad)
        
        print(f"Ruta calculada: {' -> '.join(ruta)}")
        print(f"Peso total ({self.prioridad}): {peso}")
        print(f"ETA: {self.eta_segundos} segundos")
        
        return True

    def iniciar_envio(self) -> None:
        """Inicia el proceso de envio."""
        if not self.ruta:
            print("Error: Debe calcular la ruta primero")
            return
        
        self.estado = "en_proceso"
        self.tiempo_inicio = time.time()
        self.libro.cambiar_estado("en_transito")
        self.libro.biblioteca_origen = self.origen
        self.libro.biblioteca_destino = self.destino
        
        print(f"Transferencia iniciada: {self.libro.titulo}")
        print(f"Desde: {self.origen} -> Hacia: {self.destino}")

    def avanzar_paso(self) -> Optional[str]:
        """
        Avanza al siguiente nodo de la ruta.
        Retorna el siguiente nodo o None si ya llego al destino.
        """
        if self.estado != "en_proceso":
            return None
        
        if self.indice_actual >= len(self.ruta) - 1:
            self.completar_envio()
            return None
        
        self.indice_actual += 1
        nodo_actual = self.ruta[self.indice_actual]
        
        print(f"Libro '{self.libro.titulo}' ahora en: {nodo_actual}")
        return nodo_actual

    def completar_envio(self) -> None:
        """Marca la transferencia como completada."""
        self.estado = "completado"
        self.tiempo_fin = time.time()
        self.libro.cambiar_estado("disponible")
        
        tiempo_real = self.tiempo_fin - self.tiempo_inicio if self.tiempo_inicio else 0
        print(f"Transferencia completada: {self.libro.titulo}")
        print(f"Tiempo total: {tiempo_real:.2f} segundos")

    def obtener_progreso(self) -> float:
        """Retorna el porcentaje de progreso (0.0 a 1.0)."""
        if not self.ruta:
            return 0.0
        return self.indice_actual / (len(self.ruta) - 1)

    def obtener_nodo_actual(self) -> Optional[str]:
        """Retorna el nodo actual en la ruta."""
        if not self.ruta or self.indice_actual >= len(self.ruta):
            return None
        return self.ruta[self.indice_actual]

    def obtener_siguiente_nodo(self) -> Optional[str]:
        """Retorna el siguiente nodo en la ruta."""
        if not self.ruta or self.indice_actual >= len(self.ruta) - 1:
            return None
        return self.ruta[self.indice_actual + 1]

    def cancelar_envio(self) -> None:
        """Cancela la transferencia."""
        self.estado = "cancelado"
        self.libro.cambiar_estado("disponible")
        print(f"Transferencia cancelada: {self.libro.titulo}")

    def obtener_tiempo_restante(self) -> int:
        """Calcula el tiempo restante estimado en segundos."""
        if self.estado != "en_proceso" or not self.tiempo_inicio:
            return 0
        
        tiempo_transcurrido = time.time() - self.tiempo_inicio
        tiempo_restante = max(0, self.eta_segundos - int(tiempo_transcurrido))
        return tiempo_restante

    def __str__(self) -> str:
        progreso = int(self.obtener_progreso() * 100)
        return (f"Transferencia({self.libro.titulo}, {self.origen}->{self.destino}, "
                f"{self.estado}, {progreso}%)")