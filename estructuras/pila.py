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