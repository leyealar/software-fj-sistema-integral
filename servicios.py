"""
Modulo 3: Servicios especializados - Software FJ
Estudiante responsable: Leidy Yesenia Alvarez Arias
Curso: Programacion (213023) - UNAD
Fase 4 - Practicas simuladas
Contiene la clase abstracta Servicio y sus tres clases especializadas.
"""

import math
from abc import ABC, abstractmethod

from entidades import Entidad
from excepciones import DatoInvalidoError, ServicioNoDisponibleError


class Servicio(Entidad, ABC):
    """Clase abstracta que establece la estructura comun de los servicios."""

    def __init__(self, codigo, nombre, tarifa_base, disponible=True):
        super().__init__(codigo, nombre)
        self._tarifa_base = self._validar_numero_positivo(tarifa_base, "tarifa base")
        if not isinstance(disponible, bool):
            raise DatoInvalidoError("La disponibilidad debe ser verdadera o falsa.")
        self._disponible = disponible

    @staticmethod
    def _validar_numero_positivo(valor, campo):
        if (
            isinstance(valor, bool)
            or not isinstance(valor, (int, float))
            or not math.isfinite(valor)
            or valor <= 0
        ):
            raise DatoInvalidoError(f"El campo {campo} debe ser un numero finito mayor que cero.")
        return float(valor)

    @staticmethod
    def _validar_entero_positivo(valor, campo):
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            raise DatoInvalidoError(f"El campo {campo} debe ser un entero positivo.")
        return valor

    @staticmethod
    def _validar_porcentaje(valor, campo):
        if (
            isinstance(valor, bool)
            or not isinstance(valor, (int, float))
            or not math.isfinite(valor)
            or not 0 <= valor <= 100
        ):
            raise DatoInvalidoError(f"El porcentaje de {campo} debe estar entre 0 y 100.")
        return float(valor)

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, disponible):
        if not isinstance(disponible, bool):
            raise DatoInvalidoError("La disponibilidad debe ser verdadera o falsa.")
        self._disponible = disponible

    def _verificar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self.codigo} - {self.nombre} no esta disponible."
            )

    def _calcular_total(self, duracion, cantidad, impuesto, descuento):
        """Calcula el costo con parametros opcionales: impuesto y descuento."""
        duracion = self._validar_numero_positivo(duracion, "duracion")
        cantidad = self._validar_entero_positivo(cantidad, "cantidad")
        impuesto = self._validar_porcentaje(impuesto, "impuesto")
        descuento = self._validar_porcentaje(descuento, "descuento")
        subtotal = self._tarifa_base * duracion * cantidad
        total = subtotal * (1 + impuesto / 100) * (1 - descuento / 100)
        if not math.isfinite(total):
            raise DatoInvalidoError("El calculo produjo un valor no finito.")
        return round(total, 2)

    @abstractmethod
    def calcular_costo(self, duracion=1, cantidad=1, impuesto=0, descuento=0):
        """Calcula el costo usando variantes mediante parametros opcionales."""
        raise NotImplementedError

    @abstractmethod
    def validar_parametros(self):
        """Verifica los atributos particulares de cada servicio."""
        raise NotImplementedError

    @abstractmethod
    def describir(self):
        """Devuelve la descripcion especifica del servicio."""
        raise NotImplementedError


class ReservaSala(Servicio):
    """Servicio de reserva de salas por hora."""

    def __init__(self, codigo, nombre, tarifa_base, capacidad, disponible=True):
        super().__init__(codigo, nombre, tarifa_base, disponible)
        self._capacidad = self._validar_entero_positivo(capacidad, "capacidad")

    @property
    def capacidad(self):
        return self._capacidad

    def validar_parametros(self):
        return self._capacidad > 0

    def calcular_costo(self, duracion=1, cantidad=1, impuesto=0, descuento=0):
        self._verificar_disponibilidad()
        return self._calcular_total(duracion, cantidad, impuesto, descuento)

    def describir(self):
        return (
            f"Sala {self.codigo}: {self.nombre} | Capacidad: {self.capacidad} personas | "
            f"Tarifa por hora: ${self.tarifa_base:,.2f}"
        )


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos con control de unidades."""

    def __init__(self, codigo, nombre, tarifa_base, unidades_disponibles, disponible=True):
        super().__init__(codigo, nombre, tarifa_base, disponible)
        if (
            isinstance(unidades_disponibles, bool)
            or not isinstance(unidades_disponibles, int)
            or unidades_disponibles < 0
        ):
            raise DatoInvalidoError("Las unidades disponibles deben ser un entero no negativo.")
        self._unidades_disponibles = unidades_disponibles

    @property
    def unidades_disponibles(self):
        return self._unidades_disponibles

    def validar_parametros(self):
        return self._unidades_disponibles >= 0

    def reservar_unidades(self, cantidad):
        cantidad = self._validar_entero_positivo(cantidad, "cantidad")
        self._verificar_disponibilidad()
        if cantidad > self._unidades_disponibles:
            raise ServicioNoDisponibleError("No hay suficientes equipos disponibles.")
        self._unidades_disponibles -= cantidad

    def devolver_unidades(self, cantidad):
        cantidad = self._validar_entero_positivo(cantidad, "cantidad")
        self._unidades_disponibles += cantidad

    def calcular_costo(self, duracion=1, cantidad=1, impuesto=0, descuento=0):
        self._verificar_disponibilidad()
        cantidad = self._validar_entero_positivo(cantidad, "cantidad")
        if cantidad > self._unidades_disponibles:
            raise ServicioNoDisponibleError("No hay suficientes equipos disponibles.")
        return self._calcular_total(duracion, cantidad, impuesto, descuento)

    def describir(self):
        return (
            f"Equipo {self.codigo}: {self.nombre} | Unidades disponibles: "
            f"{self.unidades_disponibles} | Tarifa por dia: ${self.tarifa_base:,.2f}"
        )


class AsesoriaEspecializada(Servicio):
    """Servicio de asesorias profesionales por hora."""

    def __init__(self, codigo, nombre, tarifa_base, especialidad, disponible=True):
        super().__init__(codigo, nombre, tarifa_base, disponible)
        self._especialidad = self.validar_texto(especialidad, "especialidad")

    @property
    def especialidad(self):
        return self._especialidad

    def validar_parametros(self):
        return bool(self._especialidad.strip())

    def calcular_costo(self, duracion=1, cantidad=1, impuesto=0, descuento=0):
        self._verificar_disponibilidad()
        return self._calcular_total(duracion, cantidad, impuesto, descuento)

    def describir(self):
        return (
            f"Asesoria {self.codigo}: {self.nombre} | Especialidad: {self.especialidad} | "
            f"Tarifa por hora: ${self.tarifa_base:,.2f}"
        )
