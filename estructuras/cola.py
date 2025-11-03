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
        self.tipo = tipo

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