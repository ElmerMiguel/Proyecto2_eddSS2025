class Libro:
    def __init__(self, titulo="", isbn="", genero="", anio=0, autor="", 
                 estado="disponible", biblioteca_origen="", biblioteca_destino="", prioridad="tiempo"):
        self.titulo = titulo
        self.isbn = self._validar_isbn(isbn)  # Agregar validación
        self.genero = genero
        self.anio = anio
        self.autor = autor
        self.estado = estado
        self.biblioteca_origen = biblioteca_origen
        self.biblioteca_destino = biblioteca_destino
        self.prioridad = prioridad

    def _validar_isbn(self, isbn):
        """Valida formato ISBN de 13 dígitos"""
        isbn_limpio = isbn.replace("-", "").replace(" ", "")
        if len(isbn_limpio) != 13 or not isbn_limpio.isdigit():
            raise ValueError(f"ISBN inválido: debe tener 13 dígitos. Recibido: {isbn}")
        return isbn_limpio

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