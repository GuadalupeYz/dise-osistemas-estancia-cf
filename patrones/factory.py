"""
Patrón Factory - Creación de objetos

"""

from entidades.animal import Animal
from entidades.sensor import SensorPeso, SensorTemperatura
from typing import Tuple, List
import random

class AnimalFactory:
    """
    Factory para crear diferentes tipos de animales con sus sensores.
    Implementa el patrón Factory Method.
    
    Este patrón centraliza la lógica de creación de objetos complejos,
    facilitando el mantenimiento y la extensibilidad.
    """
    
    # Configuración por tipo de animal (rangos de peso iniciales)
    TIPOS_CONFIG = {
        "Ternero": {"peso_min": 150, "peso_max": 220, "descripcion": "Ganado joven"},
        "Novillo": {"peso_min": 250, "peso_max": 350, "descripcion": "Ganado en engorde"},
        "Toro": {"peso_min": 400, "peso_max": 550, "descripcion": "Ganado adulto"}
    }
    
    @staticmethod
    def crear_animal(id_animal: int, tipo: str, peso_inicial: float = None) -> Animal:
        """
        Crea un animal del tipo especificado.
        
        Args:
            id_animal: Identificador único del animal
            tipo: Tipo de animal (Ternero, Novillo, Toro)
            peso_inicial: Peso inicial en kg (opcional)
            
        Returns:
            Objeto Animal creado
            
        Raises:
            ValueError: Si el tipo de animal no es válido
        """
        if tipo not in AnimalFactory.TIPOS_CONFIG:
            tipos_validos = ", ".join(AnimalFactory.TIPOS_CONFIG.keys())
            raise ValueError(
                f"Tipo de animal no válido: '{tipo}'. "
                f"Tipos válidos: {tipos_validos}"
            )
        
        # Si no se especifica peso, usar valor aleatorio del rango
        if peso_inicial is None:
            config = AnimalFactory.TIPOS_CONFIG[tipo]
            peso_inicial = random.uniform(config["peso_min"], config["peso_max"])
        
        # Crear el animal
        animal = Animal(id_animal, tipo, peso_inicial)
        
        # Log de creación
        print(f"[FACTORY] ✓ Creado {tipo} #{id_animal} (peso inicial: {peso_inicial:.1f} kg)")
        
        return animal
    
    @staticmethod
    def crear_sensores(animal: Animal, 
                      intervalo_peso: float = 8.0, 
                      intervalo_temp: float = 6.0) -> Tuple[SensorPeso, SensorTemperatura]:
        """
        Crea y retorna los sensores asociados a un animal.
        
        Args:
            animal: Animal al que se asociarán los sensores
            intervalo_peso: Intervalo de lectura del sensor de peso (segundos)
            intervalo_temp: Intervalo de lectura del sensor de temperatura (segundos)
            
        Returns:
            Tupla (SensorPeso, SensorTemperatura)
        """
        sensor_peso = SensorPeso(animal, intervalo_peso)
        sensor_temp = SensorTemperatura(animal, intervalo_temp)
        
        print(f"[FACTORY] ✓ Sensores creados para {animal}")
        
        return sensor_peso, sensor_temp
    
    @staticmethod
    def crear_animal_completo(id_animal: int, 
                             tipo: str, 
                             peso_inicial: float = None,
                             intervalo_peso: float = 8.0,
                             intervalo_temp: float = 6.0) -> Tuple[Animal, SensorPeso, SensorTemperatura]:
        """
        Crea un animal con todos sus sensores en una sola llamada.
        Este es el método más conveniente para uso general.
        
        Args:
            id_animal: Identificador único del animal
            tipo: Tipo de animal (Ternero, Novillo, Toro)
            peso_inicial: Peso inicial en kg (opcional)
            intervalo_peso: Intervalo del sensor de peso en segundos
            intervalo_temp: Intervalo del sensor de temperatura en segundos
            
        Returns:
            Tupla (Animal, SensorPeso, SensorTemperatura)
        """
        animal = AnimalFactory.crear_animal(id_animal, tipo, peso_inicial)
        sensor_peso, sensor_temp = AnimalFactory.crear_sensores(
            animal, 
            intervalo_peso, 
            intervalo_temp
        )
        
        return animal, sensor_peso, sensor_temp
    
    @staticmethod
    def crear_lote_animales(cantidad: int, 
                           tipo: str, 
                           id_inicial: int = 1) -> List[Tuple[Animal, SensorPeso, SensorTemperatura]]:
        """
        Crea un lote de animales del mismo tipo.
        
        Args:
            cantidad: Cantidad de animales a crear
            tipo: Tipo de animal
            id_inicial: ID inicial para la secuencia
            
        Returns:
            Lista de tuplas (Animal, SensorPeso, SensorTemperatura)
        """
        lote = []
        print(f"\n[FACTORY] Creando lote de {cantidad} {tipo}(s)...")
        
        for i in range(cantidad):
            animal_completo = AnimalFactory.crear_animal_completo(
                id_inicial + i, 
                tipo
            )
            lote.append(animal_completo)
        
        print(f"[FACTORY] Lote completado: {cantidad} animales creados\n")
        return lote
    
    @staticmethod
    def obtener_tipos_disponibles() -> List[str]:
        """
        Retorna lista de tipos de animales disponibles.
        
        Returns:
            Lista de strings con los tipos disponibles
        """
        return list(AnimalFactory.TIPOS_CONFIG.keys())
    
    @staticmethod
    def obtener_info_tipo(tipo: str) -> dict:
        """
        Obtiene información sobre un tipo de animal.
        
        Args:
            tipo: Tipo de animal
            
        Returns:
            Diccionario con información del tipo
        """
        if tipo in AnimalFactory.TIPOS_CONFIG:
            return AnimalFactory.TIPOS_CONFIG[tipo].copy()
        return None