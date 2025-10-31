class Libro:
    def __init__(self, titulo="", isbn="", genero="", anio=0, autor="", 
                 estado="disponible", biblioteca_origen="", biblioteca_destino="", prioridad="tiempo"):
        
        if not titulo or not autor or not genero:
            raise ValueError("Titulo, autor y genero son obligatorios")
        
        if not self._validar_isbn(isbn):
            raise ValueError(f"ISBN invalido: {isbn}")
        
        if anio < 1000 or anio > 2025:
            raise ValueError(f"Año debe estar entre 1000 y 2025, recibido: {anio}")
        
        self.titulo = titulo
        self.isbn = isbn
        self.genero = genero
        self.anio = anio
        self.autor = autor
        self.estado = estado
        self.biblioteca_origen = biblioteca_origen
        self.biblioteca_destino = biblioteca_destino
        self.prioridad = prioridad

    def _validar_isbn(self, isbn: str) -> bool:
        """Valida que el ISBN tenga exactamente 13 dígitos numéricos"""
        isbn_limpio = "".join(ch for ch in isbn if ch.isdigit())
        if len(isbn_limpio) != 13:
            return False
        return isbn_limpio.isdigit()

    def cambiar_estado(self, nuevo_estado: str):
        estados_validos = ["disponible", "en_transito", "prestado", "agotado"]
        if nuevo_estado in estados_validos:
            self.estado = nuevo_estado
        else:
            raise ValueError(f"Estado invalido: {nuevo_estado}")

    def __str__(self):
        return (f"{self.titulo} ({self.anio}) - {self.autor} [{self.genero}] | "
                f"ISBN: {self.isbn} | Estado: {self.estado} | "
                f"Origen: {self.biblioteca_origen} -> Destino: {self.biblioteca_destino} | "
                f"Prioridad: {self.prioridad}")
