"""Modulo 3 - Servicios del sistema Software FJ.

Contiene la clase abstracta Servicio y tres servicios especializados:
ReservaSala, AlquilerEquipo y AsesoriaEspecializada.

Este modulo es independiente para facilitar su integracion con la clase
Entidad y el sistema de excepciones del proyecto grupal.
"""

from abc import ABC, abstractmethod
import math


class Servicio(ABC):
    """Clase abstracta que define el comportamiento comun de un servicio."""

    def __init__(self, codigo, nombre, tarifa_base, disponible=True):
        self._codigo = self._validar_texto(codigo, "codigo")
        self._nombre = self._validar_texto(nombre, "nombre")
        self._tarifa_base = self._validar_numero_positivo(
            tarifa_base, "tarifa base"
        )
        if not isinstance(disponible, bool):
            raise ValueError("La disponibilidad debe ser un valor booleano.")
        self._disponible = disponible

    @staticmethod
    def _validar_texto(valor, campo):
        """Valida que un dato de texto exista y no este vacio."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"El campo {campo} es obligatorio.")
        return valor.strip()

    @staticmethod
    def _validar_numero_positivo(valor, campo):
        """Valida un numero real, finito y mayor que cero."""
        if (
            isinstance(valor, bool)
            or not isinstance(valor, (int, float))
            or not math.isfinite(valor)
            or valor <= 0
        ):
            raise ValueError(f"El campo {campo} debe ser un numero mayor que cero.")
        return float(valor)

    @staticmethod
    def _validar_entero_positivo(valor, campo):
        """Valida que el dato sea un numero entero positivo."""
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            raise ValueError(f"El campo {campo} debe ser un entero positivo.")
        return valor

    @staticmethod
    def _validar_porcentaje(valor, campo):
        """Valida que el porcentaje sea finito y este entre 0 y 100."""
        if (
            isinstance(valor, bool)
            or not isinstance(valor, (int, float))
            or not math.isfinite(valor)
            or not 0 <= valor <= 100
        ):
            raise ValueError(f"El porcentaje de {campo} debe estar entre 0 y 100.")
        return float(valor)

    @property
    def codigo(self):
        """Codigo identificador del servicio (solo lectura)."""
        return self._codigo

    @property
    def nombre(self):
        """Nombre del servicio (solo lectura)."""
        return self._nombre

    @property
    def tarifa_base(self):
        """Tarifa base del servicio (solo lectura)."""
        return self._tarifa_base

    @property
    def disponible(self):
        """Indica si el servicio se encuentra disponible."""
        return self._disponible

    def _calcular_total(self, duracion, cantidad, impuesto, descuento):
        """Calcula el costo con duracion, cantidad, impuesto y descuento.

        La formula aplicada es:
            subtotal = tarifa_base * duracion * cantidad
            total = subtotal + impuesto - descuento

        El descuento se aplica despues de calcular el impuesto, de acuerdo
        con la formula porcentual incluida en este ejercicio.
        """
        duracion = self._validar_numero_positivo(duracion, "duracion")
        cantidad = self._validar_entero_positivo(cantidad, "cantidad")
        impuesto = self._validar_porcentaje(impuesto, "impuesto")
        descuento = self._validar_porcentaje(descuento, "descuento")

        subtotal = self._tarifa_base * duracion * cantidad
        total = subtotal * (1 + impuesto / 100) * (1 - descuento / 100)
        return round(total, 2)

    @abstractmethod
    def calcular_costo(self, duracion=1, cantidad=1, impuesto=0, descuento=0):
        """Calcula el costo; cada servicio implementa su propia validacion."""
        raise NotImplementedError

    @abstractmethod
    def describir(self):
        """Devuelve una descripcion legible del servicio."""
        raise NotImplementedError

    @abstractmethod
    def validar_parametros(self):
        """Verifica los parametros especificos del servicio."""
        raise NotImplementedError


class ReservaSala(Servicio):
    """Servicio para reservar salas por horas."""

    def __init__(self, codigo, nombre, tarifa_base, capacidad, disponible=True):
        super().__init__(codigo, nombre, tarifa_base, disponible)
        self._capacidad = self._validar_entero_positivo(capacidad, "capacidad")

    @property
    def capacidad(self):
        return self._capacidad

    def validar_parametros(self):
        return self._capacidad > 0

    def describir(self):
        return (
            f"Sala: {self.nombre} | Capacidad: {self.capacidad} personas | "
            f"Tarifa por hora: ${self.tarifa_base:,.2f}"
        )

    def calcular_costo(self, duracion=1, cantidad=1, impuesto=0, descuento=0):
        if not self.disponible:
            raise ValueError("La sala no se encuentra disponible.")
        return self._calcular_total(duracion, cantidad, impuesto, descuento)


class AlquilerEquipo(Servicio):
    """Servicio para alquilar equipos segun las unidades disponibles."""

    def __init__(
        self, codigo, nombre, tarifa_base, unidades_disponibles, disponible=True
    ):
        super().__init__(codigo, nombre, tarifa_base, disponible)
        if (
            isinstance(unidades_disponibles, bool)
            or not isinstance(unidades_disponibles, int)
            or unidades_disponibles < 0
        ):
            raise ValueError("Las unidades disponibles deben ser un entero igual o mayor que cero.")
        self._unidades_disponibles = unidades_disponibles

    @property
    def unidades_disponibles(self):
        return self._unidades_disponibles

    def validar_parametros(self):
        return self._unidades_disponibles >= 0

    def describir(self):
        return (
            f"Equipo: {self.nombre} | Unidades disponibles: "
            f"{self.unidades_disponibles} | Tarifa por dia: "
            f"${self.tarifa_base:,.2f}"
        )

    def calcular_costo(self, duracion=1, cantidad=1, impuesto=0, descuento=0):
        if not self.disponible:
            raise ValueError("El servicio de alquiler no esta disponible.")
        cantidad = self._validar_entero_positivo(cantidad, "cantidad")
        if cantidad > self.unidades_disponibles:
            raise ValueError("No hay suficientes equipos disponibles.")
        return self._calcular_total(duracion, cantidad, impuesto, descuento)


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoria profesional por horas."""

    def __init__(self, codigo, nombre, tarifa_base, especialidad, disponible=True):
        super().__init__(codigo, nombre, tarifa_base, disponible)
        self._especialidad = self._validar_texto(especialidad, "especialidad")

    @property
    def especialidad(self):
        return self._especialidad

    def validar_parametros(self):
        return bool(self._especialidad.strip())

    def describir(self):
        return (
            f"Asesoria: {self.nombre} | Especialidad: {self.especialidad} | "
            f"Tarifa por hora: ${self.tarifa_base:,.2f}"
        )

    def calcular_costo(self, duracion=1, cantidad=1, impuesto=0, descuento=0):
        if not self.disponible:
            raise ValueError("La asesoria no se encuentra disponible.")
        return self._calcular_total(duracion, cantidad, impuesto, descuento)
