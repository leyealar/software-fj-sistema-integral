"""Pruebas manuales de los tres servicios especializados de Software FJ."""

from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from excepciones import DatoInvalidoError, ServicioNoDisponibleError


def ejecutar_pruebas_servicios():
    print("=" * 60)
    print("PRUEBAS DEL MODULO DE SERVICIOS - SOFTWARE FJ")
    print("=" * 60)

    sala = ReservaSala("S01", "Sala de reuniones", 50000, 10)
    equipo = AlquilerEquipo("E01", "Proyector multimedia", 30000, 5)
    asesoria = AsesoriaEspecializada("A01", "Asesoria tecnologica", 80000, "Sistemas")
    servicios = [sala, equipo, asesoria]

    print("\n--- DESCRIPCION Y VALIDACION ---")
    for servicio in servicios:
        print(servicio.describir())
        print("Parametros validos:", servicio.validar_parametros())

    print("\n--- CALCULO DE COSTOS ---")
    print("Reserva de sala (2 horas):", sala.calcular_costo(duracion=2))
    print("Alquiler de 2 equipos por 3 dias:", equipo.calcular_costo(duracion=3, cantidad=2))
    print("Asesoria (2 horas con 19% de impuesto):", asesoria.calcular_costo(duracion=2, impuesto=19))
    print("Sala con impuesto y descuento:", sala.calcular_costo(duracion=2, impuesto=19, descuento=10))

    print("\n--- ERRORES CONTROLADOS ---")
    casos = [
        ("Duracion negativa", lambda: sala.calcular_costo(duracion=-2), DatoInvalidoError),
        ("Cantidad mayor al inventario", lambda: equipo.calcular_costo(duracion=2, cantidad=10), ServicioNoDisponibleError),
        ("Especialidad vacia", lambda: AsesoriaEspecializada("A02", "Asesoria", 80000, ""), DatoInvalidoError),
        ("Sala no disponible", lambda: ReservaSala("S02", "Sala cerrada", 40000, 8, disponible=False).calcular_costo(2), ServicioNoDisponibleError),
        ("Impuesto fuera de rango", lambda: sala.calcular_costo(duracion=2, impuesto=150), DatoInvalidoError),
        ("Descuento negativo", lambda: sala.calcular_costo(duracion=2, descuento=-10), DatoInvalidoError),
        ("Tarifa negativa", lambda: ReservaSala("S03", "Sala invalida", -50000, 10), DatoInvalidoError),
    ]
    for titulo, accion, tipo_error in casos:
        try:
            accion()
        except tipo_error as error:
            print(f"{titulo}: error controlado - {error}")
        else:
            print(f"{titulo}: ERROR, se esperaba una excepcion.")

    print("\nFin de las pruebas manuales del modulo de servicios.")


if __name__ == "__main__":
    ejecutar_pruebas_servicios()
