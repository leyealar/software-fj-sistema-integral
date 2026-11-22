"""Coordinador principal: administra listas internas y registra eventos/errores."""

from clientes import Cliente
from excepciones import (
    ClienteNoEncontradoError,
    DatoInvalidoError,
    EntidadDuplicadaError,
    ReservaNoEncontradaError,
    ServicioNoEncontradoError,
)
from registro import configurar_logger
from reservas import Reserva
from servicios import Servicio


class SistemaSoftwareFJ:
    """Administra clientes, servicios y reservas sin utilizar base de datos."""

    def __init__(self, ruta_log="logs/software_fj.log"):
        self._clientes = []
        self._servicios = []
        self._reservas = []
        self._logger = configurar_logger(ruta_log)

    @property
    def clientes(self):
        return tuple(self._clientes)

    @property
    def servicios(self):
        return tuple(self._servicios)

    @property
    def reservas(self):
        return tuple(self._reservas)

    def _buscar_por_codigo(self, elementos, codigo, tipo_error, etiqueta):
        for elemento in elementos:
            if elemento.codigo == codigo:
                return elemento
        raise tipo_error(f"No se encontro {etiqueta} con codigo {codigo}.")

    def registrar_cliente(self, cliente):
        """Registra cliente usando try/except/else/finally y lista interna."""
        try:
            if not isinstance(cliente, Cliente):
                raise DatoInvalidoError("El objeto que se intenta registrar no es un Cliente.")
            if any(item.codigo == cliente.codigo for item in self._clientes):
                raise EntidadDuplicadaError(f"Ya existe el cliente {cliente.codigo}.")
        except Exception as error:
            self._logger.exception("Error al registrar cliente.")
            raise
        else:
            self._clientes.append(cliente)
            self._logger.info("Cliente registrado: %s", cliente.codigo)
            return cliente
        finally:
            self._logger.info("Finalizo la operacion de registro de cliente.")

    def registrar_servicio(self, servicio):
        try:
            if not isinstance(servicio, Servicio):
                raise DatoInvalidoError("El objeto que se intenta registrar no es un Servicio.")
            if any(item.codigo == servicio.codigo for item in self._servicios):
                raise EntidadDuplicadaError(f"Ya existe el servicio {servicio.codigo}.")
            if not servicio.validar_parametros():
                raise DatoInvalidoError("Los parametros del servicio no son validos.")
        except Exception:
            self._logger.exception("Error al registrar servicio.")
            raise
        else:
            self._servicios.append(servicio)
            self._logger.info("Servicio registrado: %s", servicio.codigo)
            return servicio
        finally:
            self._logger.info("Finalizo la operacion de registro de servicio.")

    def buscar_cliente(self, codigo):
        return self._buscar_por_codigo(
            self._clientes, codigo, ClienteNoEncontradoError, "cliente"
        )

    def buscar_servicio(self, codigo):
        return self._buscar_por_codigo(
            self._servicios, codigo, ServicioNoEncontradoError, "servicio"
        )

    def crear_reserva(self, codigo=None, codigo_cliente=None, codigo_servicio=None,
                      duracion=None, cantidad=1, impuesto=0, descuento=0):
        try:
            if not codigo or not codigo_cliente or not codigo_servicio or duracion is None:
                raise DatoInvalidoError(
                    "Faltan datos obligatorios: codigo, cliente, servicio y duracion."
                )
            if any(item.codigo == codigo for item in self._reservas):
                raise EntidadDuplicadaError(f"Ya existe la reserva {codigo}.")
            cliente = self.buscar_cliente(codigo_cliente)
            servicio = self.buscar_servicio(codigo_servicio)
            reserva = Reserva(
                codigo, cliente, servicio, duracion,
                cantidad=cantidad, impuesto=impuesto, descuento=descuento
            )
        except Exception as error:
            self._logger.exception("Error al crear reserva %s.", codigo)
            # Encadenamiento: el error original queda disponible en __cause__.
            from excepciones import ReservaNoValidaError
            raise ReservaNoValidaError(
                f"La solicitud de reserva {codigo} no pudo completarse."
            ) from error
        else:
            self._reservas.append(reserva)
            self._logger.info("Reserva creada: %s", codigo)
            return reserva
        finally:
            self._logger.info("Finalizo la operacion de creacion de reserva %s.", codigo)

    def buscar_reserva(self, codigo):
        return self._buscar_por_codigo(
            self._reservas, codigo, ReservaNoEncontradaError, "reserva"
        )

    def confirmar_reserva(self, codigo):
        reserva = self.buscar_reserva(codigo)
        try:
            resultado = reserva.confirmar()
        except Exception:
            self._logger.exception("Error al confirmar reserva %s.", codigo)
            raise
        else:
            self._logger.info("Reserva confirmada: %s", codigo)
            return resultado
        finally:
            self._logger.info("Finalizo la operacion de confirmacion de reserva %s.", codigo)

    def cancelar_reserva(self, codigo):
        reserva = self.buscar_reserva(codigo)
        try:
            resultado = reserva.cancelar()
        except Exception:
            self._logger.exception("Error al cancelar reserva %s.", codigo)
            raise
        else:
            self._logger.info("Reserva cancelada: %s", codigo)
            return resultado
        finally:
            self._logger.info("Finalizo la operacion de cancelacion de reserva %s.", codigo)

    def procesar_reserva(self, codigo):
        reserva = self.buscar_reserva(codigo)
        try:
            resultado = reserva.procesar()
        except Exception:
            self._logger.exception("Error al procesar reserva %s.", codigo)
            raise
        else:
            self._logger.info("Reserva procesada: %s", codigo)
            return resultado
        finally:
            self._logger.info("Finalizo la operacion de procesamiento de reserva %s.", codigo)

    def resumen(self):
        return {
            "clientes": len(self._clientes),
            "servicios": len(self._servicios),
            "reservas": len(self._reservas),
        }

    def cerrar(self):
        """Vacía y cierra los manejadores del archivo de logs.

        Este método libera el archivo para que pueda moverse, eliminarse o
        limpiarse después de las pruebas, especialmente en Windows.
        """
        for handler in list(self._logger.handlers):
            self._logger.removeHandler(handler)
            handler.flush()
            handler.close()
