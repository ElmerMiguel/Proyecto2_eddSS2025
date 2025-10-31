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

    def cargar_bibliotecas_csv(self, ruta_archivo: str) -> int:
        """
        Carga bibliotecas desde CSV.
        Formato esperado: ID,Nombre,Ubicacion,t_ingreso,t_traspaso,i_despacho
        Retorna el numero de bibliotecas cargadas.
        """
        if not os.path.exists(ruta_archivo):
            print(f"Error: No se encontro el archivo {ruta_archivo}")
            return 0
        
        contador = 0
        
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                
                for fila in lector:
                    id_bib = fila['ID'].strip()
                    nombre = fila['Nombre'].strip()
                    ubicacion = fila['Ubicacion'].strip()
                    t_ingreso = int(fila['t_ingreso'])
                    t_traspaso = int(fila['t_traspaso'])
                    i_despacho = int(fila['i_despacho'])
                    
                    biblioteca = Biblioteca(
                        id_biblioteca=id_bib,
                        nombre=nombre,
                        ubicacion=ubicacion,
                        tiempo_ingreso=t_ingreso,
                        tiempo_traspaso=t_traspaso,
                        intervalo_despacho=i_despacho
                    )
                    
                    self.bibliotecas[id_bib] = biblioteca
                    self.inventario_global.agregar_biblioteca(id_bib)  # ← Línea agregada
                    self.grafo.agregar_nodo(id_bib)
                
                    contador += 1
            
            print(f"Se cargaron {contador} bibliotecas desde {ruta_archivo}")
            return contador
        
        except Exception as e:
            print(f"Error al cargar bibliotecas: {e}")
            return contador


    def cargar_conexiones_csv(self, ruta_archivo: str) -> int:
        """
        Carga conexiones (aristas) desde CSV.
        Formato esperado: Origen,Destino,Tiempo,Costo,Bidireccional
        Retorna el numero de conexiones cargadas.
        """
        if not os.path.exists(ruta_archivo):
            print(f"Error: No se encontro el archivo {ruta_archivo}")
            return 0
        
        contador = 0
        
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                
                for fila in lector:
                    origen = fila['Origen'].strip()
                    destino = fila['Destino'].strip()
                    tiempo = int(fila['Tiempo'])
                    costo = float(fila['Costo'])
                    bidireccional = fila['Bidireccional'].strip().lower() == 'true'
                    
                    if origen not in self.bibliotecas or destino not in self.bibliotecas:
                        print(f"Advertencia: Conexion invalida {origen}->{destino}")
                        continue
                    
                    self.grafo.agregar_arista(origen, destino, tiempo, costo, bidireccional)
                    contador += 1
            
            print(f"Se cargaron {contador} conexiones desde {ruta_archivo}")
            return contador
            
        except Exception as e:
            print(f"Error al cargar conexiones: {e}")
            return contador

    def iniciar_transferencia(self, isbn: str, origen: str, destino: str, prioridad: str = "tiempo") -> bool:
        """
        Inicia una transferencia de libro entre bibliotecas.
        Busca el libro en el catalogo de origen, calcula ruta y lo encola para envio.
        """
        if origen not in self.bibliotecas:
            print(f"Error: Biblioteca origen '{origen}' no existe")
            return False
        
        if destino not in self.bibliotecas:
            print(f"Error: Biblioteca destino '{destino}' no existe")
            return False
        
        biblioteca_origen = self.bibliotecas[origen]
        libro = biblioteca_origen.obtener_libro_por_isbn(isbn)
        
        if not libro:
            print(f"Error: Libro con ISBN '{isbn}' no encontrado en {origen}")
            return False
        
        if libro.estado != "disponible":
            print(f"Error: Libro '{libro.titulo}' no esta disponible (estado: {libro.estado})")
            return False
        
        transferencia = Transferencia(libro, origen, destino, prioridad)
        
        if not transferencia.calcular_ruta(self.grafo):
            return False
        
        transferencia.iniciar_envio()
        
        biblioteca_origen.eliminar_libro_catalogo(isbn)
        biblioteca_origen.cola_salida.encolar(libro)
        
        self.transferencias_activas.append(transferencia)
        
        return True

    def simular_tick(self) -> None:
        """
        Avanza la simulacion 1 tick (procesa colas y mueve transferencias).
        Debe llamarse periodicamente desde la GUI.
        """
        for biblioteca in self.bibliotecas.values():
            biblioteca.procesar_ingreso()
            biblioteca.procesar_traspaso()
            
            libro_despachado = biblioteca.procesar_salida()
            if libro_despachado:
                self._mover_libro_en_transito(libro_despachado, biblioteca.id)
        
        transferencias_a_remover = []
        for trans in self.transferencias_activas:
            if trans.estado == "completado":
                transferencias_a_remover.append(trans)
        
        for trans in transferencias_a_remover:
            self.transferencias_activas.remove(trans)
            self.transferencias_completadas.append(trans)

    def _mover_libro_en_transito(self, libro: Libro, biblioteca_actual: str) -> None:
        """Mueve un libro al siguiente nodo de su ruta."""
        for trans in self.transferencias_activas:
            if trans.libro.isbn == libro.isbn:
                siguiente_nodo = trans.avanzar_paso()
                
                if siguiente_nodo:
                    self.bibliotecas[siguiente_nodo].agregar_libro_ingreso(libro)
                else:
                    self.bibliotecas[trans.destino].agregar_libro_ingreso(libro)
                break

    def obtener_estado_biblioteca(self, id_biblioteca: str) -> Optional[dict]:
        """Retorna el estado completo de una biblioteca."""
        if id_biblioteca not in self.bibliotecas:
            return None
        
        return self.bibliotecas[id_biblioteca].obtener_estado_colas()

    def listar_bibliotecas(self) -> None:
        """Lista todas las bibliotecas de la red."""
        print("\n" + "=" * 80)
        print("BIBLIOTECAS EN LA RED")
        print("=" * 80)
        print(f"{'ID':<15}{'NOMBRE':<30}{'UBICACION'}")
        print("=" * 80)
        
        for bib in self.bibliotecas.values():
            print(f"{bib.id:<15}{bib.nombre:<30}{bib.ubicacion}")
        
        print("=" * 80)

    def listar_transferencias_activas(self) -> None:
        """Lista todas las transferencias en proceso."""
        print("\n" + "=" * 80)
        print(f"TRANSFERENCIAS ACTIVAS ({len(self.transferencias_activas)})")
        print("=" * 80)
        
        if not self.transferencias_activas:
            print("No hay transferencias activas")
        else:
            for trans in self.transferencias_activas:
                progreso = int(trans.obtener_progreso() * 100)
                tiempo_restante = trans.obtener_tiempo_restante()
                print(f"ISBN: {trans.libro.isbn} | {trans.libro.titulo}")
                print(f"  Ruta: {' -> '.join(trans.ruta)}")
                print(f"  Progreso: {progreso}% | Tiempo restante: {tiempo_restante}s")
                print("-" * 80)
        
        print("=" * 80)

    def exportar_red_completa(self, directorio: str = "graficas") -> None:
        """Exporta el grafo y todas las colas a archivos DOT."""
        os.makedirs(directorio, exist_ok=True)
        
        self.grafo.exportar_dot(f"{directorio}/red_bibliotecas.dot")
        
        for biblioteca in self.bibliotecas.values():
            biblioteca.exportar_colas_dot(directorio)
        
        print(f"Red completa exportada a {directorio}/")

    def obtener_estadisticas_red(self) -> dict:
        """Retorna estadisticas globales de la red."""
        total_libros = sum(
            bib.catalogo_local.tabla_isbn.cantidad 
            for bib in self.bibliotecas.values()
        )
        
        total_en_transito = sum(
            bib.cola_ingreso.tamanio + bib.cola_traspaso.tamanio + bib.cola_salida.tamanio
            for bib in self.bibliotecas.values()
        )
        
        return {
            "total_bibliotecas": len(self.bibliotecas),
            "total_conexiones": self.grafo.obtener_estadisticas()["aristas"],
            "total_libros_catalogados": total_libros,
            "total_en_transito": total_en_transito,
            "transferencias_activas": len(self.transferencias_activas),
            "transferencias_completadas": len(self.transferencias_completadas)
        }

    def mostrar_estadisticas_red(self) -> None:
        """Imprime estadisticas globales de la red."""
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
        
    def actualizar_inventario_libro(self, id_biblioteca: str, genero: str, incremento: int = 1):
        self.inventario_global.incrementar(id_biblioteca, genero, incremento)