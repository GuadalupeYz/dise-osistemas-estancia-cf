"""
Archivo integrador generado automaticamente
Directorio: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./patrones
Fecha: 2025-11-05 09:19:07
Total de archivos integrados: 5
"""

# ================================================================================
# ARCHIVO 1/5: __init__.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./patrones/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/5: factory.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./patrones/factory.py
# ================================================================================

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

# ================================================================================
# ARCHIVO 3/5: observer.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./patrones/observer.py
# ================================================================================

"""
Patrón Observer - Sistema de notificaciones
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict

class Observador(ABC):
    """
    Interfaz para el patrón Observer.
    
    Los observadores se suscriben a sujetos (sensores) y son notificados
    cuando ocurren eventos de interés.
    """
    
    @abstractmethod
    def actualizar(self, animal, mensaje: str, tipo: str):
        """
        Método que se llama cuando hay una notificación.
        
        Args:
            animal: Animal relacionado con la notificación
            mensaje: Mensaje descriptivo del evento
            tipo: Tipo de alerta (FIEBRE, BAJO_RENDIMIENTO, etc.)
        """
        pass


class ObservadorAlerta(Observador):
    """
    Observador concreto que maneja alertas del sistema.
    
    Registra eventos críticos, muestra alertas en consola
    y puede tomar acciones automáticas.
    """
    
    def __init__(self):
        """Inicializa el observador de alertas"""
        self.alertas: List[Dict] = []
        self.alertas_activas = 0
        self.alertas_por_tipo: Dict[str, int] = {}
        
    def actualizar(self, animal, mensaje: str, tipo: str):
        """
        Recibe notificación de un sensor y procesa la alerta.
        
        Args:
            animal: Animal relacionado
            mensaje: Descripción del evento
            tipo: Tipo de alerta
        """
        # Crear registro de alerta
        alerta = {
            "timestamp": datetime.now(),
            "animal_id": animal.id,
            "animal_tipo": animal.tipo,
            "mensaje": mensaje,
            "tipo": tipo,
            "peso_actual": animal.peso,
            "temperatura": animal.temperatura,
            "estado_salud": animal.estado_salud
        }
        
        # Agregar a la lista de alertas
        self.alertas.append(alerta)
        self.alertas_activas += 1
        
        # Contar por tipo
        self.alertas_por_tipo[tipo] = self.alertas_por_tipo.get(tipo, 0) + 1
        
        # Mostrar alerta en consola
        self._mostrar_alerta(alerta)
        
        # Tomar acciones según el tipo
        self._tomar_accion(animal, tipo)
    
    def _mostrar_alerta(self, alerta: Dict):
        """Muestra una alerta formateada en consola"""
        hora = alerta["timestamp"].strftime("%H:%M:%S")
    
        print("\n" + "="*70)
        print(f"ALERTA [{alerta['tipo']}] - {hora}")
        print(f"Animal: #{alerta['animal_id']} ({alerta['animal_tipo']})")
        print(f"Mensaje: {alerta['mensaje']}")
        print(f"Estado: Peso {alerta['peso_actual']:.1f} kg | "
          f"Temp {alerta['temperatura']:.1f}°C | "
          f"Salud: {alerta['estado_salud']}")
        print("="*70 + "\n")
    
    def _obtener_icono(self, tipo: str) -> str:
        """Retorna string vacío (sin emojis)"""
        return 
    
    def _tomar_accion(self, animal, tipo: str):
        """
        Toma acciones automáticas según el tipo de alerta.
        
        Args:
            animal: Animal afectado
            tipo: Tipo de alerta
        """
        if tipo == "FIEBRE":
            print(f"[ACCIÓN]  Separando {animal} para tratamiento veterinario...")
            print(f"[ACCIÓN]  Administrando antipirético...")
            animal.estado_salud = "En tratamiento - Fiebre"
            
        elif tipo == "BAJO_RENDIMIENTO":
            print(f"[ACCIÓN]  Revisando alimentación de {animal}...")
            print(f"[ACCIÓN]  Programando análisis nutricional...")
            
        elif tipo == "HIPOTERMIA":
            print(f"[ACCIÓN]  Proporcionando abrigo a {animal}...")
            print(f"[ACCIÓN]  Suministrando alimento calórico...")
            animal.estado_salud = "En tratamiento - Hipotermia"
    
    def obtener_resumen_alertas(self) -> str:
        """Genera un resumen de las alertas registradas"""
        if not self.alertas:
           return "No hay alertas registradas."
    
        resumen = f"\n RESUMEN DE ALERTAS (Total: {len(self.alertas)})\n"
        resumen += "-" * 50 + "\n"
    
    # Mostrar por tipo (SIN emojis)
        for tipo, cantidad in sorted(self.alertas_por_tipo.items()):
            resumen += f"• {tipo}: {cantidad} alerta(s)\n"  # <-- Sin icono
    
    # Animales más afectados
        animales_con_alertas = {}
        for alerta in self.alertas:
            animal_id = alerta["animal_id"]
            animales_con_alertas[animal_id] = animales_con_alertas.get(animal_id, 0) + 1
    
        if animales_con_alertas:
           resumen += "\nAnimales con más alertas:\n"
           for animal_id, count in sorted(animales_con_alertas.items(), 
                                      key=lambda x: x[1], 
                                      reverse=True)[:3]:
               resumen += f"  Animal #{animal_id}: {count} alerta(s)\n"
    
        return resumen
    
    def obtener_alertas_recientes(self, cantidad: int = 5) -> List[Dict]:
        """
        Obtiene las alertas más recientes.
        
        Args:
            cantidad: Número de alertas a retornar
            
        Returns:
            Lista con las últimas alertas
        """
        return self.alertas[-cantidad:] if self.alertas else []
    
    def obtener_alertas_por_tipo(self, tipo: str) -> List[Dict]:
        """
        Filtra alertas por tipo.
        
        Args:
            tipo: Tipo de alerta a filtrar
            
        Returns:
            Lista de alertas del tipo especificado
        """
        return [a for a in self.alertas if a["tipo"] == tipo]
    
    def obtener_alertas_por_animal(self, animal_id: int) -> List[Dict]:
        """
        Filtra alertas por animal.
        
        Args:
            animal_id: ID del animal
            
        Returns:
            Lista de alertas del animal
        """
        return [a for a in self.alertas if a["animal_id"] == animal_id]
    
    def limpiar_alertas(self):
        """Limpia todas las alertas registradas"""
        self.alertas.clear()
        self.alertas_activas = 0
        self.alertas_por_tipo.clear()
        print(" Alertas limpiadas")
    
    def exportar_alertas(self, archivo: str = "alertas.txt"):
        """
        Exporta las alertas a un archivo de texto.
        
        Args:
            archivo: Nombre del archivo de salida
        """
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write("="*70 + "\n")
                f.write("REGISTRO DE ALERTAS - ESTANCIA CARNES FINAS\n")
                f.write("="*70 + "\n\n")
                
                for alerta in self.alertas:
                    f.write(f"Fecha: {alerta['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Tipo: {alerta['tipo']}\n")
                    f.write(f"Animal: #{alerta['animal_id']} ({alerta['animal_tipo']})\n")
                    f.write(f"Mensaje: {alerta['mensaje']}\n")
                    f.write(f"Estado: Peso {alerta['peso_actual']:.1f} kg, "
                           f"Temp {alerta['temperatura']:.1f}°C\n")
                    f.write("-"*70 + "\n\n")
                
                f.write(self.obtener_resumen_alertas())
            
            print(f" Alertas exportadas a: {archivo}")
        except Exception as e:
            print(f" Error al exportar alertas: {e}")

# ================================================================================
# ARCHIVO 4/5: salud_observer.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./patrones/salud_observer.py
# ================================================================================

"""
Observador de Salud - Observer pattern avanzado
Observer más robusto que toma acciones automáticas sobre los animales.
Similar al controlador de riego del sistema forestal.
"""

from patrones.observer import Observador
from datetime import datetime
from typing import List, Dict

class SaludObserver(Observador):
    """
    Observador especializado en salud animal.
    
    Funcionalidades:
    - Monitoreo continuo de temperatura y peso
    - Acciones automáticas ante alertas
    - Registro de tratamientos
    - Cambio automático de estado de salud
    - Notificaciones al veterinario
    """
    
    def __init__(self, log_service=None):
        """
        Inicializa el observador de salud.
        
        Args:
            log_service: Servicio de log opcional
        """
        self.alertas_salud: List[Dict] = []
        self.animales_en_tratamiento: Dict[int, Dict] = {}
        self.tratamientos_aplicados = 0
        self.log_service = log_service
        
        print(" Observador de Salud activado")
    
    def actualizar(self, animal, mensaje: str, tipo: str):
        """
        Recibe notificación y toma acciones automáticas.
        
        Args:
            animal: Animal que generó la alerta
            mensaje: Mensaje descriptivo
            tipo: Tipo de alerta
        """
        # Registrar alerta
        alerta = {
            'timestamp': datetime.now(),
            'animal_id': animal.id,
            'tipo': tipo,
            'mensaje': mensaje,
            'temperatura': animal.temperatura,
            'peso': animal.peso,
            'estado_previo': animal.estado_salud
        }
        self.alertas_salud.append(alerta)
        
        # Log si está disponible
        if self.log_service:
            self.log_service.registrar_alerta_salud(animal, tipo, animal.temperatura)
        
        # Tomar acciones según el tipo
        self._tomar_accion_automatica(animal, tipo, alerta)
    
    def _tomar_accion_automatica(self, animal, tipo: str, alerta: Dict):
        """
        Toma acciones automáticas según el tipo de alerta.
        
        Args:
            animal: Animal afectado
            tipo: Tipo de alerta
            alerta: Diccionario con datos de la alerta
        """
        estado_anterior = animal.estado_salud
        
        if tipo == "FIEBRE":
            self._tratar_fiebre(animal)
            
        elif tipo == "HIPOTERMIA":
            self._tratar_hipotermia(animal)
            
        elif tipo == "BAJO_RENDIMIENTO":
            self._mejorar_alimentacion(animal)
        
        # Registrar cambio de estado si hubo
        if animal.estado_salud != estado_anterior:
            if self.log_service:
                self.log_service.registrar_cambio_estado(animal, estado_anterior, animal.estado_salud)
    
    def _tratar_fiebre(self, animal):
        """
        Protocolo automático para tratamiento de fiebre.
        
        Args:
            animal: Animal con fiebre
        """
        print(f"\n [SALUD] Protocolo de fiebre activado para Animal #{animal.id}")
        
        # Cambiar estado
        animal.estado_salud = "En tratamiento - Fiebre"
        
        # Registrar tratamiento
        tratamiento = {
            'tipo': 'fiebre',
            'inicio': datetime.now(),
            'animal_id': animal.id,
            'temperatura_inicial': animal.temperatura,
            'acciones': [
                "Separación del lote",
                "Administración de antipirético",
                "Hidratación reforzada",
                "Monitoreo cada 4 horas"
            ]
        }
        self.animales_en_tratamiento[animal.id] = tratamiento
        self.tratamientos_aplicados += 1
        
        # Mostrar acciones
        print(f"    Separando {animal} del lote principal")
        print(f"    Administrando antipirético")
        print(f"    Reforzando hidratación")
        print(f"    Programando monitoreo intensivo")
        
        if self.log_service:
            self.log_service.ok(f"Tratamiento de fiebre iniciado - Animal #{animal.id}")
    
    def _tratar_hipotermia(self, animal):
        """
        Protocolo automático para tratamiento de hipotermia.
        
        Args:
            animal: Animal con hipotermia
        """
        print(f"\n [SALUD] Protocolo de hipotermia activado para Animal #{animal.id}")
        
        # Cambiar estado
        animal.estado_salud = "En tratamiento - Hipotermia"
        
        # Registrar tratamiento
        tratamiento = {
            'tipo': 'hipotermia',
            'inicio': datetime.now(),
            'animal_id': animal.id,
            'temperatura_inicial': animal.temperatura,
            'acciones': [
                "Traslado a zona climatizada",
                "Provisión de abrigo",
                "Alimento calórico concentrado",
                "Monitoreo continuo"
            ]
        }
        self.animales_en_tratamiento[animal.id] = tratamiento
        self.tratamientos_aplicados += 1
        
        # Mostrar acciones
        print(f"    Trasladando {animal} a zona climatizada")
        print(f"    Proporcionando abrigo térmico")
        print(f"    Suministrando alimento calórico")
        
        if self.log_service:
            self.log_service.ok(f"Tratamiento de hipotermia iniciado - Animal #{animal.id}")
    
    def _mejorar_alimentacion(self, animal):
        """
        Protocolo para mejorar alimentación ante bajo rendimiento.
        
        Args:
            animal: Animal con bajo rendimiento
        """
        print(f"\n [SALUD] Revisión nutricional para Animal #{animal.id}")
        
        # No cambiar estado a enfermo, solo advertencia
        if animal.estado_salud == "Saludable":
            animal.estado_salud = "Bajo observación"
        
        print(f"    Programando análisis nutricional")
        print(f"    Revisando calidad del alimento")
        print(f"    Evaluando suplementación")
        
        if self.log_service:
            self.log_service.warning(f"Bajo rendimiento detectado - Animal #{animal.id}")
    
    def verificar_recuperacion(self, animal) -> bool:
        """
        Verifica si un animal en tratamiento se ha recuperado.
        
        Args:
            animal: Animal a verificar
            
        Returns:
            bool: True si se recuperó
        """
        if animal.id not in self.animales_en_tratamiento:
            return False
        
        tratamiento = self.animales_en_tratamiento[animal.id]
        
        # Criterios de recuperación
        if tratamiento['tipo'] == 'fiebre':
            if animal.temperatura < 39.0:
                self._dar_alta(animal, tratamiento)
                return True
                
        elif tratamiento['tipo'] == 'hipotermia':
            if animal.temperatura > 37.5:
                self._dar_alta(animal, tratamiento)
                return True
        
        return False
    
    def _dar_alta(self, animal, tratamiento: Dict):
        """
        Da de alta a un animal recuperado.
        
        Args:
            animal: Animal recuperado
            tratamiento: Datos del tratamiento
        """
        duracion = datetime.now() - tratamiento['inicio']
        
        print(f"\n [SALUD] Alta médica - Animal #{animal.id}")
        print(f"   Tipo: {tratamiento['tipo'].capitalize()}")
        print(f"   Duración: {duracion.seconds // 3600}h {(duracion.seconds % 3600) // 60}m")
        print(f"   Estado: Recuperado")
        
        # Cambiar estado
        animal.estado_salud = "Saludable"
        
        # Remover de tratamiento
        del self.animales_en_tratamiento[animal.id]
        
        if self.log_service:
            self.log_service.ok(f"Alta médica - Animal #{animal.id} recuperado")
    
    def obtener_resumen_salud(self) -> Dict:
        """
        Genera resumen del estado de salud del feedlot.
        
        Returns:
            dict: Estadísticas de salud
        """
        tipos_alertas = {}
        for alerta in self.alertas_salud:
            tipo = alerta['tipo']
            tipos_alertas[tipo] = tipos_alertas.get(tipo, 0) + 1
        
        return {
            'total_alertas': len(self.alertas_salud),
            'animales_en_tratamiento': len(self.animales_en_tratamiento),
            'tratamientos_aplicados': self.tratamientos_aplicados,
            'tipos_alertas': tipos_alertas
        }
    
    def mostrar_estado_tratamientos(self):
        """Muestra el estado actual de los tratamientos"""
        print("\n ANIMALES EN TRATAMIENTO:")
        print("-"*70)
        
        if not self.animales_en_tratamiento:
            print("✓ No hay animales en tratamiento actualmente")
        else:
            for animal_id, tratamiento in self.animales_en_tratamiento.items():
                duracion = datetime.now() - tratamiento['inicio']
                horas = duracion.seconds // 3600
                minutos = (duracion.seconds % 3600) // 60
                
                print(f"Animal #{animal_id}:")
                print(f"  Tipo: {tratamiento['tipo'].capitalize()}")
                print(f"  Duración: {horas}h {minutos}m")
                print(f"  Temp. inicial: {tratamiento['temperatura_inicial']:.1f}°C")
        
        print("-"*70 + "\n")
    
    def obtener_animales_criticos(self) -> List[int]:
        """
        Obtiene lista de animales en estado crítico.
        
        Returns:
            list: IDs de animales críticos
        """
        criticos = []
        for animal_id, tratamiento in self.animales_en_tratamiento.items():
            duracion = datetime.now() - tratamiento['inicio']
            # Crítico si lleva más de 2 días en tratamiento
            if duracion.days >= 2:
                criticos.append(animal_id)
        
        return criticos
    
    def generar_informe_veterinario(self) -> str:
        """
        Genera un informe para el veterinario.
        
        Returns:
            str: Informe formateado
        """
        resumen = self.obtener_resumen_salud()
        criticos = self.obtener_animales_criticos()
        
        informe = "\n" + "="*70 + "\n"
        informe += "INFORME VETERINARIO - ESTANCIA CARNES FINAS\n"
        informe += "="*70 + "\n\n"
        
        informe += f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        informe += "RESUMEN:\n"
        informe += f"  Total de alertas: {resumen['total_alertas']}\n"
        informe += f"  Animales en tratamiento: {resumen['animales_en_tratamiento']}\n"
        informe += f"  Tratamientos aplicados: {resumen['tratamientos_aplicados']}\n\n"
        
        if resumen['tipos_alertas']:
            informe += "ALERTAS POR TIPO:\n"
            for tipo, cantidad in resumen['tipos_alertas'].items():
                informe += f"  {tipo}: {cantidad}\n"
            informe += "\n"
        
        if criticos:
            informe += " CASOS CRÍTICOS (>2 días en tratamiento):\n"
            for animal_id in criticos:
                informe += f"  Animal #{animal_id}\n"
            informe += "\n"
        
        informe += "="*70 + "\n"
        
        return informe
    
    def __str__(self):
        return f"SaludObserver(alertas={len(self.alertas_salud)}, tratamientos={len(self.animales_en_tratamiento)})"

# ================================================================================
# ARCHIVO 5/5: singleton.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./patrones/singleton.py
# ================================================================================

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

