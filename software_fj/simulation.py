from software_fj.exceptions import DatoInvalidoError, ServicioNoDisponibleError
from software_fj.logger import Logger
from software_fj.models.services import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from software_fj.services.system import SistemaFJ

def ejecutar_simulacion():
    print("=" * 60)
    print(" SIMULACIÓN DEL SISTEMA SOFTWARE FJ")
    print("=" * 60)

    sistema = SistemaFJ()

    # --- Operación 1: Cliente válido ---
    try:
        c1 = sistema.registrar_cliente("C001", "Ana María López", "ana@correo.com", "3001234567")
        print("Op1 OK ->", c1.describir())
    except Exception as e:
        print("Op1 FALLÓ ->", e)

    # --- Operación 2: Cliente inválido (correo mal formado) ---
    try:
        sistema.registrar_cliente("C002", "Luis Pérez", "correo-invalido", "3109876543")
    except DatoInvalidoError as e:
        print("Op2 controlada ->", e)

    # --- Operación 3: Cliente inválido (teléfono no numérico) ---
    try:
        sistema.registrar_cliente("C003", "Carlos Ruiz", "carlos@correo.com", "ABC123")
    except DatoInvalidoError as e:
        print("Op3 controlada ->", e)

    # --- Operación 4: Cliente duplicado ---
    try:
        sistema.registrar_cliente("C001", "Otra Persona", "otra@correo.com", "3001112233")
    except DatoInvalidoError as e:
        print("Op4 controlada ->", e)

    # --- Operación 5: Servicio válido (sala) ---
    try:
        sala = sistema.agregar_servicio(ReservaSala("S001", "Sala Ejecutiva", 50000, 12))
        print("Op5 OK ->", sala.describir())
    except Exception as e:
        print("Op5 FALLÓ ->", e)

    # --- Operación 6: Servicio inválido (tarifa negativa) ---
    try:
        sistema.agregar_servicio(AlquilerEquipo("S002", "Proyector", -1000, "Video"))
    except DatoInvalidoError as e:
        print("Op6 controlada ->", e)

    # --- Operación 7: Servicio válido (equipo y asesoría) ---
    try:
        equipo = sistema.agregar_servicio(AlquilerEquipo("S003", "Laptop HP", 30000, "Cómputo"))
        asesoria = sistema.agregar_servicio(AsesoriaEspecializada("S004", "Asesoría Java", 80000, "Programación"))
        print("Op7 OK ->", equipo.describir())
        print("           ", asesoria.describir())
    except Exception as e:
        print("Op7 FALLÓ ->", e)

    # --- Operación 8: Reserva exitosa ---
    try:
        r1 = sistema.crear_reserva("R001", "C001", "S001", 3)
        costo = r1.confirmar()
        r1.procesar()
        print(f"Op8 OK -> Reserva confirmada y procesada. Costo: ${costo:.2f}")
    except Exception as e:
        print("Op8 FALLÓ ->", e)

    # --- Operación 9: Reserva fallida (servicio no disponible) ---
    try:
        asesoria.marcar_no_disponible()
        r2 = sistema.crear_reserva("R002", "C001", "S004", 2)
        r2.confirmar()
    except ServicioNoDisponibleError as e:
        print("Op9 controlada ->", e)
    except Exception as e:
        print("Op9 controlada ->", e)

    # --- Operación 10: Reserva fallida (duración inválida) y cancelación ---
    try:
        r3 = sistema.crear_reserva("R003", "C001", "S003", -2)
        r3.confirmar()
    except DatoInvalidoError as e:
        print("Op10a controlada ->", e)
    except Exception as e:
        print("Op10a controlada ->", e)

    try:
        r4 = sistema.crear_reserva("R004", "C001", "S003", 5)
        r4.confirmar()
        r4.cancelar()
        print(f"Op10b OK -> Reserva cancelada. Estado: {r4.estado}")
    except Exception as e:
        print("Op10b controlada ->", e)

    # --- Estado final del sistema ---
    sistema.listar_todo()
    Logger.registrar("Simulación finalizada correctamente.")


if __name__ == "__main__":
    try:
        ejecutar_simulacion()
    except Exception as e:
        Logger.registrar(f"Error crítico no controlado: {e}", nivel="CRITICAL")
        print("El sistema continúa estable. Revise el archivo de logs.")
