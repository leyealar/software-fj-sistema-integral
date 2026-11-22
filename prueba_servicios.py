"""Pruebas automaticas del modulo 3 - Servicios (Software FJ)."""

import unittest

from servicios import (
    Servicio,
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
)


class PruebasModuloServicios(unittest.TestCase):
    def setUp(self):
        self.sala = ReservaSala("S01", "Sala de reuniones", 50000, 10)
        self.equipo = AlquilerEquipo("E01", "Proyector multimedia", 30000, 5)
        self.asesoria = AsesoriaEspecializada(
            "A01", "Asesoria tecnologica", 80000, "Sistemas"
        )

    def test_servicio_es_abstracta(self):
        with self.assertRaises(TypeError):
            Servicio("X01", "Servicio", 1000)

    def test_descripcion_y_validacion_de_los_tres_servicios(self):
        for servicio in (self.sala, self.equipo, self.asesoria):
            self.assertTrue(servicio.validar_parametros())
            self.assertIsInstance(servicio.describir(), str)
            self.assertTrue(servicio.describir())

    def test_calculo_costo_sala(self):
        self.assertEqual(self.sala.calcular_costo(duracion=2), 100000.00)

    def test_calculo_costo_equipo_con_cantidad(self):
        self.assertEqual(
            self.equipo.calcular_costo(duracion=3, cantidad=2), 180000.00
        )

    def test_calculo_costo_asesoria_con_impuesto(self):
        self.assertEqual(
            self.asesoria.calcular_costo(duracion=2, impuesto=19), 190400.00
        )

    def test_calculo_con_impuesto_y_descuento(self):
        self.assertEqual(
            self.sala.calcular_costo(duracion=2, impuesto=19, descuento=10),
            107100.00,
        )

    def test_rechaza_texto_vacio(self):
        with self.assertRaises(ValueError):
            ReservaSala("S02", " ", 40000, 8)

    def test_rechaza_tarifa_negativa(self):
        with self.assertRaises(ValueError):
            ReservaSala("S03", "Sala", -50000, 8)

    def test_rechaza_tarifa_no_finita(self):
        for tarifa in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(tarifa=tarifa):
                with self.assertRaises(ValueError):
                    ReservaSala("S04", "Sala", tarifa, 8)

    def test_rechaza_capacidad_no_positiva(self):
        with self.assertRaises(ValueError):
            ReservaSala("S05", "Sala", 40000, 0)

    def test_rechaza_inventario_negativo(self):
        with self.assertRaises(ValueError):
            AlquilerEquipo("E02", "Portatil", 30000, -1)

    def test_rechaza_especialidad_vacia(self):
        with self.assertRaises(ValueError):
            AsesoriaEspecializada("A02", "Asesoria", 80000, "")

    def test_rechaza_duracion_negativa_o_cero(self):
        for duracion in (-2, 0):
            with self.subTest(duracion=duracion):
                with self.assertRaises(ValueError):
                    self.sala.calcular_costo(duracion=duracion)

    def test_rechaza_cantidad_mayor_al_inventario(self):
        with self.assertRaises(ValueError):
            self.equipo.calcular_costo(duracion=2, cantidad=6)

    def test_rechaza_porcentajes_fuera_de_rango(self):
        for kwargs in ({"impuesto": 150}, {"descuento": -10}, {"descuento": 101}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    self.sala.calcular_costo(duracion=2, **kwargs)

    def test_rechaza_servicio_no_disponible(self):
        sala = ReservaSala("S06", "Sala cerrada", 40000, 8, disponible=False)
        equipo = AlquilerEquipo("E03", "Equipo", 20000, 3, disponible=False)
        asesoria = AsesoriaEspecializada(
            "A03", "Asesoria", 50000, "Redes", disponible=False
        )
        for servicio in (sala, equipo, asesoria):
            with self.subTest(servicio=servicio.codigo):
                with self.assertRaises(ValueError):
                    servicio.calcular_costo(duracion=1)

    def test_no_modifica_inventario_al_calcular(self):
        unidades_iniciales = self.equipo.unidades_disponibles
        self.equipo.calcular_costo(duracion=2, cantidad=2)
        self.assertEqual(self.equipo.unidades_disponibles, unidades_iniciales)


if __name__ == "__main__":
    unittest.main(verbosity=2)
