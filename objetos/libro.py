# archivo: objetos/libro.py

class Libro:
    """
    Clase que representa un libro dentro de la biblioteca.
    """

    def __init__(self, titulo="", isbn="", genero="", anio=0, autor=""):
        self.titulo = titulo
        self.isbn = isbn
        self.genero = genero
        self.anio = anio
        self.autor = autor

    def __str__(self):
        """
        Retorna una representación legible del libro.
        """
        return f"{self.titulo} ({self.anio}) - {self.autor} [{self.genero}] | ISBN: {self.isbn}"
