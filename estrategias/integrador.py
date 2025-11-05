"""
Archivo integrador generado automaticamente
Directorio: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./estrategias
Fecha: 2025-11-05 20:04:58
Total de archivos integrados: 5
"""

# ================================================================================
# ARCHIVO 1/5: __init__.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./estrategias/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/5: estrategia_racion.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./estrategias/estrategia_racion.py
# ================================================================================

"""
Patrón Strategy - Interfaz para estrategias de alimentación

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

# ================================================================================
# ARCHIVO 3/5: racion_intensiva.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./estrategias/racion_intensiva.py
# ================================================================================

"""
Estrategia de Ración Intensiva

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

# ================================================================================
# ARCHIVO 4/5: racion_mantenimiento.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./estrategias/racion_mantenimiento.py
# ================================================================================

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

# ================================================================================
# ARCHIVO 5/5: racion_normal.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./estrategias/racion_normal.py
# ================================================================================

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

