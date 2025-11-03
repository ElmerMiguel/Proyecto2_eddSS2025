from objetos.controlador_catalogo import ControladorCatalogo
from objetos.libro import Libro
from objetos.inventario import Inventario
from estructuras.cola import Cola
from estructuras.pila import Pila
from estructuras.metodos_ordenamiento import comparar_metodos
from typing import Optional, List
import time


class Biblioteca:
    
    def __init__(self, id_biblioteca: str, nombre: str, ubicacion: str, 
                 tiempo_ingreso: int = 10, tiempo_traspaso: int = 5, intervalo_despacho: int = 3,
                 inventario: Optional[Inventario] = None):
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
        self.inventario = inventario
        
        self.pila_rollback = Pila()
        
        self.ultimo_despacho = time.time()
        
        self.estadisticas = {
            "libros_ingresados": 0,
            "libros_enviados": 0,
            "libros_recibidos": 0,
            "tiempo_total_procesamiento": 0.0
        }

    def set_inventario(self, inventario: Inventario) -> None:
        self.inventario = inventario

    def _actualizar_inventario(self, libro: Libro, delta: int) -> None:
        if not self.inventario:
            return
        genero = libro.genero if libro.genero else "SinGenero"
        if delta > 0:
            self.inventario.incrementar(self.id, genero, delta)
        elif delta < 0:
            self.inventario.decrementar(self.id, genero, abs(delta))

    def agregar_libro_catalogo(self, libro: Libro, registrar_rollback: bool = True, contar_ingreso: bool = True) -> None:
        libro.biblioteca_origen = libro.biblioteca_origen or self.id
        if not libro.biblioteca_destino:
            libro.biblioteca_destino = self.id
        libro.cambiar_estado("disponible")
        
        self.catalogo_local.agregar_libro(libro)
        
        self._actualizar_inventario(libro, 1)
        if registrar_rollback:
            operacion = {"tipo": "agregar", "libro": libro}
            self.pila_rollback.apilar(operacion)
        if contar_ingreso:
            self.estadisticas["libros_ingresados"] += 1

    def actualizar_libro(self, isbn: str, nuevos_datos: dict, registrar_rollback: bool = True) -> bool:
        libro_original = self.obtener_libro_por_isbn(isbn)
        if not libro_original:
            return False

        libro_anterior = libro_original.copy()
        genero_anterior = libro_original.genero

        libro_modificado = self.catalogo_local.actualizar_libro(isbn, nuevos_datos)

        if libro_modificado:
            genero_nuevo = libro_modificado.genero
            
            if genero_anterior != genero_nuevo:
                self._actualizar_inventario(Libro(isbn=isbn, genero=genero_anterior, titulo="", autor=""), -1)
                self._actualizar_inventario(libro_modificado, 1)

            if registrar_rollback:
                operacion = {
                    "tipo": "actualizar", 
                    "libro_anterior": libro_anterior,
                    "libro_nuevo": libro_modificado
                }
                self.pila_rollback.apilar(operacion)
            
            return True
        return False

    def agregar_libro_ingreso(self, libro: Libro) -> None:
        libro.cambiar_estado("en_transito")
        self.cola_ingreso.encolar(libro)

    def procesar_ingreso(self) -> bool:
        if self.cola_ingreso.esta_vacia():
            return False
        
        inicio = time.perf_counter()
        libro = self.cola_ingreso.desencolar()
        
        if libro.biblioteca_destino == self.id or not libro.biblioteca_destino:
            self.agregar_libro_catalogo(libro)
        else:
            libro.cambiar_estado("en_transito")
            self.cola_traspaso.encolar(libro)
        
        fin = time.perf_counter()
        self.estadisticas["tiempo_total_procesamiento"] += fin - inicio
        return True

    def procesar_traspaso(self) -> bool:
        if self.cola_traspaso.esta_vacia():
            return False
        
        inicio = time.perf_counter()
        libro = self.cola_traspaso.desencolar()
        self.cola_salida.encolar(libro)
        fin = time.perf_counter()
        self.estadisticas["tiempo_total_procesamiento"] += fin - inicio
        
        return True

    def procesar_salida(self) -> Optional[Libro]:
        tiempo_actual = time.time()
        
        if (tiempo_actual - self.ultimo_despacho) < self.intervalo_despacho:
            return None
        
        if self.cola_salida.esta_vacia():
            return None
        
        inicio = time.perf_counter()
        libro = self.cola_salida.desencolar()
        libro.cambiar_estado("en_transito")
        self.ultimo_despacho = tiempo_actual
        self.estadisticas["libros_enviados"] += 1
        fin = time.perf_counter()
        self.estadisticas["tiempo_total_procesamiento"] += fin - inicio
        
        return libro

    def registrar_recepcion(self, libro: Libro) -> None:
        libro.biblioteca_destino = self.id
        self.agregar_libro_catalogo(libro, registrar_rollback=True, contar_ingreso=False)
        self.estadisticas["libros_recibidos"] += 1

    def obtener_libro_por_isbn(self, isbn: str) -> Optional[Libro]:
        return self.catalogo_local.buscar_por_isbn(isbn)

    def eliminar_libro_catalogo(self, isbn: str) -> bool:
        libro = self.obtener_libro_por_isbn(isbn)
        if libro:
            operacion = {"tipo": "eliminar", "libro": libro}
            self.pila_rollback.apilar(operacion)
            
            self.catalogo_local.eliminar_libro(isbn)
            self._actualizar_inventario(libro, -1)
            return True
        return False

    def rollback_ultima_operacion(self) -> Optional[str]:
        if self.pila_rollback.esta_vacia():
            return "No hay operaciones para deshacer"
        
        operacion = self.pila_rollback.desapilar()
        
        if operacion["tipo"] == "agregar":
            libro = operacion["libro"]
            self.catalogo_local.eliminar_libro(libro.isbn)
            self._actualizar_inventario(libro, -1)
            return f"Se deshizo la agregación de '{libro.titulo}'"
            
        elif operacion["tipo"] == "eliminar":
            libro = operacion["libro"]
            self.catalogo_local.agregar_libro(libro)
            self._actualizar_inventario(libro, 1)
            return f"Se deshizo la eliminación de '{libro.titulo}'"

        elif operacion["tipo"] == "actualizar":
            libro_anterior = operacion["libro_anterior"]
            libro_modificado = operacion["libro_nuevo"]
            
            if libro_anterior.genero != libro_modificado.genero:
                self._actualizar_inventario(libro_modificado, -1)
                self._actualizar_inventario(libro_anterior, 1)
                
            datos_restauracion = {
                "titulo": libro_anterior.titulo,
                "autor": libro_anterior.autor,
                "genero": libro_anterior.genero,
                "anio": libro_anterior.anio,
                "biblioteca_origen": libro_anterior.biblioteca_origen,
                "biblioteca_destino": libro_anterior.biblioteca_destino,
                "estado": libro_anterior.estado,
            }
            self.catalogo_local.actualizar_libro(libro_anterior.isbn, datos_restauracion)
            return f"Se deshizo la actualización de '{libro_anterior.titulo}'"

    def ordenar_catalogo(self, metodo: str = "quick_sort", clave: str = "titulo") -> None:
        from estructuras.metodos_ordenamiento import burbuja, seleccion, insercion, shell_sort, quick_sort
        
        metodos = {
            "burbuja": burbuja,
            "seleccion": seleccion,
            "insercion": insercion,
            "shell_sort": shell_sort,
            "quick_sort": quick_sort
        }
        
        if metodo not in metodos:
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
        print("\n" + "=" * 80)
        print(f"ESTADO DE BIBLIOTECA: {self.nombre} ({self.id})")
        print("=" * 80)
        print(f"Ubicacion: {self.ubicacion}")
        print(f"Tiempo ingreso: {self.tiempo_ingreso}s | Tiempo traspaso: {self.tiempo_traspaso}s | Intervalo despacho: {self.intervalo_despacho}s")
        print("\nESTADISTICAS:")
        print(f"  Libros ingresados: {self.estadisticas['libros_ingresados']}")
        print(f"  Libros enviados: {self.estadisticas['libros_enviados']}")
        print(f"  Libros recibidos: {self.estadisticas['libros_recibidos']}")
        print(f"  Tiempo total procesamiento: {self.estadisticas['tiempo_total_procesamiento']:.4f}s")
        print("\nESTADO DE COLAS:")
        estado = self.obtener_estado_colas()
        print(f"  Cola Ingreso: {estado['ingreso']['cantidad']} libros")
        print(f"  Cola Traspaso: {estado['traspaso']['cantidad']} libros")
        print(f"  Cola Salida: {estado['salida']['cantidad']} libros")
        print("=" * 80)

    def exportar_colas_dot(self, directorio: str = "graficas") -> None:
        import os
        os.makedirs(directorio, exist_ok=True)
        
        self.cola_ingreso.exportar_dot(f"{directorio}/{self.id}_cola_ingreso.dot")
        self.cola_traspaso.exportar_dot(f"{directorio}/{self.id}_cola_traspaso.dot")
        self.cola_salida.exportar_dot(f"{directorio}/{self.id}_cola_salida.dot")
        
    def exportar_pila_dot(self, directorio: str = "graficas") -> None:
        import os
        os.makedirs(directorio, exist_ok=True)
        self.pila_rollback.exportar_dot(f"{directorio}/{self.id}_pila_rollback.dot")

    def __str__(self) -> str:
        return f"Biblioteca({self.id}, {self.nombre}, {self.ubicacion})"