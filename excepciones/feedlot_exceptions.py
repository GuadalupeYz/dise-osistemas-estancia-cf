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