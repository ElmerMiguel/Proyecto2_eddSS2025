from objetos.libro import Libro
from typing import Optional

class NodoCola:
    def __init__(self, libro: Libro):
        self.libro = libro
        self.siguiente: Optional['NodoCola'] = None

class Cola:
    def __init__(self):
        self.frente: Optional[NodoCola] = None
        self.final: Optional[NodoCola] = None
        self.tamanio = 0

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
            print("Cola vacia")
            return
        actual = self.frente
        print(f"\nCola ({self.tamanio} elementos):")
        print("=" * 80)
        while actual:
            print(f"-> {actual.libro.titulo} ({actual.libro.isbn})")
            actual = actual.siguiente
        print("=" * 80)