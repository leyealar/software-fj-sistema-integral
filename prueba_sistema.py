"""Pruebas automatizadas del sistema integral Software FJ."""

import tempfile
import unittest
from pathlib import Path

from clientes import Cliente
from entidades import Entidad
from excepciones import (
    DatoInvalidoError,
    EntidadDuplicadaError,
    OperacionNoPermitidaError,
    ReservaNoValidaError,
    ServicioNoDisponibleError,
)
from reservas import Reserva
from servicios import Servicio, ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from sistema import SistemaSoftwareFJ


class PruebasSistemaSoftwareFJ(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.log = str(Path(self.temp.name) / "software_fj.log")
        self.sistema = SistemaSoftwareFJ(self.log)
        self.cliente = Cliente("C001", "Leidy Alvarez", "leidy@example.com", "3001234567")
        self.sistema.registrar_cliente(self.cliente)
        self.sala = ReservaSala("S001", "Sala principal", 50000, 10)
        self.equipo = AlquilerEquipo("E001", "Proyector", 30000, 3)
        self.asesoria = AsesoriaEspecializada("A001", "Asesoria TI", 80000, "Sistemas")
        for servicio in (self.sala, self.equipo, self.asesoria):
            self.sistema.registrar_servicio(servicio)

    def tearDown(self):
        # Cierra el FileHandler antes de borrar el directorio temporal.
        # En Windows, un archivo abierto no se puede eliminar.
        self.sistema.cerrar()
        self.temp.cleanup()

    def test_entidad_es_abstracta(self):
        with self.assertRaises(TypeError):
            Entidad("X1", "Base")

    def test_servicio_es_abstracta(self):
        with self.assertRaises(TypeError):
            Servicio("S0", "Servicio", 1000)

    def test_registro_cliente_valido(self):
        nuevo = Cliente("C002", "Ana Ruiz", "ana@example.com", "3112345678")
        self.sistema.registrar_cliente(nuevo)
        self.assertEqual(len(self.sistema.clientes), 2)

    def test_correo_invalido(self):
        with self.assertRaises(DatoInvalidoError):
            Cliente("C003", "Ana", "correo-malo", "3112345678")

    def test_telefono_invalido(self):
        with self.assertRaises(DatoInvalidoError):
            Cliente("C003", "Ana", "ana@example.com", "12")

    def test_codigo_cliente_duplicado(self):
        with self.assertRaises(EntidadDuplicadaError):
            self.sistema.registrar_cliente(self.cliente)

    def test_registro_de_tres_servicios(self):
        self.assertEqual(len(self.sistema.servicios), 3)
        self.assertTrue(all(s.validar_parametros() for s in self.sistema.servicios))

    def test_tarifa_negativa_rechazada(self):
        with self.assertRaises(DatoInvalidoError):
            ReservaSala("S099", "Sala invalida", -10, 5)

    def test_cantidad_y_parametros_opcionales_de_calculo(self):
        self.assertEqual(self.sala.calcular_costo(2), 100000.0)
        self.assertEqual(self.equipo.calcular_costo(2, 2), 120000.0)
        self.assertEqual(self.asesoria.calcular_costo(1, 1, 19), 95200.0)
        self.assertEqual(self.sala.calcular_costo(2, 1, 19, 10), 107100.0)

    def test_inventario_negativo_rechazado(self):
        with self.assertRaises(DatoInvalidoError):
            AlquilerEquipo("E099", "Equipo", 1000, -1)

    def test_crear_reserva_correcta(self):
        reserva = self.sistema.crear_reserva("R001", "C001", "S001", 2)
        self.assertEqual(reserva.estado, Reserva.PENDIENTE)
        self.assertEqual(reserva.total, 100000.0)

    def test_reserva_con_cliente_inexistente(self):
        with self.assertRaises(ReservaNoValidaError) as contexto:
            self.sistema.crear_reserva("R002", "C999", "S001", 2)
        self.assertIsNotNone(contexto.exception.__cause__)

    def test_parametro_obligatorio_faltante(self):
        with self.assertRaises(ReservaNoValidaError) as contexto:
            self.sistema.crear_reserva("R002", "C001", "S001")
        self.assertIsInstance(contexto.exception.__cause__, DatoInvalidoError)

    def test_reserva_con_servicio_inexistente(self):
        with self.assertRaises(ReservaNoValidaError):
            self.sistema.crear_reserva("R003", "C001", "S999", 2)

    def test_reserva_no_disponible(self):
        cerrado = ReservaSala("S002", "Sala cerrada", 20000, 5, disponible=False)
        self.sistema.registrar_servicio(cerrado)
        with self.assertRaises(ReservaNoValidaError):
            self.sistema.crear_reserva("R004", "C001", "S002", 1)

    def test_confirmar_y_procesar_reserva(self):
        self.sistema.crear_reserva("R005", "C001", "S001", 1)
        self.assertEqual(self.sistema.confirmar_reserva("R005"), Reserva.CONFIRMADA)
        self.assertEqual(self.sistema.procesar_reserva("R005"), Reserva.PROCESADA)

    def test_no_procesar_sin_confirmar(self):
        self.sistema.crear_reserva("R006", "C001", "S001", 1)
        with self.assertRaises(OperacionNoPermitidaError):
            self.sistema.procesar_reserva("R006")

    def test_inventario_se_descuenta_y_se_restaura_al_cancelar(self):
        self.sistema.crear_reserva("R007", "C001", "E001", 1, cantidad=2)
        self.sistema.confirmar_reserva("R007")
        self.assertEqual(self.equipo.unidades_disponibles, 1)
        self.sistema.cancelar_reserva("R007")
        self.assertEqual(self.equipo.unidades_disponibles, 3)

    def test_reserva_supera_inventario(self):
        with self.assertRaises(ReservaNoValidaError):
            self.sistema.crear_reserva("R008", "C001", "E001", 1, cantidad=5)

    def test_no_disponibilidad_en_servicio(self):
        self.sala.cambiar_disponibilidad(False)
        with self.assertRaises(ServicioNoDisponibleError):
            self.sala.calcular_costo(1)

    def test_no_cancelar_reserva_procesada(self):
        self.sistema.crear_reserva("R009", "C001", "S001", 1)
        self.sistema.confirmar_reserva("R009")
        self.sistema.procesar_reserva("R009")
        with self.assertRaises(OperacionNoPermitidaError):
            self.sistema.cancelar_reserva("R009")

    def test_log_registra_eventos_y_errores(self):
        with self.assertRaises(DatoInvalidoError):
            self.sistema.registrar_cliente(object())
        contenido = Path(self.log).read_text(encoding="utf-8")
        self.assertIn("Cliente registrado: C001", contenido)
        self.assertIn("Error al registrar cliente", contenido)

    def test_servicios_sobrescriben_describir_y_calcular(self):
        self.assertIn("Sala", self.sala.describir())
        self.assertIn("Equipo", self.equipo.describir())
        self.assertIn("Asesoria", self.asesoria.describir())


if __name__ == "__main__":
    unittest.main(verbosity=2)
