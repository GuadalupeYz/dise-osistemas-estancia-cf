"""
Clase Animal - Representa un animal en el feedlot
Autor: Guadalupe Yañez
"""

from datetime import datetime
from typing import Optional

class Animal:
    """
    Representa un animal en el feedlot.
    Mantiene información sobre peso, temperatura y salud.
    """
    
    def __init__(self, id_animal: int, tipo: str, peso_inicial: float):
        """
        Inicializa un nuevo animal
        
        Args:
            id_animal: Identificador único del animal
            tipo: Tipo de animal (Ternero, Novillo, Toro)
            peso_inicial: Peso inicial en kg
        """
        self.id = id_animal
        self.tipo = tipo
        self.peso = peso_inicial
        self.peso_inicial = peso_inicial
        self.temperatura = 38.5  # Temperatura normal del ganado
        self.estado_salud = "Saludable"
        self.racion_actual = None
        self.fecha_ingreso = datetime.now()
        self.dias_en_feedlot = 0
        self.historial_peso = [peso_inicial]
        self.historial_temperatura = [38.5]
        
    def actualizar_peso(self, incremento: float):
        """
        Actualiza el peso del animal
        
        Args:
            incremento: Cantidad de kg a incrementar
        """
        self.peso += incremento
        self.historial_peso.append(self.peso)
        
    def actualizar_temperatura(self, nueva_temp: float):
        """
        Actualiza la temperatura del animal y detecta anomalías
        
        Args:
            nueva_temp: Nueva temperatura en °C
        """
        self.temperatura = nueva_temp
        self.historial_temperatura.append(nueva_temp)
        
        # Detectar problemas de salud
        if nueva_temp >= 39.5:
            self.estado_salud = "Enfermo - Fiebre"
        elif nueva_temp < 37.0:
            self.estado_salud = "Enfermo - Hipotermia"
        else:
            self.estado_salud = "Saludable"
    
    def esta_enfermo(self) -> bool:
        """
        Verifica si el animal está enfermo
        
        Returns:
            True si está enfermo, False si está saludable
        """
        return self.estado_salud != "Saludable"
    
    def ganancia_peso_total(self) -> float:
        """
        Calcula la ganancia total de peso desde el ingreso
        
        Returns:
            Ganancia total en kg
        """
        return self.peso - self.peso_inicial
    
    def ganancia_diaria_promedio(self) -> float:
        """
        Calcula la ganancia diaria promedio (GDP)
        
        Returns:
            GDP en kg/día
        """
        if self.dias_en_feedlot == 0:
            return 0
        return self.ganancia_peso_total() / self.dias_en_feedlot
    
    def mostrar_info(self) -> str:
        """
        Retorna información detallada del animal
        
        Returns:
            String con información formateada
        """
        return (f"[Animal #{self.id}] Tipo: {self.tipo} | "
                f"Peso: {self.peso:.2f} kg | "
                f"Temp: {self.temperatura:.1f}°C | "
                f"Estado: {self.estado_salud} | "
                f"Ganancia: +{self.ganancia_peso_total():.2f} kg")
    
    def __str__(self):
        """Representación en string del animal"""
        return f"Animal #{self.id} ({self.tipo})"
    
    def __repr__(self):
        """Representación para debugging"""
        return f"Animal(id={self.id}, tipo='{self.tipo}', peso={self.peso:.2f}kg)"