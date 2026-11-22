from software_fj.exceptions import DatoInvalidoError, OperacionNoPermitidaError, ReservaInvalidaError
from software_fj.logger import Logger
from software_fj.models.client import Cliente
from software_fj.models.services import Servicio

class Reserva:
    """Integra cliente, servicio, duración y estado."""

    ESTADOS = {"PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA"}

    def __init__(self, identificador, cliente, servicio, duracion_horas):
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("La reserva requiere un Cliente válido.")
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("La reserva requiere un Servicio válido.")
        self._identificador = identificador
        self._cliente = cliente
        self._servicio = servicio
        self._duracion_horas = duracion_horas
        self._estado = "PENDIENTE"
        self._costo_total = None

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    def confirmar(self):
        if self._estado != "PENDIENTE":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self._estado}."
            )
        self._servicio.validar_parametros(self._duracion_horas)
        self._costo_total = self._servicio.calcular_costo(self._duracion_horas)
        self._estado = "CONFIRMADA"
        Logger.registrar(f"Reserva {self._identificador} confirmada. Costo: ${self._costo_total:.2f}")
        return self._costo_total

    def cancelar(self):
        if self._estado in ("CANCELADA", "PROCESADA"):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva en estado {self._estado}."
            )
        self._estado = "CANCELADA"
        Logger.registrar(f"Reserva {self._identificador} cancelada.")

    def procesar(self):
        if self._estado != "CONFIRMADA":
            raise ReservaInvalidaError(
                "Solo se pueden procesar reservas confirmadas."
            )
        self._estado = "PROCESADA"
        Logger.registrar(f"Reserva {self._identificador} procesada correctamente.")
        return True

    def describir(self):
        costo = f"${self._costo_total:.2f}" if self._costo_total is not None else "N/A"
        return (f"Reserva[{self._identificador}] Cliente: {self._cliente.nombre} - "
                f"Servicio: {self._servicio.nombre} - Duración: {self._duracion_horas}h - "
                f"Estado: {self._estado} - Costo: {costo}")

    def __str__(self):
        return self.describir()
