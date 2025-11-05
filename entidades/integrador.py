"""
Archivo integrador generado automaticamente
Directorio: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./entidades
Fecha: 2025-11-05 20:04:58
Total de archivos integrados: 5
"""

# ================================================================================
# ARCHIVO 1/5: __init__.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./entidades/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/5: animal.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./entidades/animal.py
# ================================================================================

"""
Clase Animal - Representa un animal en el feedlot
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

# ================================================================================
# ARCHIVO 3/5: corral.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./entidades/corral.py
# ================================================================================

"""
Clase Corral - Representa un corral que contiene animales
"""

from typing import List, Optional
from entidades.animal import Animal

class Corral:
    """
    Representa un corral que contiene múltiples animales.
    Permite gestionar la capacidad y el estado de los animales.
    """
    
    def __init__(self, numero: int, capacidad: int = 50):
        """
        Inicializa un nuevo corral
        
        Args:
            numero: Número identificador del corral
            capacidad: Capacidad máxima de animales (default: 50)
        """
        self.numero = numero
        self.capacidad = capacidad
        self.animales: List[Animal] = []
        
    def agregar_animal(self, animal: Animal) -> bool:
        """
        Agrega un animal al corral si hay espacio disponible
        
        Args:
            animal: Objeto Animal a agregar
            
        Returns:
            True si se agregó exitosamente, False si el corral está lleno
        """
        if len(self.animales) < self.capacidad:
            self.animales.append(animal)
            return True
        return False
    
    def remover_animal(self, id_animal: int) -> bool:
        """
        Remueve un animal del corral por su ID
        
        Args:
            id_animal: ID del animal a remover
            
        Returns:
            True si se removió exitosamente, False si no se encontró
        """
        for animal in self.animales:
            if animal.id == id_animal:
                self.animales.remove(animal)
                return True
        return False
    
    def obtener_animal(self, id_animal: int) -> Optional[Animal]:
        """
        Obtiene un animal por su ID
        
        Args:
            id_animal: ID del animal a buscar
            
        Returns:
            Objeto Animal si se encuentra, None si no existe
        """
        for animal in self.animales:
            if animal.id == id_animal:
                return animal
        return None
    
    def peso_promedio(self) -> float:
        """
        Calcula el peso promedio de los animales en el corral
        
        Returns:
            Peso promedio en kg
        """
        if not self.animales:
            return 0.0
        return sum(a.peso for a in self.animales) / len(self.animales)
    
    def animales_enfermos(self) -> List[Animal]:
        """
        Retorna lista de animales enfermos en el corral
        
        Returns:
            Lista de animales con estado de salud anormal
        """
        return [a for a in self.animales if a.esta_enfermo()]
    
    def esta_lleno(self) -> bool:
        """
        Verifica si el corral está lleno
        
        Returns:
            True si está en capacidad máxima, False si hay espacio
        """
        return len(self.animales) >= self.capacidad
    
    def obtener_estadisticas(self) -> dict:
        """
        Genera estadísticas del corral
        
        Returns:
            Diccionario con estadísticas del corral
        """
        if not self.animales:
            return {
                "total_animales": 0,
                "peso_promedio": 0,
                "animales_enfermos": 0,
                "capacidad_usada": 0
            }
        
        return {
            "total_animales": len(self.animales),
            "peso_promedio": self.peso_promedio(),
            "animales_enfermos": len(self.animales_enfermos()),
            "capacidad_usada": (len(self.animales) / self.capacidad) * 100
        }
    
    def __str__(self):
        """Representación en string del corral"""
        return f"Corral #{self.numero} ({len(self.animales)}/{self.capacidad})"
    
    def __repr__(self):
        """Representación para debugging"""
        return f"Corral(numero={self.numero}, animales={len(self.animales)}/{self.capacidad})"

# ================================================================================
# ARCHIVO 4/5: sensor.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./entidades/sensor.py
# ================================================================================

"""
Clases Sensor - Sensores concurrentes para monitoreo
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

# ================================================================================
# ARCHIVO 5/5: veterinario.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./entidades/veterinario.py
# ================================================================================

"""
Clase Veterinario - Profesional encargado de la salud animal
Similar al Trabajador del sistema forestal.
"""

from datetime import datetime
from typing import List, Dict

class Veterinario:
    """
    Representa un veterinario del feedlot.
    
    Responsabilidades:
    - Revisar animales
    - Diagnosticar problemas
    - Aplicar tratamientos
    - Dar altas médicas
    - Mantener historial
    """
    
    def __init__(self, nombre: str, matricula: str, especialidad: str = "Bovinos"):
        """
        Inicializa un veterinario.
        
        Args:
            nombre: Nombre del veterinario
            matricula: Matrícula profesional
            especialidad: Especialidad veterinaria
        """
        self.nombre = nombre
        self.matricula = matricula
        self.especialidad = especialidad
        self.animales_atendidos: List[int] = []
        self.tratamientos_realizados: List[Dict] = []
        self.diagnosticos: List[Dict] = []
        self.fecha_ingreso = datetime.now()
        
        print(f" Veterinario {nombre} (Mat. {matricula}) incorporado al equipo")
    
    def revisar_animal(self, animal) -> Dict:
        """
        Realiza revisión completa de un animal.
        
        Args:
            animal: Animal a revisar
            
        Returns:
            dict: Diagnóstico detallado
        """
        print(f"\n [VET. {self.nombre}] Revisando Animal #{animal.id} ({animal.tipo})")
        
        # Realizar diagnóstico
        diagnostico = self._diagnosticar(animal)
        
        # Guardar en historial
        self.diagnosticos.append(diagnostico)
        if animal.id not in self.animales_atendidos:
            self.animales_atendidos.append(animal.id)
        
        # Mostrar diagnóstico
        print(f"    Diagnóstico: {diagnostico['estado']}")
        print(f"     Temperatura: {diagnostico['temperatura']:.1f}°C - {diagnostico['eval_temperatura']}")
        print(f"     Peso: {diagnostico['peso']:.1f} kg - {diagnostico['eval_peso']}")
        print(f"    Ganancia: {diagnostico['ganancia']:.2f} kg - {diagnostico['eval_ganancia']}")
        
        # Recomendaciones
        if diagnostico['recomendaciones']:
            print(f"    Recomendaciones:")
            for rec in diagnostico['recomendaciones']:
                print(f"      • {rec}")
        
        return diagnostico
    
    def _diagnosticar(self, animal) -> Dict:
        """
        Genera diagnóstico completo del animal.
        
        Args:
            animal: Animal a diagnosticar
            
        Returns:
            dict: Diagnóstico detallado
        """
        diagnostico = {
            'timestamp': datetime.now(),
            'veterinario': self.nombre,
            'animal_id': animal.id,
            'animal_tipo': animal.tipo,
            'temperatura': animal.temperatura,
            'peso': animal.peso,
            'ganancia': animal.ganancia_peso_total(),
            'estado_salud': animal.estado_salud,
            'recomendaciones': []
        }
        
        # Evaluar temperatura
        if animal.temperatura >= 40.0:
            diagnostico['eval_temperatura'] = "CRÍTICA"
            diagnostico['estado'] = "Crítico - Fiebre alta"
            diagnostico['recomendaciones'].append("Tratamiento urgente con antipirético")
            diagnostico['recomendaciones'].append("Aislamiento inmediato")
        elif animal.temperatura >= 39.5:
            diagnostico['eval_temperatura'] = "ELEVADA"
            diagnostico['estado'] = "Alerta - Fiebre moderada"
            diagnostico['recomendaciones'].append("Administrar antipirético")
            diagnostico['recomendaciones'].append("Monitoreo cada 4 horas")
        elif animal.temperatura < 37.0:
            diagnostico['eval_temperatura'] = "BAJA"
            diagnostico['estado'] = "Alerta - Hipotermia"
            diagnostico['recomendaciones'].append("Proporcionar abrigo")
            diagnostico['recomendaciones'].append("Aumentar calorías")
        else:
            diagnostico['eval_temperatura'] = "NORMAL"
            diagnostico['estado'] = "Saludable"
        
        # Evaluar peso y ganancia
        if animal.ganancia_peso_total() < 5:
            diagnostico['eval_ganancia'] = "BAJA"
            if diagnostico['estado'] == "Saludable":
                diagnostico['estado'] = "Bajo rendimiento"
            diagnostico['recomendaciones'].append("Revisar alimentación")
            diagnostico['recomendaciones'].append("Descartar problemas digestivos")
        elif animal.ganancia_peso_total() > 50:
            diagnostico['eval_ganancia'] = "EXCELENTE"
        else:
            diagnostico['eval_ganancia'] = "NORMAL"
        
        # Evaluar peso actual
        if animal.tipo == "Ternero" and animal.peso < 200:
            diagnostico['eval_peso'] = "BAJO"
            diagnostico['recomendaciones'].append("Intensificar alimentación")
        elif animal.tipo == "Novillo" and animal.peso < 300:
            diagnostico['eval_peso'] = "BAJO"
            diagnostico['recomendaciones'].append("Ración intensiva recomendada")
        else:
            diagnostico['eval_peso'] = "ADECUADO"
        
        return diagnostico
    
    def aplicar_tratamiento(self, animal, tipo_tratamiento: str) -> bool:
        """
        Aplica un tratamiento específico a un animal.
        
        Args:
            animal: Animal a tratar
            tipo_tratamiento: Tipo de tratamiento
            
        Returns:
            bool: True si se aplicó exitosamente
        """
        print(f"\n [VET. {self.nombre}] Aplicando tratamiento a Animal #{animal.id}")
        
        tratamientos_disponibles = {
            'antipiretrico': {
                'nombre': 'Antipirético',
                'indicacion': 'Reducción de fiebre',
                'dosis': '5ml/100kg'
            },
            'antibiotico': {
                'nombre': 'Antibiótico',
                'indicacion': 'Infección bacteriana',
                'dosis': '1ml/50kg'
            },
            'antiparasitario': {
                'nombre': 'Antiparasitario',
                'indicacion': 'Control de parásitos',
                'dosis': '1ml/100kg'
            },
            'vitaminas': {
                'nombre': 'Complejo vitamínico',
                'indicacion': 'Refuerzo nutricional',
                'dosis': '10ml'
            }
        }
        
        if tipo_tratamiento not in tratamientos_disponibles:
            print(f"   ✗ Tratamiento '{tipo_tratamiento}' no disponible")
            return False
        
        tratamiento_info = tratamientos_disponibles[tipo_tratamiento]
        
        # Registrar tratamiento
        tratamiento = {
            'timestamp': datetime.now(),
            'veterinario': self.nombre,
            'animal_id': animal.id,
            'tipo': tipo_tratamiento,
            'nombre': tratamiento_info['nombre'],
            'indicacion': tratamiento_info['indicacion'],
            'dosis': tratamiento_info['dosis']
        }
        
        self.tratamientos_realizados.append(tratamiento)
        
        print(f"    {tratamiento_info['nombre']} aplicado")
        print(f"    Indicación: {tratamiento_info['indicacion']}")
        print(f"    Dosis: {tratamiento_info['dosis']}")
        
        return True
    
    def dar_alta(self, animal) -> bool:
        """
        Da de alta a un animal recuperado.
        
        Args:
            animal: Animal a dar de alta
            
        Returns:
            bool: True si se dio de alta
        """
        if animal.estado_salud == "Saludable":
            print(f"     Animal #{animal.id} ya está saludable")
            return False
        
        print(f"\n [VET. {self.nombre}] Alta médica - Animal #{animal.id}")
        print(f"   Estado anterior: {animal.estado_salud}")
        print(f"   Temperatura actual: {animal.temperatura:.1f}°C")
        print(f"   Peso actual: {animal.peso:.1f} kg")
        
        # Cambiar estado
        animal.estado_salud = "Saludable"
        
        print(f"   ✓ Animal dado de alta - Estado: Saludable")
        
        return True
    
    def recomendar_estrategia_alimentacion(self, animal) -> str:
        """
        Recomienda estrategia de alimentación según estado del animal.
        
        Args:
            animal: Animal a evaluar
            
        Returns:
            str: Estrategia recomendada
        """
        if animal.esta_enfermo():
            return "mantenimiento"
        elif animal.peso < 300:
            return "intensiva"
        else:
            return "normal"
    
    def generar_informe_medico(self, animal) -> str:
        """
        Genera informe médico completo de un animal.
        
        Args:
            animal: Animal a reportar
            
        Returns:
            str: Informe médico formateado
        """
        informe = "\n" + "="*70 + "\n"
        informe += f"INFORME MÉDICO - Dr. {self.nombre}\n"
        informe += "="*70 + "\n\n"
        
        informe += f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        informe += f"Matrícula: {self.matricula}\n"
        informe += f"Especialidad: {self.especialidad}\n\n"
        
        informe += "DATOS DEL ANIMAL:\n"
        informe += f"  ID: {animal.id}\n"
        informe += f"  Tipo: {animal.tipo}\n"
        informe += f"  Peso actual: {animal.peso:.2f} kg\n"
        informe += f"  Peso inicial: {animal.peso_inicial:.2f} kg\n"
        informe += f"  Ganancia: {animal.ganancia_peso_total():.2f} kg\n"
        informe += f"  Temperatura: {animal.temperatura:.1f}°C\n"
        informe += f"  Estado de salud: {animal.estado_salud}\n\n"
        
        # Obtener diagnóstico
        diagnostico = self._diagnosticar(animal)
        
        informe += "DIAGNÓSTICO:\n"
        informe += f"  Estado general: {diagnostico['estado']}\n"
        informe += f"  Temperatura: {diagnostico['eval_temperatura']}\n"
        informe += f"  Peso: {diagnostico['eval_peso']}\n"
        informe += f"  Ganancia: {diagnostico['eval_ganancia']}\n\n"
        
        if diagnostico['recomendaciones']:
            informe += "RECOMENDACIONES:\n"
            for i, rec in enumerate(diagnostico['recomendaciones'], 1):
                informe += f"  {i}. {rec}\n"
            informe += "\n"
        
        informe += "="*70 + "\n"
        
        return informe
    
    def obtener_estadisticas(self) -> Dict:
        """
        Obtiene estadísticas de trabajo del veterinario.
        
        Returns:
            dict: Estadísticas del veterinario
        """
        return {
            'nombre': self.nombre,
            'matricula': self.matricula,
            'animales_atendidos': len(self.animales_atendidos),
            'tratamientos_realizados': len(self.tratamientos_realizados),
            'diagnosticos_realizados': len(self.diagnosticos),
            'dias_trabajo': (datetime.now() - self.fecha_ingreso).days
        }
    
    def __str__(self):
        return f"Dr. {self.nombre} (Mat. {self.matricula})"
    
    def __repr__(self):
        return f"Veterinario(nombre='{self.nombre}', matricula='{self.matricula}')"

