"""
Archivo integrador generado automaticamente
Directorio: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./excepciones
Fecha: 2025-11-05 20:04:58
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./excepciones/__init__.py
# ================================================================================

"""
Módulo de excepciones personalizadas
"""

from .feedlot_exceptions import (
    FeedlotException,
    AnimalNoEncontradoException,
    CorralNoEncontradoException,
    CorralLlenoException,
    PersistenciaException,
    EstrategiaInvalidaException,
    SensorException
)

__all__ = [
    'FeedlotException',
    'AnimalNoEncontradoException',
    'CorralNoEncontradoException',
    'CorralLlenoException',
    'PersistenciaException',
    'EstrategiaInvalidaException',
    'SensorException'
]

# ================================================================================
# ARCHIVO 2/2: feedlot_exceptions.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./excepciones/feedlot_exceptions.py
# ================================================================================

"""
Excepciones personalizadas del sistema de feedlot
"""

class FeedlotException(Exception):
    """Excepción base del sistema de feedlot"""
    pass


class AnimalNoEncontradoException(FeedlotException):
    """Se lanza cuando un animal no existe en el sistema"""
    pass


class CorralNoEncontradoException(FeedlotException):
    """Se lanza cuando un corral no existe en el sistema"""
    pass


class CorralLlenoException(FeedlotException):
    """Se lanza cuando un corral está en capacidad máxima"""
    pass


class PersistenciaException(FeedlotException):
    """Se lanza cuando hay error al guardar/cargar datos"""
    pass


class EstrategiaInvalidaException(FeedlotException):
    """Se lanza cuando una estrategia no es válida para el animal"""
    pass


class SensorException(FeedlotException):
    """Se lanza cuando hay error en los sensores"""
    pass

