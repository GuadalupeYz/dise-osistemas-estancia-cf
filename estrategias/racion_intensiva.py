"""
Estrategia de Ración Intensiva
Autor: Guadalupe Yañez

Estrategia de alimentación de alto rendimiento para engorde acelerado.
"""

from estrategias.estrategia_racion import EstrategiaRacion

class RacionIntensiva(EstrategiaRacion):
    """
    Estrategia de alimentación intensiva.
    
    Aplicación:
    - Animales en fase de engorde acelerado
    - Preparación para faena en corto plazo
    - Máximo aprovechamiento del feedlot
    
    Incremento: +2.0 kg por ciclo de alimentación
    """
    
    def __init__(self):
        """Inicializa la estrategia intensiva"""
        self.incremento_base = 2.0
        self.costo_diario = 280.0  # Pesos argentinos (mayor costo)
    
    def aplicar_racion(self, animal) -> float:
        """
        Aplica ración intensiva al animal.
        
        Args:
            animal: Animal a alimentar
            
        Returns:
            float: Incremento de peso (2.0 kg)
        """
        incremento = self.incremento_base
        animal.actualizar_peso(incremento)
        animal.racion_actual = "Intensiva"
        return incremento
    
    def obtener_nombre(self) -> str:
        """Retorna el nombre de la estrategia"""
        return "Ración Intensiva"
    
    def obtener_descripcion(self) -> str:
        """Retorna descripción detallada"""
        return (f"Alimentación de alto rendimiento para engorde acelerado. "
                f"Incremento: +{self.incremento_base} kg/día. "
                f"Costo: ${self.costo_diario}/día. "
                f"Ideal para animales jóvenes en crecimiento.")
    
    def obtener_costo_diario(self) -> float:
        """Retorna el costo diario de la ración"""
        return self.costo_diario
    
    def es_adecuada_para(self, animal) -> bool:
        """
        Determina si es adecuada para el animal.
        
        Args:
            animal: Animal a evaluar
            
        Returns:
            bool: True si el animal está sano y tiene bajo/medio peso
        """
        # Adecuada para animales saludables con peso menor a 350 kg
        # (Terneros y Novillos en crecimiento)
        return not animal.esta_enfermo() and animal.peso < 350
    
    def calcular_rendimiento(self, animal) -> dict:
        """
        Calcula métricas de rendimiento para esta estrategia.
        
        Args:
            animal: Animal a analizar
            
        Returns:
            dict: Métricas de rendimiento
        """
        dias_estimados = (400 - animal.peso) / self.incremento_base
        costo_total = dias_estimados * self.costo_diario
        
        return {
            "dias_hasta_objetivo": dias_estimados,
            "costo_total_estimado": costo_total,
            "peso_objetivo": 400,
            "ganancia_diaria": self.incremento_base
        }
    
    def __str__(self):
        return f"Ración Intensiva (+{self.incremento_base} kg/día) "