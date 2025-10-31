from objetos.libro import Libro
from typing import Optional

class NodoPila:
    def __init__(self, libro: Libro):
        self.libro = libro
        self.siguiente: Optional['NodoPila'] = None

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

    def esta_vacia(self) -> bool:
        return self.tope is None

    def ver_tope(self) -> Optional[Libro]:
        return self.tope.libro if self.tope else None

    def listar(self):
        if self.esta_vacia():
            print("Pila vacia")
            return
        actual = self.tope
        print(f"\nPila ({self.tamanio} elementos):")
        print("=" * 80)
        while actual:
            print(f"-> {actual.libro.titulo} ({actual.libro.isbn})")
            actual = actual.siguiente
        print("=" * 80)