"""Excepciones personalizadas para el sistema Software FJ."""


class ErrorSoftwareFJ(Exception):
    """Excepcion base para los errores controlados de la aplicacion."""


class DatoInvalidoError(ErrorSoftwareFJ, ValueError):
    """Se produce cuando un dato no cumple las reglas de validacion."""


class EntidadDuplicadaError(ErrorSoftwareFJ):
    """Se produce cuando se intenta registrar un codigo ya existente."""


class ClienteNoEncontradoError(ErrorSoftwareFJ):
    """Se produce cuando no existe el cliente solicitado."""


class ServicioNoEncontradoError(ErrorSoftwareFJ):
    """Se produce cuando no existe el servicio solicitado."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se produce cuando se intenta usar un servicio no disponible."""


class ReservaNoEncontradaError(ErrorSoftwareFJ):
    """Se produce cuando no existe la reserva solicitada."""


class ReservaNoValidaError(ErrorSoftwareFJ):
    """Se produce cuando una reserva no puede crearse con los datos dados."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se produce cuando una operacion no corresponde al estado actual."""
