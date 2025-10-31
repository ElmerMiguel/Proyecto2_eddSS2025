class Libro:
    def __init__(self, titulo="", isbn="", genero="", anio=0, autor="", estado="disponible"):
        self.titulo = titulo
        self.isbn = isbn
        self.genero = genero
        self.anio = anio
        self.autor = autor
        self.estado = estado  # disponible, en_transito, prestado, agotado

    def cambiar_estado(self, nuevo_estado: str):
        estados_validos = ["disponible", "en_transito", "prestado", "agotado"]
        if nuevo_estado in estados_validos:
            self.estado = nuevo_estado
        else:
            raise ValueError(f"Estado invalido: {nuevo_estado}")

    def __str__(self):
        return f"{self.titulo} ({self.anio}) - {self.autor} [{self.genero}] | ISBN: {self.isbn} | Estado: {self.estado}"