"""Clase abstracta base para las entidades del sistema Software FJ."""

from abc import ABC, abstractmethod

from excepciones import DatoInvalidoError


class Entidad(ABC):
    """Representa una entidad general identificada por codigo y nombre."""

    def __init__(self, codigo, nombre):
        self._codigo = self.validar_texto(codigo, "codigo")
        self._nombre = self.validar_texto(nombre, "nombre")

    @staticmethod
    def validar_texto(valor, campo):
        """Valida que el campo sea texto y no este vacio."""
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError(f"El campo {campo} es obligatorio.")
        return valor.strip()

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @abstractmethod
    def describir(self):
        """Devuelve una descripcion legible de la entidad."""
        raise NotImplementedError

    def __str__(self):
        return self.describir()
