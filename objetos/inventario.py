from typing import Dict, List, Optional


class Inventario:
    
    def __init__(self):
        self.bibliotecas: List[str] = []
        self.generos: List[str] = []
        self.matriz: List[List[int]] = []
        self.mapa_bibliotecas: Dict[str, int] = {}
        self.mapa_generos: Dict[str, int] = {}

    def agregar_biblioteca(self, id_biblioteca: str) -> None:
        if id_biblioteca in self.mapa_bibliotecas:
            print(f"Biblioteca '{id_biblioteca}' ya existe en el inventario")
            return
        
        self.bibliotecas.append(id_biblioteca)
        idx = len(self.bibliotecas) - 1
        self.mapa_bibliotecas[id_biblioteca] = idx
        
        self.matriz.append([0] * len(self.generos))
        
        print(f"Biblioteca '{id_biblioteca}' agregada al inventario")

    def agregar_genero(self, nombre_genero: str) -> None:
        if nombre_genero in self.mapa_generos:
            return
        
        self.generos.append(nombre_genero)
        idx = len(self.generos) - 1
        self.mapa_generos[nombre_genero] = idx
        
        for fila in self.matriz:
            fila.append(0)

    def incrementar(self, id_biblioteca: str, genero: str, cantidad: int = 1) -> None:
        if id_biblioteca not in self.mapa_bibliotecas:
            self.agregar_biblioteca(id_biblioteca)
        
        if genero not in self.mapa_generos:
            self.agregar_genero(genero)
        
        idx_bib = self.mapa_bibliotecas[id_biblioteca]
        idx_gen = self.mapa_generos[genero]
        
        self.matriz[idx_bib][idx_gen] += cantidad

    def decrementar(self, id_biblioteca: str, genero: str, cantidad: int = 1) -> bool:
        if id_biblioteca not in self.mapa_bibliotecas or genero not in self.mapa_generos:
            return False
        
        idx_bib = self.mapa_bibliotecas[id_biblioteca]
        idx_gen = self.mapa_generos[genero]
        
        if self.matriz[idx_bib][idx_gen] < cantidad:
            return False
        
        self.matriz[idx_bib][idx_gen] -= cantidad
        return True

    def obtener_cantidad(self, id_biblioteca: str, genero: str) -> int:
        if id_biblioteca not in self.mapa_bibliotecas or genero not in self.mapa_generos:
            return 0
        
        idx_bib = self.mapa_bibliotecas[id_biblioteca]
        idx_gen = self.mapa_generos[genero]
        
        return self.matriz[idx_bib][idx_gen]

    def obtener_total_por_genero(self, genero: str) -> int:
        if genero not in self.mapa_generos:
            return 0
        
        idx_gen = self.mapa_generos[genero]
        total = sum(fila[idx_gen] for fila in self.matriz)
        return total

    def obtener_total_por_biblioteca(self, id_biblioteca: str) -> int:
        if id_biblioteca not in self.mapa_bibliotecas:
            return 0
        
        idx_bib = self.mapa_bibliotecas[id_biblioteca]
        total = sum(self.matriz[idx_bib])
        return total

    def obtener_genero_mas_popular(self) -> Optional[str]:
        if not self.generos:
            return None
        
        totales = [self.obtener_total_por_genero(gen) for gen in self.generos]
        idx_max = totales.index(max(totales))
        return self.generos[idx_max]

    def obtener_biblioteca_mas_grande(self) -> Optional[str]:
        if not self.bibliotecas:
            return None
        
        totales = [self.obtener_total_por_biblioteca(bib) for bib in self.bibliotecas]
        idx_max = totales.index(max(totales))
        return self.bibliotecas[idx_max]

    def listar_generos(self) -> List[str]:
        return self.generos.copy()

    def listar_bibliotecas(self) -> List[str]:
        return self.bibliotecas.copy()

    def mostrar_inventario_completo(self) -> None:
        if not self.bibliotecas or not self.generos:
            print("Inventario vacío")
            return
        
        ancho_bib = max(len(bib) for bib in self.bibliotecas) + 2
        ancho_gen = 10
        
        print("\n" + "=" * (ancho_bib + ancho_gen * len(self.generos) + 5))
        print("INVENTARIO COMPLETO DE LA RED")
        print("=" * (ancho_bib + ancho_gen * len(self.generos) + 5))
        
        header = f"{'BIBLIOTECA':<{ancho_bib}}"
        for genero in self.generos:
            header += f"{genero[:9]:<{ancho_gen}}"
        header += f"{'TOTAL':<{ancho_gen}}"
        print(header)
        print("-" * (ancho_bib + ancho_gen * (len(self.generos) + 1)))
        
        for bib in self.bibliotecas:
            idx_bib = self.mapa_bibliotecas[bib]
            fila = f"{bib:<{ancho_bib}}"
            
            for genero in self.generos:
                idx_gen = self.mapa_generos[genero]
                cantidad = self.matriz[idx_bib][idx_gen]
                fila += f"{cantidad:<{ancho_gen}}"
            
            total_bib = self.obtener_total_por_biblioteca(bib)
            fila += f"{total_bib:<{ancho_gen}}"
            print(fila)
        
        print("-" * (ancho_bib + ancho_gen * (len(self.generos) + 1)))
        fila_total = f"{'TOTAL':<{ancho_bib}}"
        
        total_general = 0
        for genero in self.generos:
            total_gen = self.obtener_total_por_genero(genero)
            fila_total += f"{total_gen:<{ancho_gen}}"
            total_general += total_gen
        
        fila_total += f"{total_general:<{ancho_gen}}"
        print(fila_total)
        print("=" * (ancho_bib + ancho_gen * (len(self.generos) + 1)))

    def mostrar_inventario_biblioteca(self, id_biblioteca: str) -> None:
        if id_biblioteca not in self.mapa_bibliotecas:
            print(f"Biblioteca '{id_biblioteca}' no existe en el inventario")
            return
        
        idx_bib = self.mapa_bibliotecas[id_biblioteca]
        
        print(f"\n=== INVENTARIO DE '{id_biblioteca}' ===")
        print(f"{'GÉNERO':<30}{'CANTIDAD'}")
        print("-" * 40)
        
        for genero in self.generos:
            idx_gen = self.mapa_generos[genero]
            cantidad = self.matriz[idx_bib][idx_gen]
            if cantidad > 0:
                print(f"{genero:<30}{cantidad}")
        
        total = self.obtener_total_por_biblioteca(id_biblioteca)
        print("-" * 40)
        print(f"{'TOTAL':<30}{total}")
        print("=" * 40)

    def exportar_a_dict(self) -> Dict:
        return {
            "bibliotecas": self.bibliotecas,
            "generos": self.generos,
            "matriz": self.matriz
        }

    def importar_desde_dict(self, datos: Dict) -> None:
        self.bibliotecas = datos["bibliotecas"]
        self.generos = datos["generos"]
        self.matriz = datos["matriz"]
        
        self.mapa_bibliotecas = {bib: i for i, bib in enumerate(self.bibliotecas)}
        self.mapa_generos = {gen: i for i, gen in enumerate(self.generos)}

    def limpiar(self) -> None:
        self.bibliotecas.clear()
        self.generos.clear()
        self.matriz.clear()
        self.mapa_bibliotecas.clear()
        self.mapa_generos.clear()