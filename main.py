import sys
from gui_app import iniciar_gui

def main():
    try:
        iniciar_gui()
    except Exception as e:
        print(f"Error al iniciar GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()