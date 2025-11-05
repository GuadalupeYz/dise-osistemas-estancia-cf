"""
Archivo integrador generado automaticamente
Directorio: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./servicios
Fecha: 2025-11-05 09:19:07
Total de archivos integrados: 6
"""

# ================================================================================
# ARCHIVO 1/6: __init__.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./servicios/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/6: feedlot_service.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./servicios/feedlot_service.py
# ================================================================================

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

# ================================================================================
# ARCHIVO 3/6: log_service.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./servicios/log_service.py
# ================================================================================

"""
Servicio de Bitácora (Logging) - Registra todos los eventos del sistema
Similar al sistema forestal, mantiene trazabilidad completa.
"""

import os
from datetime import datetime
from enum import Enum

class NivelLog(Enum):
    """Niveles de logging similares al sistema forestal"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICO = "CRITICO"
    OK = "OK"
    ALERTA = "ALERTA"
    PERSISTENCIA = "PERSISTENCIA"

class LogService:
    """
    Servicio de bitácora para registro de eventos del feedlot.
    
    Mantiene trazabilidad completa de:
    - Lecturas de sensores
    - Aplicación de raciones
    - Alertas generadas
    - Cambios de estado
    - Operaciones del sistema
    """
    
    def __init__(self, ruta_logs: str = "logs/", nombre_archivo: str = None):
        """
        Inicializa el servicio de logs.
        
        Args:
            ruta_logs: Carpeta donde se guardarán los logs
            nombre_archivo: Nombre personalizado del archivo (opcional)
        """
        self.ruta = ruta_logs
        
        # Crear carpeta si no existe
        if not os.path.exists(self.ruta):
            os.makedirs(self.ruta)
        
        # Nombre del archivo
        if nombre_archivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"feedlot_{timestamp}.log"
        
        self.archivo = os.path.join(self.ruta, nombre_archivo)
        
        # Inicializar archivo
        self._inicializar_log()
        
        print(f" Servicio de Log configurado: {self.archivo}")
    
    def _inicializar_log(self):
        """Crea el archivo de log con encabezado"""
        with open(self.archivo, "w", encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("ESTANCIA CARNES FINAS - BITÁCORA DE EVENTOS\n")
            f.write("="*80 + "\n")
            f.write(f"Inicio de sesión: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
    
    def registrar(self, mensaje: str, nivel: NivelLog = NivelLog.INFO):
        """
        Registra un mensaje en la bitácora.
        
        Args:
            mensaje: Mensaje a registrar
            nivel: Nivel de importancia del mensaje
        """
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # Incluir milisegundos
        linea = f"[{timestamp}] [{nivel.value}] {mensaje}\n"
        
        # Escribir en archivo
        with open(self.archivo, "a", encoding='utf-8') as f:
            f.write(linea)
        
        # También imprimir si es importante
        if nivel in [NivelLog.ERROR, NivelLog.CRITICO, NivelLog.ALERTA]:
            print(f" LOG: {linea.strip()}")
    
    def info(self, mensaje: str):
        """Registra mensaje informativo"""
        self.registrar(mensaje, NivelLog.INFO)
    
    def debug(self, mensaje: str):
        """Registra mensaje de debug"""
        self.registrar(mensaje, NivelLog.DEBUG)
    
    def warning(self, mensaje: str):
        """Registra advertencia"""
        self.registrar(mensaje, NivelLog.WARNING)
    
    def error(self, mensaje: str):
        """Registra error"""
        self.registrar(mensaje, NivelLog.ERROR)
    
    def critico(self, mensaje: str):
        """Registra evento crítico"""
        self.registrar(mensaje, NivelLog.CRITICO)
    
    def ok(self, mensaje: str):
        """Registra operación exitosa"""
        self.registrar(mensaje, NivelLog.OK)
    
    def alerta(self, mensaje: str):
        """Registra alerta del sistema"""
        self.registrar(mensaje, NivelLog.ALERTA)
    
    def persistencia(self, mensaje: str):
        """Registra operación de persistencia"""
        self.registrar(mensaje, NivelLog.PERSISTENCIA)
    
    def registrar_sensor(self, animal, tipo_sensor: str, valor: float):
        """
        Registra lectura de sensor.
        
        Args:
            animal: Animal monitoreado
            tipo_sensor: Tipo de sensor (peso/temperatura)
            valor: Valor leído
        """
        mensaje = f"Sensor {tipo_sensor} - Animal #{animal.id} ({animal.tipo}): {valor}"
        self.debug(mensaje)
    
    def registrar_racion(self, animal, estrategia: str, incremento: float):
        """
        Registra aplicación de ración.
        
        Args:
            animal: Animal alimentado
            estrategia: Nombre de la estrategia
            incremento: Incremento de peso
        """
        mensaje = f"Ración {estrategia} aplicada - Animal #{animal.id}: +{incremento:.2f} kg"
        self.info(mensaje)
    
    def registrar_alerta_salud(self, animal, tipo_alerta: str, valor: float):
        """
        Registra alerta de salud.
        
        Args:
            animal: Animal con alerta
            tipo_alerta: Tipo de alerta (fiebre, bajo_rendimiento, etc.)
            valor: Valor que generó la alerta
        """
        mensaje = f"ALERTA {tipo_alerta} - Animal #{animal.id} ({animal.tipo}): {valor}"
        self.alerta(mensaje)
    
    def registrar_cambio_estado(self, animal, estado_anterior: str, estado_nuevo: str):
        """
        Registra cambio de estado de salud.
        
        Args:
            animal: Animal afectado
            estado_anterior: Estado previo
            estado_nuevo: Nuevo estado
        """
        mensaje = f"Cambio de estado - Animal #{animal.id}: {estado_anterior} → {estado_nuevo}"
        self.warning(mensaje)
    
    def registrar_inicio_sistema(self, total_animales: int, total_sensores: int):
        """
        Registra inicio del sistema.
        
        Args:
            total_animales: Número de animales
            total_sensores: Número de sensores
        """
        mensaje = f"Sistema iniciado - {total_animales} animales, {total_sensores} sensores"
        self.ok(mensaje)
    
    def registrar_fin_sistema(self, dia_final: int, ganancia_total: float):
        """
        Registra finalización del sistema.
        
        Args:
            dia_final: Día final de operación
            ganancia_total: Ganancia total del feedlot
        """
        mensaje = f"Sistema detenido - Día {dia_final}, Ganancia total: {ganancia_total:.2f} kg"
        self.ok(mensaje)
    
    def registrar_reporte(self, dia: int, peso_promedio: float, alertas: int):
        """
        Registra generación de reporte.
        
        Args:
            dia: Día del reporte
            peso_promedio: Peso promedio de los animales
            alertas: Número de alertas activas
        """
        mensaje = f"Reporte Día {dia} - Peso prom: {peso_promedio:.2f} kg, Alertas: {alertas}"
        self.info(mensaje)
    
    def crear_seccion(self, titulo: str):
        """
        Crea una sección visual en el log.
        
        Args:
            titulo: Título de la sección
        """
        with open(self.archivo, "a", encoding='utf-8') as f:
            f.write("\n" + "-"*80 + "\n")
            f.write(f"  {titulo}\n")
            f.write("-"*80 + "\n\n")
    
    def finalizar_log(self):
        """Cierra el log con un pie de página"""
        with open(self.archivo, "a", encoding='utf-8') as f:
            f.write("\n" + "="*80 + "\n")
            f.write(f"Fin de sesión: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n")
        
        print(f" Log finalizado: {self.archivo}")
    
    def obtener_estadisticas(self) -> dict:
        """
        Genera estadísticas del log.
        
        Returns:
            dict: Diccionario con conteo por nivel
        """
        stats = {nivel: 0 for nivel in NivelLog}
        
        try:
            with open(self.archivo, "r", encoding='utf-8') as f:
                for linea in f:
                    for nivel in NivelLog:
                        if f"[{nivel.value}]" in linea:
                            stats[nivel] += 1
            
            return stats
        except Exception:
            return stats
    
    def mostrar_resumen(self):
        """Muestra resumen estadístico del log"""
        stats = self.obtener_estadisticas()
        
        print("\n RESUMEN DEL LOG:")
        print("-"*50)
        for nivel, cantidad in stats.items():
            if cantidad > 0:
                icono = "okey" if nivel in [NivelLog.OK, NivelLog.INFO] else "warning"
                print(f"{icono} {nivel.value}: {cantidad}")
        print("-"*50 + "\n")
    
    def __str__(self):
        return f"LogService(archivo={self.archivo})"

# ================================================================================
# ARCHIVO 4/6: persistencia_service.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./servicios/persistencia_service.py
# ================================================================================

"""
Servicio de Persistencia - Guarda y carga el estado del sistema
Permite guardar el estado completo del feedlot y continuar simulaciones.
"""

import pickle
import os
import csv
from datetime import datetime
from typing import Optional

class PersistenciaService:
    """
    Servicio para persistencia de datos del feedlot.
    
    Funcionalidades:
    - Guardar estado completo del sistema (binario .dat)
    - Cargar estado de simulaciones anteriores
    - Exportar reportes en CSV
    - Gestión de backups automáticos
    """
    
    def __init__(self):
        """Inicializa el servicio de persistencia"""
        self.carpeta_data = "data"
        self.carpeta_csv = "reportes_csv"
        self.carpeta_backups = "data/backups"
        
        # Crear carpetas si no existen
        for carpeta in [self.carpeta_data, self.carpeta_csv, self.carpeta_backups]:
            if not os.path.exists(carpeta):
                os.makedirs(carpeta)
                print(f" Carpeta '{carpeta}/' creada")
        
        print(" Servicio de Persistencia configurado")
    
    def guardar_estado(self, sistema, archivo: str = None) -> bool:
        """
        Guarda el estado completo del sistema en formato binario.
        
        Args:
            sistema: Instancia de FeedlotSystem
            archivo: Nombre del archivo (opcional)
            
        Returns:
            bool: True si se guardó exitosamente
        """
        if archivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo = f"{self.carpeta_data}/feedlot_{timestamp}.dat"
        
        try:
            # Preparar datos para serialización
            estado = {
                'animales': sistema.animales,
                'corrales': sistema.corrales,
                'dia_actual': sistema.dia_actual,
                'fecha_inicio': sistema.fecha_inicio,
                'alertas': sistema.observador_alertas.alertas,
                'timestamp_guardado': datetime.now()
            }
            
            # Guardar con pickle
            with open(archivo, "wb") as f:
                pickle.dump(estado, f)
            
            print(f"[PERSISTENCIA] ✓ Estado guardado en: {archivo}")
            print(f"[INFO] Día: {sistema.dia_actual}, Animales: {len(sistema.animales)}")
            return True
            
        except Exception as e:
            print(f"[ERROR] ✗ No se pudo guardar el estado: {e}")
            return False
    
    def cargar_estado(self, archivo: str = None) -> Optional[dict]:
        """
        Carga el estado del sistema desde un archivo binario.
        
        Args:
            archivo: Ruta del archivo a cargar
            
        Returns:
            dict: Diccionario con el estado cargado o None si falla
        """
        if archivo is None:
            # Buscar el archivo más reciente
            archivos = [f for f in os.listdir(self.carpeta_data) if f.endswith('.dat')]
            if not archivos:
                print("[ERROR] No hay archivos de estado guardados")
                return None
            archivo = os.path.join(self.carpeta_data, sorted(archivos)[-1])
        
        try:
            with open(archivo, "rb") as f:
                estado = pickle.load(f)
            
            print(f"[PERSISTENCIA] ✓ Estado cargado desde: {archivo}")
            print(f"[INFO] Día: {estado['dia_actual']}, Animales: {len(estado['animales'])}")
            print(f"[INFO] Guardado el: {estado['timestamp_guardado'].strftime('%Y-%m-%d %H:%M:%S')}")
            
            return estado
            
        except Exception as e:
            print(f"[ERROR] ✗ No se pudo cargar el estado: {e}")
            return None
    
    def restaurar_sistema(self, sistema, estado: dict) -> bool:
        """
        Restaura el estado de un sistema desde un diccionario cargado.
        
        Args:
            sistema: Instancia de FeedlotSystem
            estado: Diccionario con el estado guardado
            
        Returns:
            bool: True si se restauró exitosamente
        """
        try:
            # Restaurar animales
            sistema.animales = estado['animales']
            sistema.corrales = estado['corrales']
            sistema.dia_actual = estado['dia_actual']
            sistema.fecha_inicio = estado['fecha_inicio']
            sistema.observador_alertas.alertas = estado['alertas']
            
            print("[PERSISTENCIA] ✓ Sistema restaurado exitosamente")
            print(f"[INFO] Continuando desde el día {sistema.dia_actual}")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] ✗ No se pudo restaurar el sistema: {e}")
            return False
    
    def exportar_reporte_csv(self, sistema, archivo: str = None) -> bool:
        """
        Exporta un reporte del feedlot en formato CSV.
        
        Args:
            sistema: Instancia de FeedlotSystem
            archivo: Nombre del archivo CSV (opcional)
            
        Returns:
            bool: True si se exportó exitosamente
        """
        if archivo is None:
            fecha = datetime.now().strftime("%Y-%m-%d")
            archivo = f"{self.carpeta_csv}/feedlot_{fecha}.csv"
        
        try:
            with open(archivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Encabezados
                writer.writerow([
                    'ID', 'Tipo', 'Peso_Actual_kg', 'Peso_Inicial_kg', 
                    'Ganancia_kg', 'GDP_kg_dia', 'Temperatura_C', 
                    'Estado_Salud', 'Racion_Actual', 'Dias_Feedlot'
                ])
                
                # Datos de cada animal
                for animal in sistema.animales.values():
                    dias = max(1, sistema.dia_actual)
                    gdp = animal.ganancia_peso_total() / dias
                    
                    writer.writerow([
                        animal.id,
                        animal.tipo,
                        round(animal.peso, 2),
                        round(animal.peso_inicial, 2),
                        round(animal.ganancia_peso_total(), 2),
                        round(gdp, 2),
                        round(animal.temperatura, 1),
                        animal.estado_salud,
                        animal.racion_actual or "Sin asignar",
                        animal.dias_en_feedlot
                    ])
            
            print(f"[PERSISTENCIA] ✓ Reporte CSV exportado: {archivo}")
            return True
            
        except Exception as e:
            print(f"[ERROR] ✗ No se pudo exportar CSV: {e}")
            return False
    
    def crear_backup(self, sistema) -> bool:
        """
        Crea un backup automático del estado actual.
        
        Args:
            sistema: Instancia de FeedlotSystem
            
        Returns:
            bool: True si se creó exitosamente
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_backup = f"{self.carpeta_backups}/backup_{timestamp}.dat"
        
        return self.guardar_estado(sistema, archivo_backup)
    
    def listar_estados_guardados(self):
        """
        Lista todos los estados guardados disponibles.
        """
        print("\n ESTADOS GUARDADOS DISPONIBLES:")
        print("-"*70)
        
        archivos = sorted([f for f in os.listdir(self.carpeta_data) 
                          if f.endswith('.dat') and not f.startswith('backup')])
        
        if not archivos:
            print("  No hay estados guardados")
        else:
            for i, archivo in enumerate(archivos, 1):
                ruta = os.path.join(self.carpeta_data, archivo)
                tamaño = os.path.getsize(ruta) / 1024  # KB
                fecha_mod = datetime.fromtimestamp(os.path.getmtime(ruta))
                
                print(f"{i}. {archivo}")
                print(f"   Tamaño: {tamaño:.2f} KB | "
                      f"Modificado: {fecha_mod.strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("-"*70 + "\n")
    
    def exportar_historico_animales(self, sistema, archivo: str = None) -> bool:
        """
        Exporta el histórico de peso de todos los animales a CSV.
        
        Args:
            sistema: Instancia de FeedlotSystem
            archivo: Nombre del archivo CSV (opcional)
            
        Returns:
            bool: True si se exportó exitosamente
        """
        if archivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo = f"{self.carpeta_csv}/historico_{timestamp}.csv"
        
        try:
            with open(archivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Encabezados
                writer.writerow(['Animal_ID', 'Tipo', 'Lectura', 'Peso_kg', 'Temperatura_C'])
                
                # Datos históricos de cada animal
                for animal in sistema.animales.values():
                    for i, (peso, temp) in enumerate(zip(animal.historial_peso, 
                                                         animal.historial_temperatura)):
                        writer.writerow([
                            animal.id,
                            animal.tipo,
                            i,
                            round(peso, 2),
                            round(temp, 1)
                        ])
            
            print(f"[PERSISTENCIA] ✓ Histórico exportado: {archivo}")
            return True
            
        except Exception as e:
            print(f"[ERROR] ✗ No se pudo exportar histórico: {e}")
            return False
    
    def limpiar_datos_antiguos(self, dias: int = 7):
        """
        Limpia archivos de datos más antiguos que N días.
        
        Args:
            dias: Días de antigüedad para eliminar
        """
        print(f"\n Limpiando archivos con más de {dias} días...")
        
        ahora = datetime.now()
        eliminados = 0
        
        for carpeta in [self.carpeta_data, self.carpeta_backups]:
            for archivo in os.listdir(carpeta):
                if archivo.endswith('.dat'):
                    ruta = os.path.join(carpeta, archivo)
                    fecha_mod = datetime.fromtimestamp(os.path.getmtime(ruta))
                    
                    if (ahora - fecha_mod).days > dias:
                        os.remove(ruta)
                        print(f"  Eliminado: {archivo}")
                        eliminados += 1
        
        print(f" {eliminados} archivo(s) eliminado(s)\n")
    
    def __str__(self):
        return "PersistenciaService(carpetas: data, reportes_csv, backups)"

# ================================================================================
# ARCHIVO 5/6: racion_service.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./servicios/racion_service.py
# ================================================================================

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

# ================================================================================
# ARCHIVO 6/6: reporte_service.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./servicios/reporte_service.py
# ================================================================================

"""
Servicio de Reportes - Generación automática de reportes

Servicio concurrente que genera reportes periódicos del feedlot.
"""

import threading
import time
from datetime import datetime
import os

class ReporteService:
    """
    Servicio que genera reportes automáticos del feedlot.
    
    Usa threading para generación periódica sin bloquear el sistema.
    Guarda reportes en archivos de texto.
    """
    
    def __init__(self, feedlot_system):
        """
        Inicializa el servicio de reportes.
        
        Args:
            feedlot_system: Instancia del FeedlotSystem (Singleton)
        """
        self.feedlot_system = feedlot_system
        self.activo = False
        self.thread = None
        self.intervalo = 15.0  # Generar reporte cada 15 segundos
        self.contador_reportes = 0
        
        # Crear carpeta de reportes
        self.carpeta_reportes = "reportes"
        if not os.path.exists(self.carpeta_reportes):
            os.makedirs(self.carpeta_reportes)
            print(f" Carpeta '{self.carpeta_reportes}/' creada")
        
        print(" Servicio de Reportes configurado")
    
    def iniciar(self):
        """
        Inicia el servicio de reportes en un hilo separado.
        """
        if not self.activo:
            self.activo = True
            self.thread = threading.Thread(target=self._ejecutar, daemon=True)
            self.thread.start()
            print(f"✓ Servicio de reportes iniciado (intervalo: {self.intervalo}s)")
    
    def detener(self):
        """
        Detiene el servicio de forma segura.
        """
        if self.activo:
            self.activo = False
            if self.thread:
                self.thread.join(timeout=2)
            print("✓ Servicio de reportes detenido")
    
    def _ejecutar(self):
        """
        Ejecuta el ciclo de generación de reportes.
        Corre en un hilo separado (daemon thread).
        """
        while self.activo:
            time.sleep(self.intervalo)
            self.generar_reporte()
    
    def generar_reporte(self):
        """
        Genera un reporte completo del feedlot.
        Este método se ejecuta periódicamente.
        """
        self.contador_reportes += 1
        self.feedlot_system.dia_actual += 1
        
        print("\n" + "="*70)
        print(f" REPORTE DIARIO - DÍA {self.feedlot_system.dia_actual}")
        print("="*70)
        
        stats = self.feedlot_system.obtener_estadisticas()
        
        if stats["total_animales"] == 0:
            print("  No hay animales en el sistema")
            print("="*70 + "\n")
            return
        
        # Información general
        print(f" Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f" Total de animales: {stats['total_animales']}")
        print(f"  Peso promedio actual: {stats['peso_promedio']:.2f} kg")
        print(f" Peso total: {stats['peso_total']:.2f} kg")
        print(f" Ganancia total promedio: {stats['ganancia_promedio']:.2f} kg")
        
        # Ganancia diaria estimada
        if self.feedlot_system.dia_actual > 0:
            gdp = stats['ganancia_promedio'] / self.feedlot_system.dia_actual
            print(f" Ganancia Diaria Promedio (GDP): {gdp:.2f} kg/día")
        
        print(f" Animales enfermos: {stats['animales_enfermos']} ({stats['porcentaje_enfermos']:.1f}%)")
        print(f" Corrales activos: {stats['total_corrales']}")
        print(f"  Total de alertas: {stats['alertas_activas']}")
        
        # Resumen de alertas si hay
        if stats['alertas_activas'] > 0:
            print(self.feedlot_system.observador_alertas.obtener_resumen_alertas())
        
        # Top 3 animales
        mejores = self.feedlot_system.obtener_mejores_animales(3)
        if mejores:
            print("\n TOP 3 ANIMALES (Mayor ganancia):")
            for i, animal in enumerate(mejores, 1):
                dias = max(1, self.feedlot_system.dia_actual)
                gdp_animal = animal.ganancia_peso_total() / dias
                print(f"  {i}. {animal.mostrar_info()} | GDP: {gdp_animal:.2f} kg/día")
        
        # Detalle por animal
        print("\n DETALLE POR ANIMAL:")
        print("-"*70)
        for animal in sorted(self.feedlot_system.animales.values(), key=lambda a: a.id):
            dias = max(1, self.feedlot_system.dia_actual)
            gdp = animal.ganancia_peso_total() / dias
            racion = animal.racion_actual or "Sin asignar"
            print(f"{animal.mostrar_info()} | GDP: {gdp:.2f} kg/día | Ración: {racion}")
        
        print("="*70 + "\n")
        
        # Guardar a archivo
        self._guardar_reporte_archivo(stats, mejores)
    
    def _guardar_reporte_archivo(self, stats: dict, mejores: list):
        """
        Guarda el reporte en un archivo de texto.
        
        Args:
            stats: Diccionario con estadísticas
            mejores: Lista de mejores animales
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"{self.carpeta_reportes}/reporte_dia{self.feedlot_system.dia_actual:03d}_{timestamp}.txt"
        
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                # Encabezado
                f.write("="*70 + "\n")
                f.write("ESTANCIA CARNES FINAS - REPORTE DÍA {}\n".format(self.feedlot_system.dia_actual))
                f.write("="*70 + "\n\n")
                
                # Información general
                f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Reporte #: {self.contador_reportes}\n\n")
                
                f.write("ESTADÍSTICAS GENERALES\n")
                f.write("-"*70 + "\n")
                f.write(f"Total animales: {stats['total_animales']}\n")
                f.write(f"Peso promedio: {stats['peso_promedio']:.2f} kg\n")
                f.write(f"Peso total: {stats['peso_total']:.2f} kg\n")
                f.write(f"Ganancia promedio: {stats['ganancia_promedio']:.2f} kg\n")
                f.write(f"Ganancia total: {stats['ganancia_total']:.2f} kg\n")
                
                if self.feedlot_system.dia_actual > 0:
                    gdp = stats['ganancia_promedio'] / self.feedlot_system.dia_actual
                    f.write(f"GDP (Ganancia Diaria Promedio): {gdp:.2f} kg/día\n")
                
                f.write(f"Animales enfermos: {stats['animales_enfermos']} ({stats['porcentaje_enfermos']:.1f}%)\n")
                f.write(f"Corrales: {stats['total_corrales']}\n")
                f.write(f"Alertas: {stats['alertas_activas']}\n\n")
                
                # Top animales
                if mejores:
                    f.write("TOP 3 ANIMALES (Mayor ganancia)\n")
                    f.write("-"*70 + "\n")
                    for i, animal in enumerate(mejores, 1):
                        dias = max(1, self.feedlot_system.dia_actual)
                        gdp_animal = animal.ganancia_peso_total() / dias
                        f.write(f"{i}. Animal #{animal.id} ({animal.tipo}) - "
                               f"Ganancia: +{animal.ganancia_peso_total():.2f} kg - "
                               f"GDP: {gdp_animal:.2f} kg/día\n")
                    f.write("\n")
                
                # Detalle por animal
                f.write("DETALLE POR ANIMAL\n")
                f.write("-"*70 + "\n")
                for animal in sorted(self.feedlot_system.animales.values(), key=lambda a: a.id):
                    dias = max(1, self.feedlot_system.dia_actual)
                    gdp = animal.ganancia_peso_total() / dias
                    racion = animal.racion_actual or "Sin asignar"
                    
                    f.write(f"Animal #{animal.id} ({animal.tipo})\n")
                    f.write(f"  Peso actual: {animal.peso:.2f} kg\n")
                    f.write(f"  Peso inicial: {animal.peso_inicial:.2f} kg\n")
                    f.write(f"  Ganancia total: +{animal.ganancia_peso_total():.2f} kg\n")
                    f.write(f"  GDP: {gdp:.2f} kg/día\n")
                    f.write(f"  Temperatura: {animal.temperatura:.1f}°C\n")
                    f.write(f"  Estado: {animal.estado_salud}\n")
                    f.write(f"  Ración: {racion}\n")
                    f.write("\n")
                
                # Alertas si hay
                if stats['alertas_activas'] > 0:
                    f.write("RESUMEN DE ALERTAS\n")
                    f.write("-"*70 + "\n")
                    f.write(self.feedlot_system.observador_alertas.obtener_resumen_alertas())
                    f.write("\n")
                
                f.write("="*70 + "\n")
                f.write("Fin del reporte\n")
            
            print(f" Reporte guardado: {nombre_archivo}")
            
        except Exception as e:
            print(f"✗ Error al guardar reporte: {e}")
    
    def generar_reporte_final(self):
        """
        Genera un reporte final completo al terminar la simulación.
        """
        print("\n" + "="*70)
        print(" REPORTE FINAL - ESTANCIA CARNES FINAS")
        print("="*70)
        
        stats = self.feedlot_system.obtener_estadisticas()
        
        if stats["total_animales"] == 0:
            print("  No hay datos para reportar")
            print("="*70 + "\n")
            return
        
        # Resumen general
        print(f" Días totales de operación: {self.feedlot_system.dia_actual}")
        print(f" Reportes generados: {self.contador_reportes}")
        print(f" Total animales: {stats['total_animales']}")
        print(f" Ganancia total del feedlot: {stats['ganancia_total']:.2f} kg")
        print(f"  Peso final promedio: {stats['peso_promedio']:.2f} kg")
        print(f" Peso total final: {stats['peso_total']:.2f} kg")
        
        if self.feedlot_system.dia_actual > 0:
            gdp_general = stats['ganancia_promedio'] / self.feedlot_system.dia_actual
            print(f" GDP General: {gdp_general:.2f} kg/día")
        
        print(f" Total animales enfermos: {stats['animales_enfermos']}")
        print(f" Total alertas generadas: {stats['alertas_activas']}")
        
        # Top 5 mejores animales
        print("\n TOP 5 MEJORES ANIMALES:")
        mejores = self.feedlot_system.obtener_mejores_animales(5)
        for i, animal in enumerate(mejores, 1):
            dias = max(1, self.feedlot_system.dia_actual)
            gdp = animal.ganancia_peso_total() / dias
            print(f"  {i}. {animal.mostrar_info()} | GDP: {gdp:.2f} kg/día")
        
        # Animales con alertas
        animales_alerta = self.feedlot_system.obtener_animales_alerta()
        if animales_alerta:
            print(f"\n  ANIMALES CON ALERTAS ({len(animales_alerta)}):")
            for animal in animales_alerta:
                print(f"  • {animal.mostrar_info()}")
        
        # Estadísticas por corral
        if self.feedlot_system.corrales:
            print("\n ESTADÍSTICAS POR CORRAL:")
            for corral in sorted(self.feedlot_system.corrales.values(), key=lambda c: c.numero):
                stats_corral = corral.obtener_estadisticas()
                print(f"  {corral}: Peso prom. {stats_corral['peso_promedio']:.1f} kg, "
                      f"Uso {stats_corral['capacidad_usada']:.0f}%")
        
        print("\n" + "="*70)
        print(" SIMULACIÓN COMPLETADA EXITOSAMENTE")
        print("="*70 + "\n")
        
        # Guardar reporte final
        self._guardar_reporte_final(stats, mejores)
    
    def _guardar_reporte_final(self, stats: dict, mejores: list):
        """
        Guarda el reporte final en un archivo especial.
        
        Args:
            stats: Diccionario con estadísticas
            mejores: Lista de mejores animales
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"{self.carpeta_reportes}/REPORTE_FINAL_{timestamp}.txt"
        
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                f.write("="*70 + "\n")
                f.write("ESTANCIA CARNES FINAS - REPORTE FINAL\n")
                f.write("="*70 + "\n\n")
                
                f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Días de operación: {self.feedlot_system.dia_actual}\n")
                f.write(f"Reportes generados: {self.contador_reportes}\n\n")
                
                f.write("RESUMEN EJECUTIVO\n")
                f.write("-"*70 + "\n")
                f.write(f"Total animales: {stats['total_animales']}\n")
                f.write(f"Ganancia total: {stats['ganancia_total']:.2f} kg\n")
                f.write(f"Peso final promedio: {stats['peso_promedio']:.2f} kg\n")
                
                if self.feedlot_system.dia_actual > 0:
                    gdp = stats['ganancia_promedio'] / self.feedlot_system.dia_actual
                    f.write(f"GDP General: {gdp:.2f} kg/día\n")
                
                f.write(f"Tasa de enfermedad: {stats['porcentaje_enfermos']:.1f}%\n")
                f.write(f"Total alertas: {stats['alertas_activas']}\n\n")
                
                f.write("TOP 5 MEJORES ANIMALES\n")
                f.write("-"*70 + "\n")
                for i, animal in enumerate(mejores, 1):
                    dias = max(1, self.feedlot_system.dia_actual)
                    gdp = animal.ganancia_peso_total() / dias
                    f.write(f"{i}. {animal} - Ganancia: +{animal.ganancia_peso_total():.2f} kg "
                           f"(GDP: {gdp:.2f} kg/día)\n")
                
                f.write("\n" + "="*70 + "\n")
                f.write("Fin del reporte final\n")
            
            print(f" Reporte final guardado: {nombre_archivo}")
            
        except Exception as e:
            print(f"✗ Error al guardar reporte final: {e}")
    
    def __str__(self):
        return f"ReporteService(reportes={self.contador_reportes}, activo={self.activo})"

