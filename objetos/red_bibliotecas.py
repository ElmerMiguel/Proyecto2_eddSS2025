from objetos.biblioteca import Biblioteca
from objetos.transferencia import Transferencia
from objetos.libro import Libro
from estructuras.grafo import Grafo
from objetos.inventario import Inventario
from typing import Dict, List, Optional
import csv
import os


class RedBibliotecas:
    """
    Controlador principal de la red de bibliotecas.
    Gestiona el grafo, las bibliotecas y las transferencias activas.
    """
    
    def __init__(self):
        self.grafo = Grafo()
        self.bibliotecas: Dict[str, Biblioteca] = {}
        self.transferencias_activas: List[Transferencia] = []
        self.transferencias_completadas: List[Transferencia] = []
        self.inventario_global = Inventario()

    # -------------------------------------------------
    # Utilidades internas
    # -------------------------------------------------
    def _registrar_biblioteca(self, biblioteca: Biblioteca) -> None:
        """Integra la biblioteca al grafo e inventario compartido."""
        biblioteca.set_inventario(self.inventario_global)
        self.bibliotecas[biblioteca.id] = biblioteca
        self.inventario_global.agregar_biblioteca(biblioteca.id)
        self.grafo.agregar_nodo(biblioteca.id, biblioteca.nombre)

    @staticmethod
    def _mapear_columnas(encabezado: List[str]) -> Dict[str, int]:
        """Crea un mapa columna -> indice en minusculas para acceso flexible."""
        return {col.strip().lower(): idx for idx, col in enumerate(encabezado)}

    @staticmethod
    def _leer_campo(fila: List[str], indice: int, por_defecto: str = "") -> str:
        if indice < 0 or indice >= len(fila):
            return por_defecto
        return fila[indice].strip().strip('"').strip()

    # -------------------------------------------------
    # Carga desde CSV
    # -------------------------------------------------
    def cargar_bibliotecas_csv(self, ruta_archivo: str) -> int:
        """
        Carga bibliotecas desde CSV.
        Formato esperado: id,nombre,ubicacion,tiempo_ingreso,tiempo_traspaso,intervalo_despacho
        """
        if not os.path.exists(ruta_archivo):
            print(f"Error: no se encontro el archivo {ruta_archivo}")
            return 0
        
        contador = 0
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                lector = csv.reader(archivo)
                encabezado = next(lector, None)
                if not encabezado:
                    print("Archivo de bibliotecas vacio.")
                    return 0
                
                for fila in lector:
                    if not fila or len(fila) < 6:
                        continue
                    
                    mapa = self._mapear_columnas(encabezado)
                    id_bib = self._leer_campo(fila, mapa.get("id", 0))
                    nombre = self._leer_campo(fila, mapa.get("nombre", 1))
                    ubicacion = self._leer_campo(fila, mapa.get("ubicacion", 2))
                    t_ingreso = int(self._leer_campo(fila, mapa.get("t_ingreso", 3), "10") or 10)
                    t_traspaso = int(self._leer_campo(fila, mapa.get("t_traspaso", 4), "5") or 5)
                    intervalo = int(self._leer_campo(fila, mapa.get("dispatchinterval", 5), "3") or 3)
                    
                    biblioteca = Biblioteca(
                        id_biblioteca=id_bib,
                        nombre=nombre,
                        ubicacion=ubicacion,
                        tiempo_ingreso=t_ingreso,
                        tiempo_traspaso=t_traspaso,
                        intervalo_despacho=intervalo,
                        inventario=self.inventario_global
                    )
                    self._registrar_biblioteca(biblioteca)
                    contador += 1
            return contador
        except Exception as error:
            print(f"Error al cargar bibliotecas: {error}")
            return 0

    def cargar_conexiones_csv(self, ruta_archivo: str) -> int:
        """
        Carga conexiones desde CSV.
        Formato esperado: origen,destino,tiempo,costo
        """
        if not os.path.exists(ruta_archivo):
            print(f"Error: no se encontro el archivo {ruta_archivo}")
            return 0
        
        contador = 0
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                lector = csv.reader(archivo)
                encabezado = next(lector, None)
                if not encabezado:
                    print("Archivo de conexiones vacio.")
                    return 0
                
                for fila in lector:
                    if not fila or len(fila) < 4:
                        continue
                    
                    mapa = self._mapear_columnas(encabezado)
                    origen = self._leer_campo(fila, mapa.get("origenid", 0))
                    destino = self._leer_campo(fila, mapa.get("destinoid", 1))
                    tiempo = int(self._leer_campo(fila, mapa.get("tiempo", 2), "0") or 0)
                    costo = float(self._leer_campo(fila, mapa.get("costo", 3), "0") or 0.0)
                    
                    if origen not in self.bibliotecas or destino not in self.bibliotecas:
                        print(f"Conexion invalida: {origen} -> {destino}")
                        continue
                    
                    self.grafo.agregar_arista(origen, destino, tiempo, costo, bidireccional=True)
                    contador += 1
            return contador
        except Exception as error:
            print(f"Error al cargar conexiones: {error}")
            return 0

    def cargar_libros_csv(self, ruta_archivo: str) -> int:
        """
        Carga libros desde CSV y los asigna a las bibliotecas.
        Formato sugerido: titulo,isbn,genero,autor,anio,biblioteca_origen,biblioteca_destino,prioridad
        """
        if not os.path.exists(ruta_archivo):
            print(f"Error: no se encontro el archivo {ruta_archivo}")
            return 0
        
        if not self.bibliotecas:
            print("No hay bibliotecas registradas. Cargue bibliotecas primero.")
            return 0
        
        cargados = 0
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                lector = csv.reader(archivo)
                encabezado = next(lector, None)
                if not encabezado:
                    print("Archivo de libros vacio.")
                    return 0
                
                mapa = self._mapear_columnas(encabezado)
                for fila in lector:
                    if not fila or len(fila) < 4:
                        continue
                    
                    try:
                        titulo = self._leer_campo(fila, mapa.get("titulo", 0))
                        isbn = self._leer_campo(fila, mapa.get("isbn", 1))
                        genero = self._leer_campo(fila, mapa.get("genero", 2))
                        autor = self._leer_campo(fila, mapa.get("autor", 3))
                        anio = int(self._leer_campo(fila, mapa.get("anio", 4), "0") or 0)
                        origen = self._leer_campo(fila, mapa.get("biblioteca_origen", 5))
                        destino = self._leer_campo(fila, mapa.get("biblioteca_destino", 6))
                        prioridad = self._leer_campo(fila, mapa.get("prioridad", 7), "tiempo") or "tiempo"
                        
                        if not origen or origen not in self.bibliotecas:
                            print(f"Libro '{titulo}' omitido: biblioteca origen invalida")
                            continue
                        
                        libro = Libro(
                            titulo=titulo,
                            isbn=isbn,
                            genero=genero,
                            anio=anio,
                            autor=autor,
                            estado="disponible",
                            biblioteca_origen=origen,
                            biblioteca_destino=destino,
                            prioridad=prioridad
                        )
                        
                        biblioteca = self.bibliotecas[origen]
                        biblioteca.agregar_libro_catalogo(
                            libro,
                            registrar_rollback=False,
                            contar_ingreso=False
                        )
                        cargados += 1
                        
                        if destino and destino != origen:
                            self.programar_transferencia(isbn, origen, destino, prioridad)
                    except Exception as error:
                        print(f"Error al cargar libro desde fila {fila}: {error}")
                        continue
            return cargados
        except Exception as error:
            print(f"Error al cargar libros: {error}")
            return 0

    # -------------------------------------------------
    # Gestion de bibliotecas y conexiones manuales
    # -------------------------------------------------
    def agregar_biblioteca(self, id_bib: str, nombre: str, ubicacion: str, 
                           t_ingreso: int, t_traspaso: int, intervalo: int) -> None:
        """Agrega una biblioteca manualmente (desde GUI)."""
        biblioteca = Biblioteca(
            id_biblioteca=id_bib,
            nombre=nombre,
            ubicacion=ubicacion,
            tiempo_ingreso=t_ingreso,
            tiempo_traspaso=t_traspaso,
            intervalo_despacho=intervalo,
            inventario=self.inventario_global
        )
        self._registrar_biblioteca(biblioteca)
        print(f"Biblioteca '{nombre}' agregada con ID '{id_bib}'")
    
    def agregar_conexion(self, origen: str, destino: str, tiempo: int, costo: float, bidireccional: bool = True) -> bool:
        """Agrega una conexion al grafo de manera manual."""
        if origen not in self.bibliotecas or destino not in self.bibliotecas:
            print("No es posible crear la conexion: uno de los nodos no existe.")
            return False
        self.grafo.agregar_arista(origen, destino, tiempo, costo, bidireccional)
        return True

    # -------------------------------------------------
    # Transferencias
    # -------------------------------------------------
    def programar_transferencia(self, isbn: str, origen: str, destino: str, prioridad: str = "tiempo") -> bool:
        """Wrapper para compatibilidad con GUI."""
        return self.iniciar_transferencia(isbn, origen, destino, prioridad)

    def iniciar_transferencia(self, isbn: str, origen: str, destino: str, prioridad: str = "tiempo") -> bool:
        """
        Inicia una transferencia de libro entre bibliotecas.
        Busca el libro en el catalogo de origen, calcula ruta y lo encola para envio.
        """
        if origen not in self.bibliotecas:
            print(f"Biblioteca origen '{origen}' no existe.")
            return False
        
        if destino not in self.bibliotecas:
            print(f"Biblioteca destino '{destino}' no existe.")
            return False
        
        if origen == destino:
            print("La biblioteca origen y destino son iguales.")
            return False
        
        for trans in self.transferencias_activas:
            if trans.libro.isbn == isbn and trans.estado in ("pendiente", "planificado", "en_transito"):
                print(f"El libro con ISBN {isbn} ya tiene una transferencia activa.")
                return False
        
        biblioteca_origen = self.bibliotecas[origen]
        libro = biblioteca_origen.obtener_libro_por_isbn(isbn)
        
        if not libro:
            print(f"Libro con ISBN '{isbn}' no encontrado en {origen}.")
            return False
        
        if libro.estado != "disponible":
            print(f"Libro '{libro.titulo}' no esta disponible (estado: {libro.estado}).")
            return False
        
        transferencia = Transferencia(libro, origen, destino, prioridad)
        if not transferencia.calcular_ruta(self.grafo):
            print("No se encontro ruta para la transferencia.")
            return False
        
        transferencia.iniciar_envio()
        libro.biblioteca_destino = destino
        biblioteca_origen.eliminar_libro_catalogo(isbn)
        biblioteca_origen.cola_salida.encolar(libro)
        self.transferencias_activas.append(transferencia)
        
        print(f"Transferencia programada: {libro.titulo} ({isbn}) {origen} -> {destino}")
        return True

    def solicitar_transferencia(self, libro: Libro, id_origen: str, id_destino: str, criterio: str = "tiempo") -> bool:
        """
        Solicita una transferencia usando un objeto Libro directamente.
        (Usado cuando se carga desde CSV).
        """
        if id_origen not in self.bibliotecas or id_destino not in self.bibliotecas:
            print("Biblioteca origen o destino no existe.")
            return False
        
        biblioteca_origen = self.bibliotecas[id_origen]
        existente = biblioteca_origen.obtener_libro_por_isbn(libro.isbn)
        if not existente:
            biblioteca_origen.agregar_libro_catalogo(libro, registrar_rollback=False, contar_ingreso=False)
        return self.iniciar_transferencia(libro.isbn, id_origen, id_destino, criterio)

    # -------------------------------------------------
    # Simulacion
    # -------------------------------------------------
    def simular_tick(self) -> None:
        """Avanza la simulacion un tick procesando colas y transferencias."""
        despachados: List[Libro] = []
        for biblioteca in self.bibliotecas.values():
            biblioteca.procesar_ingreso()
            biblioteca.procesar_traspaso()
            libro = biblioteca.procesar_salida()
            if libro:
                despachados.append((libro, biblioteca.id))
        
        for libro, origen in despachados:
            self._mover_libro_en_transito(libro, origen)
        
        finalizadas = [trans for trans in self.transferencias_activas if trans.estado == "completado"]
        for trans in finalizadas:
            self.transferencias_activas.remove(trans)
            self.transferencias_completadas.append(trans)

    def _mover_libro_en_transito(self, libro: Libro, biblioteca_actual: str) -> None:
        """Mueve un libro al siguiente nodo de su ruta."""
        for trans in self.transferencias_activas:
            if trans.libro.isbn == libro.isbn:
                siguiente = trans.avanzar_paso()
                if siguiente:
                    self.bibliotecas[siguiente].agregar_libro_ingreso(libro)
                else:
                    destino = trans.destino
                    self.bibliotecas[destino].agregar_libro_ingreso(libro)
                break

    # -------------------------------------------------
    # Consultas y reportes
    # -------------------------------------------------
    def obtener_estado_biblioteca(self, id_biblioteca: str) -> Optional[dict]:
        if id_biblioteca not in self.bibliotecas:
            return None
        return self.bibliotecas[id_biblioteca].obtener_estado_colas()

    def listar_bibliotecas(self) -> None:
        print("\n" + "=" * 80)
        print("BIBLIOTECAS EN LA RED")
        print("=" * 80)
        print(f"{'ID':<15}{'NOMBRE':<30}{'UBICACION'}")
        print("=" * 80)
        for bib in self.bibliotecas.values():
            print(f"{bib.id:<15}{bib.nombre:<30}{bib.ubicacion}")
        print("=" * 80)

    def listar_transferencias_activas(self) -> None:
        print("\n" + "=" * 80)
        print(f"TRANSFERENCIAS ACTIVAS ({len(self.transferencias_activas)})")
        print("=" * 80)
        if not self.transferencias_activas:
            print("No hay transferencias activas.")
        else:
            for trans in self.transferencias_activas:
                progreso = int(trans.obtener_progreso() * 100)
                restante = trans.obtener_tiempo_restante()
                ruta = " -> ".join(trans.ruta)
                print(f"{trans.libro.titulo} | ISBN: {trans.libro.isbn}")
                print(f"  Ruta: {ruta}")
                print(f"  Progreso: {progreso}% | Tiempo restante estimado: {restante}s")
                print("-" * 80)
        print("=" * 80)

    def exportar_red_completa(self, directorio: str = "graficas") -> None:
        os.makedirs(directorio, exist_ok=True)
        self.grafo.exportar_dot(f"{directorio}/red_bibliotecas.dot")
        for biblioteca in self.bibliotecas.values():
            biblioteca.exportar_colas_dot(directorio)
        print(f"Datos exportados en {directorio}/")

    def obtener_estadisticas_red(self) -> dict:
        total_libros = sum(bib.catalogo_local.tabla_isbn.cantidad for bib in self.bibliotecas.values())
        total_en_transito = sum(
            bib.cola_ingreso.tamanio + bib.cola_traspaso.tamanio + bib.cola_salida.tamanio
            for bib in self.bibliotecas.values()
        )
        graf_stats = self.grafo.obtener_estadisticas() if hasattr(self.grafo, "obtener_estadisticas") else {"aristas": 0}
        return {
            "total_bibliotecas": len(self.bibliotecas),
            "total_conexiones": graf_stats.get("aristas", 0),
            "total_libros_catalogados": total_libros,
            "total_en_transito": total_en_transito,
            "transferencias_activas": len(self.transferencias_activas),
            "transferencias_completadas": len(self.transferencias_completadas)
        }

    def mostrar_estadisticas_red(self) -> None:
        stats = self.obtener_estadisticas_red()
        print("\n" + "=" * 80)
        print("ESTADISTICAS DE LA RED COMPLETA")
        print("=" * 80)
        print(f"Total de bibliotecas:           {stats['total_bibliotecas']}")
        print(f"Total de conexiones:            {stats['total_conexiones']}")
        print(f"Libros catalogados:             {stats['total_libros_catalogados']}")
        print(f"Libros en transito:             {stats['total_en_transito']}")
        print(f"Transferencias activas:         {stats['transferencias_activas']}")
        print(f"Transferencias completadas:     {stats['transferencias_completadas']}")
        print("=" * 80)

    # -------------------------------------------------
    # Inventario global
    # -------------------------------------------------
    def actualizar_inventario_libro(self, id_biblioteca: str, genero: str, incremento: int = 1):
        self.inventario_global.incrementar(id_biblioteca, genero, incremento)