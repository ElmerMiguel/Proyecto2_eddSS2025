from objetos.controlador_catalogo import ControladorCatalogo, Libro

class Menu:
    def __init__(self):
        self.bm = ControladorCatalogo()

    def ejecutar(self):
        while True:
            self.mostrar_menu_principal()
            opcion = self.leer_entero("Seleccione una opcion: ")

            if opcion == 1:
                self.submenu_gestion_libros()
            elif opcion == 2:
                self.submenu_busquedas()
            elif opcion == 3:
                self.submenu_comparaciones()
            elif opcion == 4:
                self.submenu_archivos()
            elif opcion == 0:
                print("\nCerrando sistema de biblioteca...")
                break
            else:
                print("Opcion no valida. Intente nuevamente.")

    def mostrar_menu_principal(self):
        self.mostrar_separador()
        print("               BIBLIOTECA MAGICA")
        self.mostrar_separador()
        print("1. Gestion de Libros")
        print("2. Busquedas Especializadas")
        print("3. Analisis de Rendimiento")
        print("4. Gestion de Archivos")
        print("0. Salir del Sistema")
        self.mostrar_separador()

    # -----------------------
    # Submenus
    # -----------------------
    def submenu_gestion_libros(self):
        while True:
            self.mostrar_separador()
            print("           GESTION DE LIBROS")
            self.mostrar_separador()
            print("1. Agregar nuevo libro")
            print("2. Eliminar libro por ISBN")
            print("3. Mostrar libros ordenados por titulo")
            print("0. Volver al menu principal")
            self.mostrar_separador()

            opcion = self.leer_entero("Seleccione una opcion: ")

            if opcion == 1:
                self.opcion_agregar()
            elif opcion == 2:
                self.opcion_eliminar()
            elif opcion == 3:
                self.opcion_mostrar_por_titulo()
            elif opcion == 0:
                break
            else:
                print("Opcion no valida.")

            if opcion != 0:
                self.pausar()

    def submenu_busquedas(self):
        while True:
            self.mostrar_separador()
            print("         BUSQUEDAS ESPECIALIZADAS")
            self.mostrar_separador()
            print("1. Buscar por titulo (Arbol AVL)")
            print("2. Buscar por ISBN (Tabla Hash)")
            print("3. Buscar por anio especifico (Arbol B)")
            print("4. Buscar por genero (Arbol B+)")
            print("5. Buscar por rango de fechas (Arbol B)")
            print("0. Volver al menu principal")
            self.mostrar_separador()

            opcion = self.leer_entero("Seleccione una opcion: ")

            if opcion == 1:
                self.opcion_buscar_titulo()
            elif opcion == 2:
                self.opcion_buscar_isbn()
            elif opcion == 3:
                self.opcion_buscar_fecha()
            elif opcion == 4:
                self.opcion_buscar_genero()
            elif opcion == 5:
                self.opcion_buscar_rango_fechas()
            elif opcion == 0:
                break
            else:
                print("Opcion no valida.")

            if opcion != 0:
                self.pausar()

    def submenu_comparaciones(self):
        while True:
            self.mostrar_separador()
            print("        ANALISIS DE RENDIMIENTO")
            self.mostrar_separador()
            print("1. Medir rendimiento de busquedas")
            print("2. Exportar graficos de arboles (DOT)")
            print("0. Volver al menu principal")
            self.mostrar_separador()

            opcion = self.leer_entero("Seleccione una opcion: ")

            if opcion == 1:
                self.opcion_medir_rendimiento()
            elif opcion == 2:
                self.opcion_exportar_arboles()
            elif opcion == 0:
                break
            else:
                print("Opcion no valida.")

            if opcion != 0:
                self.pausar()

    def submenu_archivos(self):
        while True:
            self.mostrar_separador()
            print("          GESTION DE ARCHIVOS")
            self.mostrar_separador()
            print("1. Cargar libros desde archivo CSV")
            print("0. Volver al menu principal")
            self.mostrar_separador()

            opcion = self.leer_entero("Seleccione una opcion: ")

            if opcion == 1:
                self.bm.cargar_desde_csv()
            elif opcion == 0:
                break
            else:
                print("Opcion no valida.")

            if opcion != 0:
                self.pausar()

    # -----------------------
    # Opciones del menú
    # -----------------------
    def opcion_agregar(self):
        self.mostrar_separador()
        print("         AGREGAR NUEVO LIBRO")
        self.mostrar_separador()

        titulo = input("Titulo: ").strip()
        isbn = input("ISBN: ").strip()
        genero = input("Genero: ").strip()
        while True:
            try:
                anio = int(input("Año de publicacion (1000-2025): "))
                if 1000 <= anio <= 2025:
                    break
            except ValueError:
                pass
            print("Ingrese un año valido entre 1000 y 2025")
        autor = input("Autor: ").strip()

        libro = Libro(titulo, isbn, genero, anio, autor)
        self.bm.agregar_libro(libro)

    def opcion_eliminar(self):
        self.mostrar_separador()
        print("         ELIMINAR LIBRO")
        self.mostrar_separador()
        self.bm.mostrar_resumen_libros()
        isbn = input("Ingrese ISBN del libro a eliminar: ").strip()
        self.bm.eliminar_libro(isbn)

    def opcion_mostrar_por_titulo(self):
        self.mostrar_separador()
        print("       MOSTRAR LIBROS ORDENADOS POR TITULO")
        self.mostrar_separador()
        self.bm.arbol_titulos.listar_titulos()

    def opcion_buscar_titulo(self):
        self.mostrar_separador()
        print("         BUSCAR POR TITULO")
        self.mostrar_separador()
        self.bm.mostrar_titulos_disponibles()
        titulo = input("Ingrese titulo a buscar: ").strip()
        libro = self.bm.buscar_por_titulo(titulo)
        if libro:
            print(f"\nLibro encontrado: {libro.titulo} - {libro.autor} - {libro.genero} - {libro.anio} - {libro.isbn}")
        else:
            print(f"\nNo se encontro el libro con titulo '{titulo}'.")

    def opcion_buscar_isbn(self):
        self.mostrar_separador()
        print("         BUSCAR POR ISBN")
        self.mostrar_separador()
        self.bm.mostrar_isbns_disponibles()
        isbn = input("Ingrese ISBN a buscar: ").strip()
        libro = self.bm.buscar_por_isbn(isbn)
        if libro:
            print(f"\nLibro encontrado: {libro.titulo} - {libro.autor} - {libro.genero} - {libro.anio} - {libro.isbn}")
        else:
            print(f"\nNo se encontro el libro con ISBN '{isbn}'.")

    def opcion_buscar_fecha(self):
        self.mostrar_separador()
        print("         BUSCAR POR ANIO")
        self.mostrar_separador()
        self.bm.mostrar_anios_disponibles()
        anio = self.leer_entero("Ingrese anio a buscar: ")
        libros = self.bm.buscar_por_fecha(anio)
        if not libros:
            print(f"\nNo se encontro ningun libro de {anio}.")
        else:
            for libro in libros:
                print(f"{libro.titulo} - {libro.autor} - {libro.genero} - {libro.anio} - {libro.isbn}")

    def opcion_buscar_genero(self):
        self.mostrar_separador()
        print("         BUSCAR POR GENERO")
        self.mostrar_separador()
        self.bm.mostrar_generos_disponibles()
        genero = input("Ingrese genero a buscar: ").strip()
        libros = self.bm.buscar_por_genero(genero)
        if not libros:
            print(f"No se encontraron libros del genero '{genero}'.")
        else:
            for libro in libros:
                print(f"{libro.titulo} - {libro.autor} - {libro.genero} - {libro.anio} - {libro.isbn}")

    def opcion_buscar_rango_fechas(self):
        self.mostrar_separador()
        print("       BUSCAR POR RANGO DE FECHAS")
        self.mostrar_separador()
        inicio = self.leer_entero("Ingrese anio inicial: ")
        fin = self.leer_entero("Ingrese anio final: ")
        libros = self.bm.buscar_por_rango_fechas(inicio, fin)
        for libro in libros:
            print(f"{libro.titulo} - {libro.autor} - {libro.genero} - {libro.anio} - {libro.isbn}")
        if not libros:
            print("No se encontraron libros en ese rango.")

    def opcion_medir_rendimiento(self):
        print("Medicion de rendimiento aun no implementada en detalle.")

    def opcion_exportar_arboles(self):
        print("Exportando arboles a DOT y PNG...")
        self.bm.exportar_todos_los_dots()

    # -----------------------
    # Helpers
    # -----------------------
    @staticmethod
    def leer_entero(mensaje: str) -> int:
        while True:
            try:
                return int(input(mensaje))
            except ValueError:
                print("Ingrese un numero valido.")

    @staticmethod
    def pausar():
        input("\nPresione Enter para continuar...")

    @staticmethod
    def mostrar_separador():
        print("="*50)
