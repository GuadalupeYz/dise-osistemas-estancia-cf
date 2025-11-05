"""
Estrategia de Ración de Mantenimiento

Estrategia de alimentación mínima para animales enfermos o en recuperación.
"""

from estrategias.estrategia_racion import EstrategiaRacion

class RacionMantenimiento(EstrategiaRacion):
    """
    Estrategia de alimentación de mantenimiento.
    
    Aplicación:
    - Animales enfermos en recuperación
    - Animales con problemas de salud
    - Período de adaptación al feedlot
    - Situaciones de estrés
    
    Incremento: +0.3 kg por ciclo de alimentación
    """
    
    def __init__(self):
        """Inicializa la estrategia de mantenimiento"""
        self.incremento_base = 0.3
        self.costo_diario = 100.0  # Pesos argentinos (menor costo)
    
    def aplicar_racion(self, animal) -> float:
        """
        Aplica ración de mantenimiento al animal.
        
        Args:
            animal: Animal a alimentar
            
        Returns:
            float: Incremento de peso (0.3 kg)
        """
        incremento = self.incremento_base
        animal.actualizar_peso(incremento)
        animal.racion_actual = "Mantenimiento"
        return incremento
    
    def obtener_nombre(self) -> str:
        """Retorna el nombre de la estrategia"""
        return "Ración de Mantenimiento"
    
    def obtener_descripcion(self) -> str:
        """Retorna descripción detallada"""
        return (f"Alimentación mínima para recuperación y mantenimiento. "
                f"Incremento: +{self.incremento_base} kg/día. "
                f"Costo: ${self.costo_diario}/día. "
                f"Ideal para animales enfermos o en período de adaptación.")
    
    def obtener_costo_diario(self) -> float:
        """Retorna el costo diario de la ración"""
        return self.costo_diario
    
    def es_adecuada_para(self, animal) -> bool:
        """
        Determina si es adecuada para el animal.
        
        Args:
            animal: Animal a evaluar
            
        Returns:
            bool: True si el animal está enfermo o necesita cuidados
        """
        # Adecuada para animales enfermos o con fiebre
        return animal.esta_enfermo() or animal.temperatura >= 39.5
    
    def obtener_recomendaciones(self, animal) -> list:
        """
        Genera recomendaciones específicas para el animal.
        
        Args:
            animal: Animal a evaluar
            
        Returns:
            list: Lista de recomendaciones
        """
        recomendaciones = [
            "Mantener observación veterinaria constante",
            "Proporcionar agua fresca y abundante",
            "Aislar de animales saludables si es necesario",
            "Monitorear temperatura dos veces al día"
        ]
        
        if animal.temperatura >= 39.5:
            recomendaciones.append(" Administrar antipirético bajo supervisión")
            recomendaciones.append(" Control de temperatura cada 4 horas")
        
        if animal.temperatura < 37.0:
            recomendaciones.append(" Proporcionar abrigo y ambiente cálido")
            recomendaciones.append(" Aumentar calorías gradualmente")
        
        return recomendaciones
    
    def tiempo_recuperacion_estimado(self, animal) -> int:
        """
        Estima el tiempo de recuperación del animal.
        
        Args:
            animal: Animal a evaluar
            
        Returns:
            int: Días estimados de recuperación
        """
        if not animal.esta_enfermo():
            return 0
        
        # Estimación basada en la temperatura
        if animal.temperatura >= 40.0:
            return 7  # Fiebre alta: 1 semana
        elif animal.temperatura >= 39.5:
            return 3  # Fiebre moderada: 3 días
        elif animal.temperatura < 37.0:
            return 5  # Hipotermia: 5 días
        else:
            return 2  # Recuperación general
    
    def __str__(self):
        return f"Ración de Mantenimiento (+{self.incremento_base} kg/día) "