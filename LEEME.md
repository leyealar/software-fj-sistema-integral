# LEEME - Software FJ, Fase 4

## Requisitos

- Python 3.10 o superior.
- No se necesitan librerias externas.

## Ejecucion

1. Descargar o clonar el repositorio completo.
2. Abrir una terminal en la carpeta donde se encuentra `main.py`.
3. Ejecutar `python main.py` para realizar las 16 operaciones simuladas.
4. Ejecutar `python -m unittest -v prueba_sistema.py` para ejecutar las 23 pruebas.

## Archivos

El proyecto se separa en modulos: `entidades.py`, `clientes.py`, `servicios.py`, `reservas.py`, `excepciones.py`, `registro.py`, `sistema.py`, `main.py` y `prueba_sistema.py`.

## Logs

La carpeta `logs` se crea automaticamente. El archivo `logs/software_fj.log` registra los eventos y errores de la aplicacion. No se usa una base de datos; los datos se administran mediante objetos y listas internas.

## Nota sobre el trabajo colaborativo

Este paquete contiene el desarrollo individual realizado por Leidy Yesenia Alvarez Arias a partir del enunciado del Anexo 3. Se comparte para su revision. No contiene una integracion con el codigo de los otros integrantes, ya que no se dispuso de los archivos base ni del repositorio grupal en el intercambio documentado.


## Cierre de logs

El sistema dispone del metodo `cerrar()` para vaciar y cerrar el manejador del archivo de logs. Las pruebas lo llaman antes de eliminar sus carpetas temporales; esto evita bloqueos de archivos en Windows.

## Autoria

Desarrollo individual de Leidy Yesenia Alvarez Arias, curso Programacion (213023), UNAD.
