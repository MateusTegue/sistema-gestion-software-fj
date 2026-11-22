from software_fj.exceptions import ErrorSistemaFJ
from software_fj.logger import Logger
from software_fj.models.services import (
    AlquilerEquipo,
    AsesoriaEspecializada,
    ReservaSala,
)
from software_fj.services.system import SistemaFJ


def _registrar_cliente(sistema):
    print("\n--- Registrar cliente ---")
    cliente = sistema.registrar_cliente(
        input("Identificador: ").strip(),
        input("Nombre: ").strip(),
        input("Correo: ").strip(),
        input("Teléfono: ").strip(),
    )
    print("Cliente registrado:", cliente.describir())


def _crear_servicio(sistema):
    print("\n--- Agregar servicio ---")
    print("1. Reserva de sala")
    print("2. Alquiler de equipo")
    print("3. Asesoría especializada")
    tipo = input("Tipo de servicio: ").strip()
    identificador = input("Identificador: ").strip()
    nombre = input("Nombre: ").strip()
    tarifa = float(input("Tarifa por hora: ").strip())

    if tipo == "1":
        capacidad = int(input("Capacidad de la sala: ").strip())
        servicio = ReservaSala(identificador, nombre, tarifa, capacidad)
    elif tipo == "2":
        tipo_equipo = input("Tipo de equipo: ").strip()
        servicio = AlquilerEquipo(identificador, nombre, tarifa, tipo_equipo)
    elif tipo == "3":
        area = input("Área de asesoría: ").strip()
        servicio = AsesoriaEspecializada(identificador, nombre, tarifa, area)
    else:
        print("Tipo de servicio no válido.")
        return

    sistema.agregar_servicio(servicio)
    print("Servicio agregado:", servicio.describir())


def _crear_reserva(sistema):
    print("\n--- Crear y confirmar reserva ---")
    reserva = sistema.crear_reserva(
        input("Identificador de reserva: ").strip(),
        input("Identificador del cliente: ").strip(),
        input("Identificador del servicio: ").strip(),
        float(input("Duración en horas: ").strip()),
    )
    costo = reserva.confirmar()
    print(f"Reserva confirmada. Costo total: ${costo:.2f}")
    if input("¿Desea procesarla ahora? (s/n): ").strip().lower() == "s":
        reserva.procesar()
        print("Reserva procesada.")


def ejecutar_menu():
    """Ejecuta el menú interactivo hasta que el usuario finaliza."""
    sistema = SistemaFJ()
    print("=" * 60)
    print(" SISTEMA DE GESTIÓN SOFTWARE FJ")
    print("=" * 60)

    while True:
        print("\n1. Registrar cliente")
        print("2. Agregar servicio")
        print("3. Crear reserva")
        print("4. Consultar información")
        print("5. Finalizar y mostrar resultados")
        opcion = input("Seleccione una opción: ").strip()

        try:
            if opcion == "1":
                _registrar_cliente(sistema)
            elif opcion == "2":
                _crear_servicio(sistema)
            elif opcion == "3":
                _crear_reserva(sistema)
            elif opcion == "4":
                sistema.listar_todo()
            elif opcion == "5":
                print("\n=== RESULTADO FINAL ===")
                sistema.listar_todo()
                Logger.registrar("Ejecución interactiva finalizada.")
                print("Programa finalizado.")
                break
            else:
                print("Opción no válida. Seleccione una opción del 1 al 5.")
        except ErrorSistemaFJ as error:
            print(f"No se pudo completar la operación: {error}")
        except ValueError:
            print("Dato no válido: revise que los valores numéricos sean correctos.")
        except (EOFError, KeyboardInterrupt):
            print("\nEjecución interrumpida. Estado actual:")
            sistema.listar_todo()
            break

