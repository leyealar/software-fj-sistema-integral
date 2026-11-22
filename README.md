# Sistema Integral de Gestion - Software FJ

**Curso:** Programacion (213023) - UNAD  
**Actividad:** Fase 4 - Practicas simuladas  
**Ejercicio 1:** Sistema Integral de Gestion de Clientes, Servicios y Reservas

## Descripcion

Aplicacion de consola desarrollada en Python para administrar clientes, servicios y reservas de Software FJ. La informacion se mantiene en listas internas durante la ejecucion; no se utiliza un motor de base de datos. Los eventos y errores se registran en `logs/software_fj.log`.

## Componentes

- `entidades.py`: clase abstracta `Entidad`.
- `clientes.py`: clase `Cliente` con encapsulacion y validaciones de correo y telefono.
- `servicios.py`: clase abstracta `Servicio` y las clases `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada`.
- `reservas.py`: clase `Reserva` con confirmacion, cancelacion, procesamiento y estados.
- `excepciones.py`: excepciones personalizadas para datos invalidos, duplicados, servicios y reservas.
- `registro.py`: configuracion del archivo de logs.
- `sistema.py`: administracion de listas internas y operaciones del sistema.
- `main.py`: demostracion de 16 operaciones, incluidos casos validos e invalidos.
- `prueba_sistema.py`: 23 pruebas automatizadas con `unittest`.

## Requisitos

Python 3.10 o superior. No se requieren paquetes externos.

## Ejecutar la demostracion

```bash
python main.py
```

## Ejecutar las pruebas

```bash
python -m unittest -v prueba_sistema.py
```

## Manejo de errores y costos

La solucion utiliza excepciones personalizadas, bloques `try/except`, `try/except/else/finally` y encadenamiento con `raise ... from ...`. Los errores y eventos se guardan en `logs/software_fj.log`. El calculo de costos admite distintas variantes mediante parametros opcionales para duracion, cantidad, impuesto y descuento.

## Alcance y transparencia

Esta version se presenta como desarrollo individual construido con base en el enunciado del Anexo 3. Incluye los componentes funcionales del sistema para su revision. No se afirma que exista una integracion con un repositorio grupal ni que el codigo haya sido integrado con los aportes de otros estudiantes. El repositorio individual se utiliza para conservar y compartir el desarrollo realizado por la estudiante.


## Autoria del desarrollo individual

Estudiante: Leidy Yesenia Alvarez Arias - Ingenieria de Sistemas, UNAD.

Este repositorio contiene una implementacion individual basada en el enunciado del Anexo 3. No representa una integracion con el codigo de otros integrantes.
