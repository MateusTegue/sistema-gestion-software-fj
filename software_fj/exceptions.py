class ErrorSistemaFJ(Exception):
    """Excepción base del sistema Software FJ."""
    pass


class DatoInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando un dato ingresado no cumple las validaciones."""
    pass


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando un servicio no está disponible para reserva."""
    pass


class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza cuando una reserva no puede procesarse correctamente."""
    pass


class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Se lanza cuando se intenta una operación no permitida."""
    pass
