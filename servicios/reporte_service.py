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