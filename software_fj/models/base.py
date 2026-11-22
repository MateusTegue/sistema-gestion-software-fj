from abc import ABC, abstractmethod

from software_fj.exceptions import DatoInvalidoError


class EntidadBase(ABC):
    """Clase abstracta que representa entidades generales del sistema."""

    def __init__(self, identificador):
        if not identificador or not str(identificador).strip():
            raise DatoInvalidoError("El identificador no puede estar vacío.")
        self._identificador = str(identificador).strip()

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def describir(self):
        """Devuelve una descripción textual de la entidad."""
        pass
