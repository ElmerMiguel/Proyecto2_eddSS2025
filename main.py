# archivo: main.py
from menu.menu import Menu

def main():
    try:
        menu = Menu()
        menu.ejecutar()
    except Exception as e:
        print(f"Error al iniciar: {e}")

if __name__ == "__main__":
    main()
