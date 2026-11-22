"""
Sistema Integral de Gestión - Software FJ

Estudiante: Leidy Yesenia Álvarez Arias
Programa: Ingeniería de Sistemas
Curso: Programación - 213023
Actividad: Fase 4 - Prácticas simuladas
UNAD
"""

"""Ejecucion de demostracion con mas de diez operaciones simuladas."""

from clientes import Cliente
from excepciones import ErrorSoftwareFJ
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from sistema import SistemaSoftwareFJ


def ejecutar_operacion(numero, titulo, accion):
    """Ejecuta una operacion sin detener la demostracion ante errores esperados."""
    print(f"\nOPERACION {numero}: {titulo}")
    try:
        resultado = accion()
    except ErrorSoftwareFJ as error:
        print(f"Resultado: error controlado - {error}")
    else:
        print(f"Resultado: correcto - {resultado}")
    finally:
        print(f"Fin de la operacion {numero}.")


def ejecutar_demostracion():
    sistema = SistemaSoftwareFJ()
    print("=" * 72)
    print("SISTEMA INTEGRAL DE GESTION - SOFTWARE FJ")
    print("Demostracion de clientes, servicios, reservas y manejo de excepciones")
    print("=" * 72)

    cliente_1 = Cliente("C001", "Laura Gomez", "laura.gomez@example.com", "3001234567")
    cliente_2 = Cliente("C002", "Carlos Ruiz", "carlos.ruiz@example.com", "3017654321")
    sala = ReservaSala("S001", "Sala de reuniones", 50000, 12)
    equipo = AlquilerEquipo("E001", "Proyector multimedia", 30000, 4)
    asesoria = AsesoriaEspecializada("A001", "Asesoria tecnologica", 80000, "Sistemas")

    ejecutar_operacion(1, "Registrar cliente valido", lambda: sistema.registrar_cliente(cliente_1).describir())
    ejecutar_operacion(2, "Rechazar cliente con correo invalido", lambda: sistema.registrar_cliente(
        Cliente("C003", "Ana Torres", "correo-no-valido", "3025557788")
    ).describir())
    ejecutar_operacion(3, "Registrar segundo cliente valido", lambda: sistema.registrar_cliente(cliente_2).describir())
    ejecutar_operacion(4, "Registrar servicio de reserva de sala", lambda: sistema.registrar_servicio(sala).describir())
    ejecutar_operacion(5, "Registrar servicio de alquiler de equipos", lambda: sistema.registrar_servicio(equipo).describir())
    ejecutar_operacion(6, "Registrar servicio de asesoria", lambda: sistema.registrar_servicio(asesoria).describir())
    ejecutar_operacion(7, "Rechazar servicio con tarifa negativa", lambda: sistema.registrar_servicio(
        ReservaSala("S099", "Sala invalida", -1000, 8)
    ).describir())
    ejecutar_operacion(8, "Crear reserva de sala", lambda: sistema.crear_reserva(
        "R001", "C001", "S001", 2, impuesto=19
    ).describir())
    ejecutar_operacion(9, "Confirmar reserva R001", lambda: sistema.confirmar_reserva("R001"))
    ejecutar_operacion(10, "Procesar reserva R001", lambda: sistema.procesar_reserva("R001"))
    ejecutar_operacion(11, "Crear reserva de equipos dentro del inventario", lambda: sistema.crear_reserva(
        "R002", "C002", "E001", 3, cantidad=2, descuento=5
    ).describir())
    ejecutar_operacion(12, "Confirmar reserva de equipos y descontar inventario", lambda: sistema.confirmar_reserva("R002"))
    ejecutar_operacion(13, "Rechazar reserva que supera el inventario restante", lambda: sistema.crear_reserva(
        "R003", "C001", "E001", 2, cantidad=5
    ).describir())
    ejecutar_operacion(14, "Crear reserva de asesoria y cancelarla", lambda: sistema.crear_reserva(
        "R004", "C001", "A001", 1.5, impuesto=19
    ).describir())
    ejecutar_operacion(15, "Cancelar reserva pendiente R004", lambda: sistema.cancelar_reserva("R004"))
    ejecutar_operacion(16, "Rechazar reserva por parametro obligatorio faltante", lambda: sistema.crear_reserva(
        "R005", "C001", "S001"
    ).describir())

    print("\n" + "=" * 72)
    print("RESUMEN FINAL")
    print(sistema.resumen())
    print("Los eventos y errores se registraron en logs/software_fj.log")
    print("La demostracion termino sin detenerse por los errores controlados.")
    print("=" * 72)


if __name__ == "__main__":
    ejecutar_demostracion()
