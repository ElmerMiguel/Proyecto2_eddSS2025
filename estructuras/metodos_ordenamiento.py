from typing import List, Tuple
from objetos.libro import Libro
import time

def medir_tiempo(func, libros: List[Libro], clave: str) -> Tuple[List[Libro], float]:
    inicio = time.perf_counter()
    resultado = func(libros.copy(), clave)
    fin = time.perf_counter()
    return resultado, fin - inicio

def burbuja(libros: List[Libro], clave="titulo") -> List[Libro]:
    n = len(libros)
    for i in range(n):
        for j in range(0, n - i - 1):
            if getattr(libros[j], clave) > getattr(libros[j + 1], clave):
                libros[j], libros[j + 1] = libros[j + 1], libros[j]
    return libros

def seleccion(libros: List[Libro], clave="titulo") -> List[Libro]:
    n = len(libros)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if getattr(libros[j], clave) < getattr(libros[min_idx], clave):
                min_idx = j
        libros[i], libros[min_idx] = libros[min_idx], libros[i]
    return libros

def insercion(libros: List[Libro], clave="titulo") -> List[Libro]:
    for i in range(1, len(libros)):
        key = libros[i]
        j = i - 1
        while j >= 0 and getattr(libros[j], clave) > getattr(key, clave):
            libros[j + 1] = libros[j]
            j -= 1
        libros[j + 1] = key
    return libros

def shell_sort(libros: List[Libro], clave="titulo") -> List[Libro]:
    n = len(libros)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = libros[i]
            j = i
            while j >= gap and getattr(libros[j - gap], clave) > getattr(temp, clave):
                libros[j] = libros[j - gap]
                j -= gap
            libros[j] = temp
        gap //= 2
    return libros

def quick_sort(libros: List[Libro], clave="titulo") -> List[Libro]:
    if len(libros) <= 1:
        return libros
    # Elegir el pivote
    pivote = libros[len(libros) // 2]
    
    # Particionar la lista
    izq = [x for x in libros if getattr(x, clave) < getattr(pivote, clave)]
    centro = [x for x in libros if getattr(x, clave) == getattr(pivote, clave)]
    der = [x for x in libros if getattr(x, clave) > getattr(pivote, clave)]
    
    # Llamada recursiva
    return quick_sort(izq, clave) + centro + quick_sort(der, clave)

def comparar_metodos(libros: List[Libro], clave="titulo") -> str:
    
    metodos = {
        "Burbuja": burbuja,
        "Seleccion": seleccion,
        "Insercion": insercion,
        "Shell Sort": shell_sort,
        "QuickSort": quick_sort
    }
    
    lineas = []
    lineas.append(f"\nComparacion de metodos de ordenamiento por **{clave}**")
    lineas.append("=" * 60)
    lineas.append(f"{'METODO':<20}{'TIEMPO (segundos)':<25}{'ELEMENTOS'}")
    lineas.append("=" * 60)
    
    for nombre, metodo in metodos.items():
        _, tiempo = medir_tiempo(metodo, libros, clave)
        lineas.append(f"{nombre:<20}{tiempo:<25.6f}{len(libros)}")
    
    lineas.append("=" * 60)
    
    reporte = "\n".join(lineas)
    print(reporte) 
    return reporte