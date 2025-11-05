"""
Servicio de Persistencia - Guarda y carga el estado del sistema
Permite guardar el estado completo del feedlot y continuar simulaciones.
"""

from excepciones.feedlot_exceptions import PersistenciaException
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
        raise PersistenciaException(f"Error al guardar estado: {e}")
    
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
        raise PersistenciaException(f"Error al cargar estado: {e}") 


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