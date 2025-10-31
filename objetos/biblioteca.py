from objetos.controlador_catalogo import ControladorCatalogo
from objetos.libro import Libro
from estructuras.cola import Cola
from estructuras.pila import Pila
from estructuras.metodos_ordenamiento import comparar_metodos
from typing import Optional, List
import time


class Biblioteca:
    """
    Representa un nodo del grafo (biblioteca individual).
    Cada biblioteca tiene su propio catalogo y 3 colas de procesamiento.
    """
    
    def __init__(self, id_biblioteca: str, nombre: str, ubicacion: str, 
                 tiempo_ingreso: int = 10, tiempo_traspaso: int = 5, intervalo_despacho: int = 3):
        self.id = id_biblioteca
        self.nombre = nombre
        self.ubicacion = ubicacion
        
        self.tiempo_ingreso = tiempo_ingreso
        self.tiempo_traspaso = tiempo_traspaso
        self.intervalo_despacho = intervalo_despacho
        
        self.cola_ingreso = Cola(tipo="ingreso")
        self.cola_traspaso = Cola(tipo="traspaso")
        self.cola_salida = Cola(tipo="salida")
        
        self.catalogo_local = ControladorCatalogo()
        
        self.pila_rollback = Pila()
        
        self.ultimo_despacho = time.time()
        
        self.estadisticas = {
            "libros_ingresados": 0,
            "libros_enviados": 0,
            "libros_recibidos": 0,
            "tiempo_total_procesamiento": 0
        }

    def agregar_libro_ingreso(self, libro: Libro) -> None:
        """Agrega un libro a la cola de ingreso."""
        libro.cambiar_estado("en_transito")
        self.cola_ingreso.encolar(libro)
        print(f"Libro '{libro.titulo}' agregado a cola de ingreso de {self.nombre}")

    def procesar_ingreso(self) -> bool:
        """
        Procesa un libro de la cola de ingreso.
        Decide si va al catalogo local o a la cola de traspaso.
        Retorna True si proceso algo, False si la cola estaba vacia.
        """
        if self.cola_ingreso.esta_vacia():
            return False
        
        libro = self.cola_ingreso.desencolar()
        
        time.sleep(self.tiempo_ingreso / 1000)
        
        if libro.biblioteca_destino == self.id or not libro.biblioteca_destino:
            libro.cambiar_estado("disponible")
            self.catalogo_local.agregar_libro(libro)
            self.estadisticas["libros_ingresados"] += 1
            self.pila_rollback.apilar(libro)
            print(f"Libro '{libro.titulo}' agregado al catalogo de {self.nombre}")
        else:
            libro.cambiar_estado("en_transito")
            self.cola_traspaso.encolar(libro)
            print(f"Libro '{libro.titulo}' movido a cola de traspaso en {self.nombre}")
        
        return True

    def procesar_traspaso(self) -> bool:
        """
        Prepara un libro para ser enviado (cola traspaso -> cola salida).
        Retorna True si proceso algo, False si la cola estaba vacia.
        """
        if self.cola_traspaso.esta_vacia():
            return False
        
        libro = self.cola_traspaso.desencolar()
        
        time.sleep(self.tiempo_traspaso / 1000)
        
        self.cola_salida.encolar(libro)
        print(f"Libro '{libro.titulo}' preparado para envio desde {self.nombre}")
        
        return True

    def procesar_salida(self) -> Optional[Libro]:
        """
        Despacha un libro si ha pasado el intervalo de despacho.
        Retorna el libro despachado o None si no se puede despachar.
        """
        tiempo_actual = time.time()
        
        if (tiempo_actual - self.ultimo_despacho) < self.intervalo_despacho:
            return None
        
        if self.cola_salida.esta_vacia():
            return None
        
        libro = self.cola_salida.desencolar()
        self.ultimo_despacho = tiempo_actual
        self.estadisticas["libros_enviados"] += 1
        
        print(f"Libro '{libro.titulo}' despachado desde {self.nombre}")
        return libro

    def obtener_libro_por_isbn(self, isbn: str) -> Optional[Libro]:
        """Busca un libro en el catalogo local por ISBN."""
        return self.catalogo_local.buscar_por_isbn(isbn)

    def eliminar_libro_catalogo(self, isbn: str) -> bool:
        """Elimina un libro del catalogo local."""
        libro = self.obtener_libro_por_isbn(isbn)
        if libro:
            self.catalogo_local.eliminar_libro(isbn)
            return True
        return False

    def rollback_ultimo_ingreso(self) -> Optional[Libro]:
        """Deshace el ultimo libro ingresado al catalogo."""
        if self.pila_rollback.esta_vacia():
            print("No hay operaciones para deshacer")
            return None
        
        libro = self.pila_rollback.desapilar()
        self.catalogo_local.eliminar_libro(libro.isbn)
        print(f"Se deshizo el ingreso de '{libro.titulo}'")
        return libro

    def ordenar_catalogo(self, metodo: str = "quick_sort", clave: str = "titulo") -> None:
        """
        Ordena el catalogo local usando uno de los 5 metodos.
        metodo: "burbuja", "seleccion", "insercion", "shell_sort", "quick_sort"
        """
        from estructuras.metodos_ordenamiento import burbuja, seleccion, insercion, shell_sort, quick_sort
        
        metodos = {
            "burbuja": burbuja,
            "seleccion": seleccion,
            "insercion": insercion,
            "shell_sort": shell_sort,
            "quick_sort": quick_sort
        }
        
        if metodo not in metodos:
            print(f"Metodo invalido: {metodo}")
            return
        
        libros_lista = []
        actual = self.catalogo_local.lista_secuencial.cabeza
        while actual:
            libros_lista.append(actual.data)
            actual = actual.siguiente
        
        libros_ordenados = metodos[metodo](libros_lista, clave)
        
        print(f"Catalogo de {self.nombre} ordenado por {clave} usando {metodo}")
        for libro in libros_ordenados:
            print(f"  - {getattr(libro, clave)}: {libro.titulo}")

    def comparar_metodos_ordenamiento(self, clave: str = "titulo") -> None:
        """Compara los 5 metodos de ordenamiento en el catalogo local."""
        libros_lista = []
        actual = self.catalogo_local.lista_secuencial.cabeza
        while actual:
            libros_lista.append(actual.data)
            actual = actual.siguiente
        
        if not libros_lista:
            print(f"El catalogo de {self.nombre} esta vacio")
            return
        
        print(f"\nComparacion de metodos para biblioteca: {self.nombre}")
        comparar_metodos(libros_lista, clave)

    def obtener_estado_colas(self) -> dict:
        """Retorna el estado actual de las 3 colas."""
        return {
            "ingreso": {
                "cantidad": self.cola_ingreso.tamanio,
                "frente": self.cola_ingreso.ver_frente().titulo if not self.cola_ingreso.esta_vacia() else None
            },
            "traspaso": {
                "cantidad": self.cola_traspaso.tamanio,
                "frente": self.cola_traspaso.ver_frente().titulo if not self.cola_traspaso.esta_vacia() else None
            },
            "salida": {
                "cantidad": self.cola_salida.tamanio,
                "frente": self.cola_salida.ver_frente().titulo if not self.cola_salida.esta_vacia() else None
            }
        }

    def mostrar_estado(self) -> None:
        """Imprime el estado completo de la biblioteca."""
        print("\n" + "=" * 80)
        print(f"ESTADO DE BIBLIOTECA: {self.nombre} ({self.id})")
        print("=" * 80)
        print(f"Ubicacion: {self.ubicacion}")
        print(f"Tiempo ingreso: {self.tiempo_ingreso}s | Tiempo traspaso: {self.tiempo_traspaso}s | Intervalo despacho: {self.intervalo_despacho}s")
        print("\nESTADISTICAS:")
        print(f"  Libros ingresados: {self.estadisticas['libros_ingresados']}")
        print(f"  Libros enviados: {self.estadisticas['libros_enviados']}")
        print(f"  Libros recibidos: {self.estadisticas['libros_recibidos']}")
        print("\nESTADO DE COLAS:")
        estado = self.obtener_estado_colas()
        print(f"  Cola Ingreso: {estado['ingreso']['cantidad']} libros")
        print(f"  Cola Traspaso: {estado['traspaso']['cantidad']} libros")
        print(f"  Cola Salida: {estado['salida']['cantidad']} libros")
        print("=" * 80)

    def exportar_colas_dot(self, directorio: str = "graficas") -> None:
        """Exporta las 3 colas a archivos DOT."""
        import os
        os.makedirs(directorio, exist_ok=True)
        
        self.cola_ingreso.exportar_dot(f"{directorio}/{self.id}_cola_ingreso.dot")
        self.cola_traspaso.exportar_dot(f"{directorio}/{self.id}_cola_traspaso.dot")
        self.cola_salida.exportar_dot(f"{directorio}/{self.id}_cola_salida.dot")

    def __str__(self) -> str:
        return f"Biblioteca({self.id}, {self.nombre}, {self.ubicacion})"