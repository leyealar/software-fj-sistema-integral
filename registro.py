"""Configuracion central del registro de eventos y errores (logs)."""

import logging
from pathlib import Path


def configurar_logger(ruta_archivo="logs/software_fj.log", nombre="SoftwareFJ"):
    """Crea un logger de archivo para conservar eventos y errores del sistema."""
    ruta = Path(ruta_archivo)
    ruta.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(nombre)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Reemplaza los handlers previos para evitar mensajes duplicados.
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()

    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    archivo = logging.FileHandler(ruta, encoding="utf-8")
    archivo.setLevel(logging.INFO)
    archivo.setFormatter(formato)
    logger.addHandler(archivo)

    return logger
