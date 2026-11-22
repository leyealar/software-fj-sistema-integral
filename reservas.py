"""Entidad Reserva con estados y operaciones controladas."""

from entidades import Entidad
from excepciones import DatoInvalidoError, OperacionNoPermitidaError, ReservaNoValidaError
from servicios import AlquilerEquipo


class Reserva(Entidad):
    """Reserva que relaciona un cliente, un servicio, duracion y estado."""

    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    PROCESADA = "PROCESADA"
    CANCELADA = "CANCELADA"

    def __init__(self, codigo, cliente, servicio, duracion, cantidad=1,
                 impuesto=0, descuento=0):
        super().__init__(codigo, f"Reserva {codigo}")
        try:
            if cliente is None or not hasattr(cliente, "correo"):
                raise DatoInvalidoError("Debe asociarse un cliente valido.")
            if servicio is None or not hasattr(servicio, "calcular_costo"):
                raise DatoInvalidoError("Debe asociarse un servicio valido.")
            self._duracion = servicio._validar_numero_positivo(duracion, "duracion")
            self._cantidad = servicio._validar_entero_positivo(cantidad, "cantidad")
            self._impuesto = servicio._validar_porcentaje(impuesto, "impuesto")
            self._descuento = servicio._validar_porcentaje(descuento, "descuento")
            self._total = servicio.calcular_costo(
                self._duracion, self._cantidad, self._impuesto, self._descuento
            )
        except Exception as error:
            raise ReservaNoValidaError(
                f"No fue posible crear la reserva {codigo}: {error}"
            ) from error

        self._cliente = cliente
        self._servicio = servicio
        self._estado = self.PENDIENTE
        self._inventario_descontado = False

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def total(self):
        return self._total

    @property
    def estado(self):
        return self._estado

    def confirmar(self):
        if self._estado != self.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"Solo se puede confirmar una reserva pendiente; estado actual: {self._estado}."
            )
        if isinstance(self._servicio, AlquilerEquipo):
            self._servicio.reservar_unidades(self._cantidad)
            self._inventario_descontado = True
        self._estado = self.CONFIRMADA
        return self._estado

    def cancelar(self):
        if self._estado not in (self.PENDIENTE, self.CONFIRMADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva en estado {self._estado}."
            )
        if self._inventario_descontado and isinstance(self._servicio, AlquilerEquipo):
            self._servicio.devolver_unidades(self._cantidad)
            self._inventario_descontado = False
        self._estado = self.CANCELADA
        return self._estado

    def procesar(self):
        if self._estado != self.CONFIRMADA:
            raise OperacionNoPermitidaError(
                "La reserva debe estar confirmada antes de procesarse."
            )
        self._estado = self.PROCESADA
        return self._estado

    def describir(self):
        return (
            f"{self.codigo} | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | Duracion: {self.duracion} | "
            f"Cantidad: {self.cantidad} | Total: ${self.total:,.2f} | "
            f"Estado: {self.estado}"
        )
