from software_fj.exceptions import DatoInvalidoError, ReservaInvalidaError, ServicioNoDisponibleError
from software_fj.logger import Logger
from software_fj.models.client import Cliente
from software_fj.models.reservation import Reserva
from software_fj.models.services import Servicio

class SistemaFJ:
    """Gestor principal: administra clientes, servicios y reservas."""

    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []
        Logger.registrar("Sistema Software FJ iniciado.")

    # ---------- Gestión de clientes ----------
    def registrar_cliente(self, identificador, nombre, correo, telefono):
        try:
            if any(c.identificador == str(identificador) for c in self._clientes):
                raise DatoInvalidoError(f"Ya existe un cliente con ID {identificador}.")
            cliente = Cliente(identificador, nombre, correo, telefono)
            self._clientes.append(cliente)
            Logger.registrar(f"Cliente registrado: {cliente.describir()}")
            return cliente
        except DatoInvalidoError as e:
            Logger.registrar(f"Error al registrar cliente: {e}", nivel="ERROR")
            raise
        except Exception as e:
            Logger.registrar(f"Error inesperado al registrar cliente: {e}", nivel="ERROR")
            raise DatoInvalidoError("Error inesperado al registrar cliente.") from e

    def buscar_cliente(self, identificador):
        for c in self._clientes:
            if c.identificador == str(identificador):
                return c
        raise DatoInvalidoError(f"Cliente con ID {identificador} no encontrado.")

    # ---------- Gestión de servicios ----------
    def agregar_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("El objeto no es un servicio válido.")
        if any(s.identificador == servicio.identificador for s in self._servicios):
            raise DatoInvalidoError(f"Ya existe un servicio con ID {servicio.identificador}.")
        self._servicios.append(servicio)
        Logger.registrar(f"Servicio agregado: {servicio.describir()}")
        return servicio

    def buscar_servicio(self, identificador):
        for s in self._servicios:
            if s.identificador == str(identificador):
                return s
        raise ServicioNoDisponibleError(f"Servicio con ID {identificador} no encontrado.")

    # ---------- Gestión de reservas ----------
    def crear_reserva(self, identificador, id_cliente, id_servicio, duracion_horas):
        try:
            cliente = self.buscar_cliente(id_cliente)
            servicio = self.buscar_servicio(id_servicio)
            reserva = Reserva(identificador, cliente, servicio, duracion_horas)
            self._reservas.append(reserva)
            Logger.registrar(f"Reserva creada: {reserva.describir()}")
            return reserva
        except (DatoInvalidoError, ServicioNoDisponibleError) as e:
            Logger.registrar(f"Error al crear reserva {identificador}: {e}", nivel="ERROR")
            raise
        except Exception as e:
            Logger.registrar(f"Error inesperado al crear reserva: {e}", nivel="ERROR")
            raise ReservaInvalidaError("Error inesperado al crear la reserva.") from e

    def listar_todo(self):
        print("\n=== CLIENTES ===")
        for c in self._clientes:
            print(" -", c.describir())
        print("\n=== SERVICIOS ===")
        for s in self._servicios:
            print(" -", s.describir())
        print("\n=== RESERVAS ===")
        for r in self._reservas:
            print(" -", r.describir())
