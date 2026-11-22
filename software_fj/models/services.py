from abc import ABC, abstractmethod

from software_fj.exceptions import DatoInvalidoError, ServicioNoDisponibleError
from software_fj.models.base import EntidadBase

class Servicio(EntidadBase, ABC):
    """Clase abstracta para los servicios ofrecidos por Software FJ."""

    def __init__(self, identificador, nombre, tarifa_base, disponible=True):
        super().__init__(identificador)
        self._nombre = self._validar_texto(nombre, "nombre del servicio")
        self._tarifa_base = self._validar_tarifa(tarifa_base)
        self._disponible = bool(disponible)

    @staticmethod
    def _validar_texto(valor, campo):
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatoInvalidoError(f"El {campo} debe tener al menos 3 caracteres.")
        return valor.strip().title()

    @staticmethod
    def _validar_tarifa(tarifa):
        try:
            tarifa = float(tarifa)
        except (TypeError, ValueError) as e:
            raise DatoInvalidoError(f"Tarifa inválida: {tarifa}") from e
        if tarifa <= 0:
            raise DatoInvalidoError("La tarifa base debe ser mayor que cero.")
        return tarifa

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    def marcar_no_disponible(self):
        self._disponible = False

    def marcar_disponible(self):
        self._disponible = True

    @abstractmethod
    def calcular_costo(self, duracion_horas, **kwargs):
        """Calcula el costo del servicio. Debe implementarse en cada subclase."""
        pass

    @abstractmethod
    def describir(self):
        pass

    def validar_parametros(self, duracion_horas):
        if not isinstance(duracion_horas, (int, float)) or duracion_horas <= 0:
            raise DatoInvalidoError("La duración debe ser un número positivo.")
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self._nombre}' no está disponible."
            )

    # Método sobrecargado (variantes con impuestos y descuentos)
    def calcular_costo_con_impuesto(self, duracion_horas, impuesto=0.19):
        base = self.calcular_costo(duracion_horas)
        return round(base * (1 + impuesto), 2)

    def calcular_costo_con_descuento(self, duracion_horas, descuento=0.10):
        base = self.calcular_costo(duracion_horas)
        return round(base * (1 - descuento), 2)

    def __str__(self):
        return self.describir()


class ReservaSala(Servicio):
    """Servicio de reserva de salas."""

    def __init__(self, identificador, nombre, tarifa_base, capacidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatoInvalidoError("La capacidad debe ser un entero positivo.")
        self._capacidad = capacidad

    @property
    def capacidad(self):
        return self._capacidad

    def calcular_costo(self, duracion_horas, **kwargs):
        self.validar_parametros(duracion_horas)
        return round(self._tarifa_base * duracion_horas, 2)

    def describir(self):
        return (f"ReservaSala[{self.identificador}] {self._nombre} - "
                f"Capacidad: {self._capacidad} - Tarifa/h: ${self._tarifa_base:.2f}")


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos."""

    def __init__(self, identificador, nombre, tarifa_base, tipo_equipo, disponible=True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        self._tipo_equipo = self._validar_texto(tipo_equipo, "tipo de equipo")

    @property
    def tipo_equipo(self):
        return self._tipo_equipo

    def calcular_costo(self, duracion_horas, **kwargs):
        self.validar_parametros(duracion_horas)
        # Recargo del 5% por manipulación de equipos
        return round(self._tarifa_base * duracion_horas * 1.05, 2)

    def describir(self):
        return (f"AlquilerEquipo[{self.identificador}] {self._nombre} - "
                f"Tipo: {self._tipo_equipo} - Tarifa/h: ${self._tarifa_base:.2f}")


class AsesoriaEspecializada(Servicio):
    """Servicio de asesorías especializadas."""

    def __init__(self, identificador, nombre, tarifa_base, area, disponible=True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        self._area = self._validar_texto(area, "área de asesoría")

    @property
    def area(self):
        return self._area

    def calcular_costo(self, duracion_horas, **kwargs):
        self.validar_parametros(duracion_horas)
        # Recargo del 15% por especialización
        return round(self._tarifa_base * duracion_horas * 1.15, 2)

    def describir(self):
        return (f"AsesoriaEspecializada[{self.identificador}] {self._nombre} - "
                f"Área: {self._area} - Tarifa/h: ${self._tarifa_base:.2f}")


