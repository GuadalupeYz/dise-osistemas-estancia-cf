"""
Servicio de Raciones - Aplica estrategias de alimentación

Servicio concurrente que aplica estrategias de alimentación automáticamente.
"""

import threading
import time
from typing import Dict
from estrategias.estrategia_racion import EstrategiaRacion
from estrategias.racion_normal import RacionNormal
from estrategias.racion_intensiva import RacionIntensiva
from estrategias.racion_mantenimiento import RacionMantenimiento

class RacionService:
    """
    Servicio que aplica estrategias de alimentación de forma automática.
    
    Usa threading para aplicación continua y concurrente.
    Implementa el patrón Strategy para gestión de alimentación.
    """
    
    def __init__(self, feedlot_system):
        """
        Inicializa el servicio de raciones.
        
        Args:
            feedlot_system: Instancia del FeedlotSystem (Singleton)
        """
        self.feedlot_system = feedlot_system
        self.estrategias: Dict[int, EstrategiaRacion] = {}
        self.activo = False
        self.thread = None
        self.intervalo = 10.0  # Aplicar raciones cada 10 segundos
        
        # Estrategias disponibles (instancias pre-creadas)
        self.racion_normal = RacionNormal()
        self.racion_intensiva = RacionIntensiva()
        self.racion_mantenimiento = RacionMantenimiento()
        
        print(" Servicio de Raciones configurado")
    
    def asignar_estrategia(self, id_animal: int, estrategia: EstrategiaRacion):
        """
        Asigna una estrategia de alimentación específica a un animal.
        
        Args:
            id_animal: ID del animal
            estrategia: Estrategia a asignar
        """
        self.estrategias[id_animal] = estrategia
        print(f"[RACION] Estrategia '{estrategia.obtener_nombre()}' "
              f"asignada a Animal #{id_animal}")
    
    def asignar_estrategia_automatica(self, id_animal: int):
        """
        Asigna automáticamente la mejor estrategia según el estado del animal.
        
        Lógica de asignación:
        - Enfermo -> Mantenimiento
        - Peso < 300 kg -> Intensiva (engorde acelerado)
        - Peso >= 300 kg -> Normal (mantenimiento de ganancia)
        
        Args:
            id_animal: ID del animal
        """
        animal = self.feedlot_system.animales.get(id_animal)
        if not animal:
            return
        
        # Lógica de decisión
        if animal.esta_enfermo():
            estrategia = self.racion_mantenimiento
            razon = "animal enfermo"
        elif animal.peso < 300:
            estrategia = self.racion_intensiva
            razon = "peso bajo (<300 kg)"
        else:
            estrategia = self.racion_normal
            razon = "peso adecuado (>=300 kg)"
        
        self.asignar_estrategia(id_animal, estrategia)
        print(f"   └─ Razón: {razon}")
    
    def cambiar_estrategia(self, id_animal: int, tipo_estrategia: str):
        """
        Cambia la estrategia de un animal por tipo.
        
        Args:
            id_animal: ID del animal
            tipo_estrategia: 'normal', 'intensiva' o 'mantenimiento'
        """
        estrategias_map = {
            'normal': self.racion_normal,
            'intensiva': self.racion_intensiva,
            'mantenimiento': self.racion_mantenimiento
        }
        
        if tipo_estrategia.lower() in estrategias_map:
            estrategia = estrategias_map[tipo_estrategia.lower()]
            self.asignar_estrategia(id_animal, estrategia)
        else:
            print(f"✗ Tipo de estrategia no válido: {tipo_estrategia}")
    
    def iniciar(self):
        """
        Inicia el servicio de raciones en un hilo separado.
        """
        if not self.activo:
            self.activo = True
            self.thread = threading.Thread(target=self._ejecutar, daemon=True)
            self.thread.start()
            print("✓ Servicio de raciones iniciado (intervalo: {}s)".format(self.intervalo))
    
    def detener(self):
        """
        Detiene el servicio de forma segura.
        """
        if self.activo:
            self.activo = False
            if self.thread:
                self.thread.join(timeout=2)
            print("✓ Servicio de raciones detenido")
    
    def _ejecutar(self):
        """
        Ejecuta el ciclo de aplicación de raciones.
        Corre en un hilo separado (daemon thread).
        """
        while self.activo:
            time.sleep(self.intervalo)
            self._aplicar_raciones()
    
    def _aplicar_raciones(self):
        """
        Aplica las raciones asignadas a cada animal.
        Este método se ejecuta periódicamente.
        """
        if not self.feedlot_system.animales:
            return
        
        print("\n [RACION] Aplicando raciones programadas...")
        
        total_incremento = 0
        animales_procesados = 0
        
        for id_animal, animal in self.feedlot_system.animales.items():
    # Si no tiene estrategia asignada, asignar automáticamente
           if id_animal not in self.estrategias:
              self.asignar_estrategia_automatica(id_animal)
    
    # Aplicar estrategia
           estrategia = self.estrategias.get(id_animal)
           if estrategia:
              incremento = estrategia.aplicar_racion(animal)
              total_incremento += incremento
              animales_procesados += 1
        
        # Mostrar con indicador según la estrategia
              if isinstance(estrategia, RacionIntensiva):
                 indicador = "[INTENS]"
              elif isinstance(estrategia, RacionMantenimiento):
                 indicador = "[MANTEN]"
              else:
                 indicador = "[NORMAL]"
        
        print(f"  {indicador} {animal}: {estrategia.obtener_nombre()} → +{incremento:.1f} kg")
        
        # Resumen
        if animales_procesados > 0:
            promedio = total_incremento / animales_procesados
            print(f"\n   Total: +{total_incremento:.1f} kg | "
                  f"Promedio: +{promedio:.2f} kg/animal")
    
    def obtener_estadisticas_raciones(self) -> dict:
        """
        Genera estadísticas sobre las estrategias aplicadas.
        
        Returns:
            Diccionario con estadísticas
        """
        if not self.estrategias:
            return {}
        
        # Contar por tipo de estrategia
        conteo = {
            'normal': 0,
            'intensiva': 0,
            'mantenimiento': 0
        }
        
        costo_total = 0
        
        for estrategia in self.estrategias.values():
            if isinstance(estrategia, RacionNormal):
                conteo['normal'] += 1
            elif isinstance(estrategia, RacionIntensiva):
                conteo['intensiva'] += 1
            elif isinstance(estrategia, RacionMantenimiento):
                conteo['mantenimiento'] += 1
            
            costo_total += estrategia.obtener_costo_diario()
        
        return {
            'total_animales': len(self.estrategias),
            'racion_normal': conteo['normal'],
            'racion_intensiva': conteo['intensiva'],
            'racion_mantenimiento': conteo['mantenimiento'],
            'costo_diario_total': costo_total,
            'costo_promedio': costo_total / len(self.estrategias) if self.estrategias else 0
        }
    
    def mostrar_resumen_estrategias(self):
        """
        Muestra un resumen de las estrategias aplicadas.
        """
        stats = self.obtener_estadisticas_raciones()
        
        if not stats:
            print("  No hay estrategias asignadas")
            return
        
        print("\n" + "="*70)
        print("  RESUMEN DE ESTRATEGIAS DE ALIMENTACIÓN")
        print("="*70)
        print(f"Total animales: {stats['total_animales']}")
        print(f"  ✓ Ración Normal: {stats['racion_normal']}")
        print(f"   Ración Intensiva: {stats['racion_intensiva']}")
        print(f"   Ración Mantenimiento: {stats['racion_mantenimiento']}")
        print(f"\n Costo diario total: ${stats['costo_diario_total']:.2f}")
        print(f" Costo promedio por animal: ${stats['costo_promedio']:.2f}")
        print("="*70 + "\n")
    
    def optimizar_estrategias(self):
        """
        Revisa y optimiza las estrategias de todos los animales.
        Útil para ajustar estrategias según cambios de estado.
        """
        print("\n Optimizando estrategias de alimentación...")
        
        cambios = 0
        for id_animal in self.feedlot_system.animales.keys():
            estrategia_actual = self.estrategias.get(id_animal)
            
            # Determinar estrategia óptima
            animal = self.feedlot_system.animales[id_animal]
            
            if animal.esta_enfermo() and not isinstance(estrategia_actual, RacionMantenimiento):
                self.asignar_estrategia(id_animal, self.racion_mantenimiento)
                cambios += 1
            elif not animal.esta_enfermo() and isinstance(estrategia_actual, RacionMantenimiento):
                # Animal recuperado, volver a estrategia normal o intensiva
                if animal.peso < 300:
                    self.asignar_estrategia(id_animal, self.racion_intensiva)
                else:
                    self.asignar_estrategia(id_animal, self.racion_normal)
                cambios += 1
        
        print(f"✓ Optimización completada: {cambios} cambio(s) realizado(s)")
    
    def __str__(self):
        return f"RacionService(animales={len(self.estrategias)}, activo={self.activo})"