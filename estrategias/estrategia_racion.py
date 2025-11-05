"""
Patrón Strategy - Interfaz para estrategias de alimentación
Autor: Guadalupe Yañez

El patrón Strategy define una familia de algoritmos (estrategias de alimentación),
los encapsula y los hace intercambiables. Permite que el algoritmo varíe
independientemente de los clientes que lo utilizan.
"""

from abc import ABC, abstractmethod

class EstrategiaRacion(ABC):
    """
    Interfaz abstracta para el patrón Strategy.
    
    Define el contrato que todas las estrategias de alimentación
    deben implementar.
    
    Cada estrategia concreta implementará su propio algoritmo
    de alimentación con diferentes incrementos de peso.
    """
    
    @abstractmethod
    def aplicar_racion(self, animal) -> float:
        """
        Aplica la estrategia de alimentación al animal.
        
        Este es el método principal que debe ser implementado
        por cada estrategia concreta.
        
        Args:
            animal: Objeto Animal al que se aplicará la ración
            
        Returns:
            float: Incremento de peso esperado en kg
        """
        pass
    
    @abstractmethod
    def obtener_nombre(self) -> str:
        """
        Retorna el nombre de la estrategia.
        
        Returns:
            str: Nombre descriptivo de la estrategia
        """
        pass
    
    @abstractmethod
    def obtener_descripcion(self) -> str:
        """
        Retorna una descripción detallada de la estrategia.
        
        Returns:
            str: Descripción de la estrategia y sus efectos
        """
        pass
    
    def obtener_costo_diario(self) -> float:
        """
        Retorna el costo diario estimado de la ración (opcional).
        
        Returns:
            float: Costo en pesos/día (puede ser sobrescrito)
        """
        return 0.0
    
    def es_adecuada_para(self, animal) -> bool:
        """
        Determina si esta estrategia es adecuada para el animal (opcional).
        
        Args:
            animal: Animal a evaluar
            
        Returns:
            bool: True si la estrategia es adecuada
        """
        return True
    
    def __str__(self):
        """Representación en string de la estrategia"""
        return self.obtener_nombre()
    
    def __repr__(self):
        """Representación para debugging"""
        return f"{self.__class__.__name__}()"