"""
Clase Corral - Representa un corral que contiene animales
Autor: Guadalupe Yañez
"""

from typing import List, Optional
from entidades.animal import Animal

class Corral:
    """
    Representa un corral que contiene múltiples animales.
    Permite gestionar la capacidad y el estado de los animales.
    """
    
    def __init__(self, numero: int, capacidad: int = 50):
        """
        Inicializa un nuevo corral
        
        Args:
            numero: Número identificador del corral
            capacidad: Capacidad máxima de animales (default: 50)
        """
        self.numero = numero
        self.capacidad = capacidad
        self.animales: List[Animal] = []
        
    def agregar_animal(self, animal: Animal) -> bool:
        """
        Agrega un animal al corral si hay espacio disponible
        
        Args:
            animal: Objeto Animal a agregar
            
        Returns:
            True si se agregó exitosamente, False si el corral está lleno
        """
        if len(self.animales) < self.capacidad:
            self.animales.append(animal)
            return True
        return False
    
    def remover_animal(self, id_animal: int) -> bool:
        """
        Remueve un animal del corral por su ID
        
        Args:
            id_animal: ID del animal a remover
            
        Returns:
            True si se removió exitosamente, False si no se encontró
        """
        for animal in self.animales:
            if animal.id == id_animal:
                self.animales.remove(animal)
                return True
        return False
    
    def obtener_animal(self, id_animal: int) -> Optional[Animal]:
        """
        Obtiene un animal por su ID
        
        Args:
            id_animal: ID del animal a buscar
            
        Returns:
            Objeto Animal si se encuentra, None si no existe
        """
        for animal in self.animales:
            if animal.id == id_animal:
                return animal
        return None
    
    def peso_promedio(self) -> float:
        """
        Calcula el peso promedio de los animales en el corral
        
        Returns:
            Peso promedio en kg
        """
        if not self.animales:
            return 0.0
        return sum(a.peso for a in self.animales) / len(self.animales)
    
    def animales_enfermos(self) -> List[Animal]:
        """
        Retorna lista de animales enfermos en el corral
        
        Returns:
            Lista de animales con estado de salud anormal
        """
        return [a for a in self.animales if a.esta_enfermo()]
    
    def esta_lleno(self) -> bool:
        """
        Verifica si el corral está lleno
        
        Returns:
            True si está en capacidad máxima, False si hay espacio
        """
        return len(self.animales) >= self.capacidad
    
    def obtener_estadisticas(self) -> dict:
        """
        Genera estadísticas del corral
        
        Returns:
            Diccionario con estadísticas del corral
        """
        if not self.animales:
            return {
                "total_animales": 0,
                "peso_promedio": 0,
                "animales_enfermos": 0,
                "capacidad_usada": 0
            }
        
        return {
            "total_animales": len(self.animales),
            "peso_promedio": self.peso_promedio(),
            "animales_enfermos": len(self.animales_enfermos()),
            "capacidad_usada": (len(self.animales) / self.capacidad) * 100
        }
    
    def __str__(self):
        """Representación en string del corral"""
        return f"Corral #{self.numero} ({len(self.animales)}/{self.capacidad})"
    
    def __repr__(self):
        """Representación para debugging"""
        return f"Corral(numero={self.numero}, animales={len(self.animales)}/{self.capacidad})"