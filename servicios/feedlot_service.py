"""
Servicio Principal del Feedlot - Implementa Patrón Singleton

Este es el corazón del sistema. Gestiona todo el feedlot de forma centralizada.
"""

from typing import List, Dict, Optional
from patrones.singleton import SingletonMeta
from entidades.animal import Animal
from entidades.corral import Corral
from entidades.sensor import Sensor
from patrones.observer import ObservadorAlerta
from estrategias.estrategia_racion import EstrategiaRacion
from estrategias.racion_normal import RacionNormal
import time

class FeedlotSystem(metaclass=SingletonMeta):
    """
    Sistema central de gestión del feedlot.
    
    Implementa el patrón Singleton para garantizar una única instancia
    que coordine todos los componentes del sistema.
    
    Responsabilidades:
    - Gestionar animales y corrales
    - Coordinar sensores
    - Manejar observadores y alertas
    - Aplicar estrategias de alimentación
    - Generar estadísticas
    """
    
    def __init__(self):
        """
        Inicializa el sistema (solo se ejecuta una vez gracias al Singleton)
        """
        # Evitar reinicialización en llamadas subsecuentes
        if not hasattr(self, 'initialized'):
            # Colecciones principales
            self.animales: Dict[int, Animal] = {}
            self.corrales: Dict[int, Corral] = {}
            self.sensores: List[Sensor] = []
            
            # Observer para alertas
            self.observador_alertas = ObservadorAlerta()
            
            # Estrategia por defecto
            self.estrategia_default = RacionNormal()
            
            # Estado del sistema
            self.activo = False
            self.dia_actual = 0
            self.fecha_inicio = None
            
            # Marcador de inicialización
            self.initialized = True
            
            print(" [SINGLETON] Sistema Feedlot 'Estancia Carnes Finas' inicializado")
    
    def agregar_animal(self, animal: Animal, numero_corral: int = 1) -> bool:
        """
        Agrega un animal al sistema y lo asigna a un corral.
        
        Args:
            animal: Objeto Animal a agregar
            numero_corral: Número del corral donde asignarlo
            
        Returns:
            bool: True si se agregó exitosamente
        """
        # Verificar que el animal no exista
        if animal.id in self.animales:
            print(f" Animal #{animal.id} ya existe en el sistema")
            return False
        
        # Agregar a la colección de animales
        self.animales[animal.id] = animal
        
        # Crear corral si no existe
        if numero_corral not in self.corrales:
            self.corrales[numero_corral] = Corral(numero_corral)
            print(f"✓ Corral #{numero_corral} creado")
        
        # Agregar animal al corral
        if self.corrales[numero_corral].agregar_animal(animal):
            print(f"✓ {animal} agregado al {self.corrales[numero_corral]}")
            return True
        else:
            print(f"✗ Error: {self.corrales[numero_corral]} está lleno")
            # Remover de la colección si no se pudo agregar al corral
            del self.animales[animal.id]
            return False
    
    def remover_animal(self, id_animal: int) -> bool:
        """
        Remueve un animal del sistema.
        
        Args:
            id_animal: ID del animal a remover
            
        Returns:
            bool: True si se removió exitosamente
        """
        if id_animal not in self.animales:
            print(f"✗ Animal #{id_animal} no encontrado")
            return False
        
        # Remover de corrales
        for corral in self.corrales.values():
            if corral.remover_animal(id_animal):
                break
        
        # Remover de la colección
        animal = self.animales.pop(id_animal)
        print(f"✓ {animal} removido del sistema")
        return True
    
    def agregar_sensor(self, sensor: Sensor):
        """
        Agrega un sensor al sistema y lo suscribe al observador.
        
        Args:
            sensor: Sensor a agregar
        """
        # Suscribir al observador de alertas
        sensor.agregar_observador(self.observador_alertas)
        
        # Agregar a la lista de sensores
        self.sensores.append(sensor)
    
    def iniciar_monitoreo(self):
        """
        Inicia el monitoreo del feedlot.
        Activa todos los sensores en hilos concurrentes.
        """
        if not self.activo:
            self.activo = True
            
            # Registrar inicio
            from datetime import datetime
            self.fecha_inicio = datetime.now()
            
            print("\n" + "="*70)
            print(" INICIANDO MONITOREO DE ESTANCIA CARNES FINAS")
            print("="*70)
            
            # Iniciar todos los sensores
            for sensor in self.sensores:
                sensor.iniciar()
            
            print(f"✓ {len(self.sensores)} sensores activos")
            print(f"✓ {len(self.animales)} animales bajo monitoreo")
            print(f"✓ {len(self.corrales)} corrales operativos")
            print(f" Inicio: {self.fecha_inicio.strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*70 + "\n")
    
    def detener_monitoreo(self):
        """
        Detiene el monitoreo del feedlot.
        Desactiva todos los sensores de forma segura.
        """
        if self.activo:
            self.activo = False
            print("\n Deteniendo monitoreo...")
            
            # Detener todos los sensores
            for sensor in self.sensores:
                sensor.detener()
            
            print("✓ Todos los sensores detenidos")
            print("✓ Monitoreo finalizado\n")
    
    def aplicar_estrategia_racion(self, id_animal: int, estrategia: EstrategiaRacion):
        """
        Aplica una estrategia de alimentación a un animal específico.
        
        Args:
            id_animal: ID del animal
            estrategia: Estrategia de alimentación a aplicar
        """
        if id_animal in self.animales:
            animal = self.animales[id_animal]
            incremento = estrategia.aplicar_racion(animal)
            print(f"[STRATEGY] {estrategia.obtener_nombre()} aplicada a {animal} → +{incremento:.1f} kg")
        else:
            print(f"✗ Animal #{id_animal} no encontrado")
    
    def obtener_animal(self, id_animal: int) -> Optional[Animal]:
        """
        Obtiene un animal por su ID.
        
        Args:
            id_animal: ID del animal
            
        Returns:
            Animal o None si no existe
        """
        return self.animales.get(id_animal)
    
    def obtener_corral(self, numero_corral: int) -> Optional[Corral]:
        """
        Obtiene un corral por su número.
        
        Args:
            numero_corral: Número del corral
            
        Returns:
            Corral o None si no existe
        """
        return self.corrales.get(numero_corral)
    
    def obtener_estadisticas(self) -> Dict:
        """
        Genera estadísticas generales del feedlot.
        
        Returns:
            Diccionario con estadísticas completas
        """
        if not self.animales:
            return {
                "total_animales": 0,
                "peso_promedio": 0,
                "ganancia_promedio": 0,
                "animales_enfermos": 0,
                "total_corrales": 0,
                "alertas_activas": 0
            }
        
        # Calcular métricas
        pesos = [a.peso for a in self.animales.values()]
        ganancias = [a.ganancia_peso_total() for a in self.animales.values()]
        enfermos = [a for a in self.animales.values() if a.esta_enfermo()]
        
        return {
            "total_animales": len(self.animales),
            "peso_promedio": sum(pesos) / len(pesos),
            "peso_total": sum(pesos),
            "ganancia_promedio": sum(ganancias) / len(ganancias),
            "ganancia_total": sum(ganancias),
            "animales_enfermos": len(enfermos),
            "porcentaje_enfermos": (len(enfermos) / len(self.animales)) * 100,
            "total_corrales": len(self.corrales),
            "alertas_activas": len(self.observador_alertas.alertas),
            "dia_actual": self.dia_actual
        }
    
    def mostrar_estado(self):
        """
        Muestra el estado actual del feedlot en consola.
        """
        print("\n" + "="*70)
        print(" ESTADO ACTUAL DEL FEEDLOT")
        print("="*70)
        
        stats = self.obtener_estadisticas()
        
        if stats["total_animales"] > 0:
            print(f" Día: {stats['dia_actual']}")
            print(f" Animales: {stats['total_animales']}")
            print(f"  Peso promedio: {stats['peso_promedio']:.2f} kg")
            print(f" Peso total: {stats['peso_total']:.2f} kg")
            print(f" Ganancia promedio: {stats['ganancia_promedio']:.2f} kg")
            print(f" Ganancia total: {stats['ganancia_total']:.2f} kg")
            print(f" Animales enfermos: {stats['animales_enfermos']} ({stats['porcentaje_enfermos']:.1f}%)")
            print(f" Corrales activos: {stats['total_corrales']}")
            print(f"  Alertas registradas: {stats['alertas_activas']}")
        else:
            print("  No hay animales en el sistema")
        
        print("="*70 + "\n")
    
    def listar_animales(self):
        """
        Lista todos los animales con su información detallada.
        """
        print("\n LISTADO DE ANIMALES:")
        print("-"*70)
        
        if not self.animales:
            print("  No hay animales registrados")
        else:
            for animal in sorted(self.animales.values(), key=lambda a: a.id):
                print(animal.mostrar_info())
        
        print("-"*70 + "\n")
    
    def listar_corrales(self):
        """
        Lista todos los corrales con sus estadísticas.
        """
        print("\n LISTADO DE CORRALES:")
        print("-"*70)
        
        if not self.corrales:
            print("  No hay corrales creados")
        else:
            for corral in sorted(self.corrales.values(), key=lambda c: c.numero):
                stats = corral.obtener_estadisticas()
                print(f"{corral} | Peso prom: {stats['peso_promedio']:.1f} kg | "
                      f"Enfermos: {stats['animales_enfermos']} | "
                      f"Uso: {stats['capacidad_usada']:.1f}%")
        
        print("-"*70 + "\n")
    
    def obtener_mejores_animales(self, cantidad: int = 5) -> List[Animal]:
        """
        Obtiene los animales con mejor ganancia de peso.
        
        Args:
            cantidad: Número de animales a retornar
            
        Returns:
            Lista de animales ordenados por ganancia
        """
        return sorted(
            self.animales.values(),
            key=lambda a: a.ganancia_peso_total(),
            reverse=True
        )[:cantidad]
    
    def obtener_animales_alerta(self) -> List[Animal]:
        """
        Obtiene lista de animales con alertas activas.
        
        Returns:
            Lista de animales enfermos o con problemas
        """
        return [a for a in self.animales.values() if a.esta_enfermo()]
    
    def resetear_sistema(self):
        """
        Resetea el sistema a su estado inicial.
         CUIDADO: Elimina todos los datos.
        """
        print("\n  RESETEANDO SISTEMA...")
        
        # Detener monitoreo si está activo
        if self.activo:
            self.detener_monitoreo()
        
        # Limpiar colecciones
        self.animales.clear()
        self.corrales.clear()
        self.sensores.clear()
        self.observador_alertas.limpiar_alertas()
        
        # Resetear contadores
        self.dia_actual = 0
        self.fecha_inicio = None
        
        print("✓ Sistema reseteado completamente\n")
    
    def __str__(self):
        """Representación en string del sistema"""
        return f"FeedlotSystem(animales={len(self.animales)}, corrales={len(self.corrales)})"
    
    def __repr__(self):
        """Representación para debugging"""
        return (f"FeedlotSystem(animales={len(self.animales)}, "
                f"corrales={len(self.corrales)}, "
                f"sensores={len(self.sensores)}, "
                f"activo={self.activo})")