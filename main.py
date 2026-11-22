"""Punto de entrada del sistema interactivo Software FJ."""

from software_fj.logger import Logger
from software_fj.menu import ejecutar_menu


if __name__ == "__main__":
    try:
        ejecutar_menu()
    except Exception as e:
        Logger.registrar(f"Error crítico no controlado: {e}", nivel="CRITICAL")
        print("El sistema se cerró por un error inesperado. Revise el archivo de logs.")
