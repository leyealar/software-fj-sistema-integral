"""Modelo de cliente con atributos encapsulados y validaciones."""

import re

from entidades import Entidad
from excepciones import DatoInvalidoError


class Cliente(Entidad):
    """Cliente de Software FJ. Sus datos se consultan mediante propiedades."""

    def __init__(self, codigo, nombre, correo, telefono):
        super().__init__(codigo, nombre)
        self._correo = self._validar_correo(correo)
        self._telefono = self._validar_telefono(telefono)

    @staticmethod
    def _validar_correo(correo):
        if not isinstance(correo, str):
            raise DatoInvalidoError("El correo debe ser texto.")
        correo = correo.strip().lower()
        patron = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        if not re.match(patron, correo):
            raise DatoInvalidoError("El correo electronico no tiene un formato valido.")
        return correo

    @staticmethod
    def _validar_telefono(telefono):
        if not isinstance(telefono, str):
            raise DatoInvalidoError("El telefono debe ingresarse como texto.")
        telefono_limpio = re.sub(r"[\s()+-]", "", telefono)
        if not telefono_limpio.isdigit() or not 7 <= len(telefono_limpio) <= 15:
            raise DatoInvalidoError("El telefono debe contener entre 7 y 15 digitos.")
        return telefono.strip()

    @property
    def correo(self):
        return self._correo

    @property
    def telefono(self):
        return self._telefono

    def describir(self):
        return (
            f"Cliente {self.codigo}: {self.nombre} | "
            f"Correo: {self.correo} | Telefono: {self.telefono}"
        )
