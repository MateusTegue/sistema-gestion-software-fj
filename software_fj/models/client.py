from software_fj.exceptions import DatoInvalidoError
from software_fj.models.base import EntidadBase

class Cliente(EntidadBase):
    """Representa un cliente con validaciones y encapsulación."""

    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)
        self._nombre = self._validar_nombre(nombre)
        self._correo = self._validar_correo(correo)
        self._telefono = self._validar_telefono(telefono)

    @staticmethod
    def _validar_nombre(nombre):
        if not nombre or not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise DatoInvalidoError("El nombre debe tener al menos 3 caracteres.")
        return nombre.strip().title()

    @staticmethod
    def _validar_correo(correo):
        if not correo or "@" not in correo or "." not in correo.split("@")[-1]:
            raise DatoInvalidoError(f"Correo inválido: {correo}")
        return correo.strip().lower()

    @staticmethod
    def _validar_telefono(telefono):
        tel = str(telefono).strip()
        if not tel.isdigit() or len(tel) < 7:
            raise DatoInvalidoError(f"Teléfono inválido: {telefono}")
        return tel

    @property
    def nombre(self):
        return self._nombre

    @property
    def correo(self):
        return self._correo

    @property
    def telefono(self):
        return self._telefono

    def describir(self):
        return f"Cliente[{self.identificador}] {self._nombre} - {self._correo} - {self._telefono}"

    def __str__(self):
        return self.describir()
