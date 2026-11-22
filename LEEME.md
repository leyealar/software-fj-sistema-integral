# Modulo 3 - Servicios | Software FJ

## Archivos

- `servicios.py`: clase abstracta `Servicio` y las clases `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada`.
- `prueba_servicios.py`: pruebas automaticas de comportamiento, calculo de costos y validacion de errores.

## Requisitos

Python 3. No requiere instalar paquetes externos; utiliza `abc`, `math` y `unittest` de la biblioteca estandar.

## Como ejecutar

Desde una terminal ubicada en esta carpeta:

```bash
python -m unittest -v prueba_servicios.py
```

Tambien se puede ejecutar directamente:

```bash
python prueba_servicios.py
```

## Ejemplo de uso

```python
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada

sala = ReservaSala("S01", "Sala de reuniones", 50000, 10)
equipo = AlquilerEquipo("E01", "Proyector multimedia", 30000, 5)
asesoria = AsesoriaEspecializada("A01", "Asesoria tecnologica", 80000, "Sistemas")

print(sala.describir())
print(sala.calcular_costo(duracion=2, impuesto=19, descuento=10))
print(equipo.calcular_costo(duracion=3, cantidad=2))
print(asesoria.calcular_costo(duracion=2))
```

## Decisiones de implementacion

- `Servicio` es una clase abstracta. No se crean objetos directamente de ella.
- Las tres clases concretas heredan de `Servicio` y redefinen `calcular_costo`, `describir` y `validar_parametros`; esto permite aplicar herencia y polimorfismo.
- Los atributos se mantienen encapsulados y se consultan mediante propiedades de solo lectura.
- Las validaciones rechazan textos vacios, tarifas no positivas, numeros no finitos, duraciones incorrectas, cantidades fuera de rango, porcentajes distintos del intervalo 0 a 100 y servicios no disponibles.
- `calcular_costo` acepta parametros opcionales de cantidad, impuesto y descuento para ofrecer distintas formas de calcular el valor sin duplicar metodos.
- El modulo utiliza `ValueError` para los datos u operaciones no validas. En la integracion, el responsable del modulo de excepciones puede sustituir estas excepciones por las excepciones personalizadas del proyecto.
- El registro central de eventos y errores debe conectarse con el manejador de logs del proyecto grupal para evitar crear registros duplicados o incompatibles.

## Indicacion para integrar con el proyecto grupal

Este modulo se entrega de forma independiente. Para integrarlo:

1. Revisar la clase `Entidad` del proyecto y decidir si `Servicio` debe heredar de ella, en lugar de inicializar por separado `codigo` y `nombre`.
2. Adaptar las validaciones para utilizar las excepciones personalizadas definidas por el equipo, conservando los mensajes y condiciones de validacion.
3. Conectar el registro de errores y eventos con el archivo de logs central del proyecto.
4. Mantener los nombres de las clases y metodos o actualizar los imports del programa principal si el equipo acuerda otros nombres.
5. Ejecutar nuevamente las pruebas del modulo y las pruebas generales del sistema despues de la integracion.

**Importante:** la integracion con `Entidad`, las excepciones personalizadas y el archivo de logs depende de los archivos centrales del equipo, que no hacen parte de este modulo independiente.
