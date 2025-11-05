"""
Patrón Singleton - Garantiza una única instancia
"""

import threading

class SingletonMeta(type):
    """
    Metaclase para implementar el patrón Singleton thread-safe.
    
    Esta metaclase garantiza que solo exista una instancia de la clase
    que la utilice, incluso en entornos multi-threaded.
    
    Uso:
        class MiClase(metaclass=SingletonMeta):
            pass
        
        # Siempre retorna la misma instancia
        obj1 = MiClase()
        obj2 = MiClase()
        assert obj1 is obj2  # True
    """
    
    _instances = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        """
        Thread-safe singleton implementation.
        
        Si la instancia no existe, la crea bajo un lock para evitar
        condiciones de carrera en entornos multi-threaded.
        """
        # Double-checked locking pattern
        if cls not in cls._instances:
            with cls._lock:
                # Verificar nuevamente dentro del lock
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        
        return cls._instances[cls]
    
    @classmethod
    def reset_instances(cls):
        """
        Método para resetear todas las instancias.
        Útil para testing.
        """
        with cls._lock:
            cls._instances.clear()