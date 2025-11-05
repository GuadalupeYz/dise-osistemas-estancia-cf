"""
Clases Sensor - Sensores concurrentes para monitoreo
Autor: Guadalupe Yañez
Implementa: Patrón Observer + Threading
"""

import threading
import time
import random
from abc import ABC, abstractmethod
from typing import List

class Sensor(ABC):
    """
    Clase abstracta base para todos los sensores.
    Implementa el patrón Observer y usa threading para operación concurrente.
    """
    
    def __init__(self, animal, intervalo: float = 5.0):
        """
        Inicializa un sensor
        
        Args:
            animal: Animal asociado al sensor
            intervalo: Tiempo entre lecturas en segundos
        """
        self.animal = animal
        self.intervalo = intervalo
        self.activo = False
        self.thread = None
        self.observadores = []
        
    def agregar_observador(self, observador):
        """
        Agrega un observador (patrón Observer)
        
        Args:
            observador: Objeto que implementa la interfaz Observador
        """
        self.observadores.append(observador)
        
    def notificar_observadores(self, mensaje: str, tipo: str):
        """
        Notifica a todos los observadores registrados
        
        Args:
            mensaje: Mensaje de la notificación
            tipo: Tipo de alerta (FIEBRE, BAJO_RENDIMIENTO, etc.)
        """
        for obs in self.observadores:
            obs.actualizar(self.animal, mensaje, tipo)
    
    @abstractmethod
    def realizar_lectura(self):
        """
        Método abstracto para realizar lectura del sensor.
        Debe ser implementado por las subclases.
        """
        pass
    
    def iniciar(self):
        """Inicia el sensor en un hilo separado (daemon thread)"""
        if not self.activo:
            self.activo = True
            self.thread = threading.Thread(target=self._ejecutar, daemon=True)
            self.thread.start()
            
    def detener(self):
        """Detiene el sensor de forma segura"""
        self.activo = False
        if self.thread:
            self.thread.join(timeout=2)
            
    def _ejecutar(self):
        """
        Ejecuta el ciclo de lectura del sensor.
        Corre en un hilo separado.
        """
        while self.activo:
            self.realizar_lectura()
            time.sleep(self.intervalo)


class SensorPeso(Sensor):
    """
    Sensor de peso - simula ganancia diaria de peso.
    Monitorea el incremento de peso y detecta bajo rendimiento.
    """
    
    def realizar_lectura(self):
        """
        Realiza una lectura de peso simulada.
        Simula variación natural de peso diaria.
        """
        # Simula variación natural de peso (0.5 a 1.5 kg)
        variacion = random.uniform(0.5, 1.5)
        self.animal.actualizar_peso(variacion)
        
        # Log de la lectura
        mensaje = (f"[SensorPeso] {self.animal} → "
                  f"+{variacion:.2f} kg (Total: {self.animal.peso:.2f} kg)")
        print(mensaje)
        
        # Notificar si hay bajo rendimiento (< 0.7 kg/día)
        if variacion < 0.7:
            self.notificar_observadores(
                f"Bajo rendimiento en {self.animal}: +{variacion:.2f} kg",
                "BAJO_RENDIMIENTO"
            )


class SensorTemperatura(Sensor):
    """
    Sensor de temperatura - detecta fiebre e hipotermia.
    Monitorea la temperatura corporal del animal.
    """
    
    def realizar_lectura(self):
        """
        Realiza una lectura de temperatura simulada.
        Detecta fiebre (>39.5°C) e hipotermia (<37.0°C).
        """
        # Temperatura base normal: 38.5°C
        temperatura_base = 38.5
        variacion = random.uniform(-0.5, 1.5)
        nueva_temp = temperatura_base + variacion
        
        temp_anterior = self.animal.temperatura
        self.animal.actualizar_temperatura(nueva_temp)
        
        # Mostrar solo si hay cambio significativo o anomalía
        if abs(nueva_temp - temp_anterior) > 0.3 or nueva_temp >= 39.5 or nueva_temp < 37.0:
            # Determinar estado
            if nueva_temp >= 39.5:
                estado = " FIEBRE"
            elif nueva_temp < 37.0:
                estado = " HIPOTERMIA"
            else:
                estado = "✓ Normal"
            
            mensaje = f"[SensorTemp] {self.animal} → {nueva_temp:.1f}°C {estado}"
            print(mensaje)
            
            # Notificar si hay fiebre
            if nueva_temp >= 39.5:
                self.notificar_observadores(
                    f"Fiebre detectada en {self.animal}: {nueva_temp:.1f}°C",
                    "FIEBRE"
                )
            # Notificar si hay hipotermia
            elif nueva_temp < 37.0:
                self.notificar_observadores(
                    f"Hipotermia en {self.animal}: {nueva_temp:.1f}°C",
                    "HIPOTERMIA"
                )