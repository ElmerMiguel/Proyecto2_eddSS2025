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
        self.apilar(libro)

    def pop(self) -> Optional[Libro]:
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
    
    def exportar_dot(self, nombre_archivo: str) -> None:
        with open(nombre_archivo, 'w') as archivo:
            archivo.write("digraph Pila {\n")
            archivo.write("    rankdir=TB;\n")
            archivo.write("    node [shape=rectangle, style=filled, fillcolor=lightcoral];\n")
            
            if self.esta_vacia():
                archivo.write("    vacio [label=\"Pila vacía\"];\n")
            else:
                actual = self.tope
                contador = 0
                
                while actual:
                    # Mostrar tipo de operación si es un dict
                    if hasattr(actual.data, 'get') and 'tipo' in actual.data:
                        label = f"{actual.data['tipo'].capitalize()}"
                    else:
                        label = f"Operación {contador + 1}"
                    
                    archivo.write(f"    nodo{contador} [label=\"{label}\"];\n")
                    if actual.siguiente:
                        archivo.write(f"    nodo{contador} -> nodo{contador+1};\n")
                    actual = actual.siguiente
                    contador += 1
            
            archivo.write("}\n")