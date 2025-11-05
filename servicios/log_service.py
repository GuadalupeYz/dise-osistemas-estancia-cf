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