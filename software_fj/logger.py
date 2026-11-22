import datetime

class Logger:
    """Registra eventos y errores en un archivo de logs."""

    ARCHIVO = "registro_eventos.log"

    @staticmethod
    def registrar(mensaje, nivel="INFO"):
        try:
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(Logger.ARCHIVO, "a", encoding="utf-8") as f:
                f.write(f"[{fecha}] [{nivel}] {mensaje}\n")
        except OSError as e:
            # Si falla el log, no se interrumpe la aplicación
            print(f"Advertencia: no se pudo escribir en el log: {e}")
