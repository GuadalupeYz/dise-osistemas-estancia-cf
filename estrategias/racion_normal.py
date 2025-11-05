"""
Estrategia de Ración Normal

Estrategia de alimentación estándar para animales en condiciones normales.
"""

from estrategias.estrategia_racion import EstrategiaRacion

class RacionNormal(EstrategiaRacion):
    """
    Estrategia de alimentación normal.
    
    Aplicación:
    - Animales en condiciones estándar
    - Engorde progresivo sin prisa
    - Costo-beneficio equilibrado
    
    Incremento: +1.0 kg por ciclo de alimentación
    """
    
    def __init__(self):
        """Inicializa la estrategia normal"""
        self.incremento_base = 1.0
        self.costo_diario = 150.0  # Pesos argentinos
    
    def aplicar_racion(self, animal) -> float:
        """
        Aplica ración normal al animal.
        
        Args:
            animal: Animal a alimentar
            
        Returns:
            float: Incremento de peso (1.0 kg)
        """
        incremento = self.incremento_base
        animal.actualizar_peso(incremento)
        animal.racion_actual = "Normal"
        return incremento
    
    def obtener_nombre(self) -> str:
        """Retorna el nombre de la estrategia"""
        return "Ración Normal"
    
    def obtener_descripcion(self) -> str:
        """Retorna descripción detallada"""
        return (f"Alimentación estándar para engorde progresivo. "
                f"Incremento: +{self.incremento_base} kg/día. "
                f"Costo: ${self.costo_diario}/día")
    
    def obtener_costo_diario(self) -> float:
        """Retorna el costo diario de la ración"""
        return self.costo_diario
    
    def es_adecuada_para(self, animal) -> bool:
        """
        Determina si es adecuada para el animal.
        
        Args:
            animal: Animal a evaluar
            
        Returns:
            bool: True si el animal está sano y en peso medio
        """
        # Adecuada para animales saludables en cualquier peso
        return not animal.esta_enfermo()
    
    def __str__(self):
        return f"Ración Normal (+{self.incremento_base} kg/día)"