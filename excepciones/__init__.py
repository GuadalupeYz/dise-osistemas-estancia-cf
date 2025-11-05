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