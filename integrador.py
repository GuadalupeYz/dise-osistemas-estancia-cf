"""
Archivo integrador generado automaticamente
Directorio: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/.
Fecha: 2025-11-05 20:04:58
Total de archivos integrados: 3
"""

# ================================================================================
# ARCHIVO 1/3: buscar_paquete.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./buscar_paquete.py
# ================================================================================

"""
Script para buscar el paquete python_forestacion desde el directorio raiz del proyecto.
Incluye funcionalidad para integrar archivos Python en cada nivel del arbol de directorios.
"""
import os
import sys
from datetime import datetime


def buscar_paquete(directorio_raiz: str, nombre_paquete: str) -> list:
    """
    Busca un paquete Python en el directorio raiz y subdirectorios.

    Args:
        directorio_raiz: Directorio desde donde iniciar la busqueda
        nombre_paquete: Nombre del paquete a buscar

    Returns:
        Lista de rutas donde se encontro el paquete
    """
    paquetes_encontrados = []

    for raiz, directorios, archivos in os.walk(directorio_raiz):
        # Verificar si el directorio actual es el paquete buscado
        nombre_dir = os.path.basename(raiz)

        if nombre_dir == nombre_paquete:
            # Verificar que sea un paquete Python (contiene __init__.py)
            if '__init__.py' in archivos:
                paquetes_encontrados.append(raiz)
                print(f"[+] Paquete encontrado: {raiz}")
            else:
                print(f"[!] Directorio encontrado pero no es un paquete Python: {raiz}")

    return paquetes_encontrados


def obtener_archivos_python(directorio: str) -> list:
    """
    Obtiene todos los archivos Python en un directorio (sin recursion).

    Args:
        directorio: Ruta del directorio a examinar

    Returns:
        Lista de rutas completas de archivos .py
    """
    archivos_python = []
    try:
        for item in os.listdir(directorio):
            ruta_completa = os.path.join(directorio, item)
            if os.path.isfile(ruta_completa) and item.endswith('.py'):
                # Excluir archivos integradores para evitar recursion infinita
                if item not in ['integrador.py', 'integradorFinal.py']:
                    archivos_python.append(ruta_completa)
    except PermissionError:
        print(f"[!] Sin permisos para leer: {directorio}")

    return sorted(archivos_python)


def obtener_subdirectorios(directorio: str) -> list:
    """
    Obtiene todos los subdirectorios inmediatos de un directorio.

    Args:
        directorio: Ruta del directorio a examinar

    Returns:
        Lista de rutas completas de subdirectorios
    """
    subdirectorios = []
    try:
        for item in os.listdir(directorio):
            ruta_completa = os.path.join(directorio, item)
            if os.path.isdir(ruta_completa):
                # Excluir directorios especiales
                if not item.startswith('.') and item not in ['__pycache__', 'venv', '.venv']:
                    subdirectorios.append(ruta_completa)
    except PermissionError:
        print(f"[!] Sin permisos para leer: {directorio}")

    return sorted(subdirectorios)


def leer_contenido_archivo(ruta_archivo: str) -> str:
    """
    Lee el contenido de un archivo Python.

    Args:
        ruta_archivo: Ruta completa del archivo

    Returns:
        Contenido del archivo como string
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except Exception as error:
        print(f"[!] Error al leer {ruta_archivo}: {error}")
        return f"# Error al leer este archivo: {error}\n"


def crear_archivo_integrador(directorio: str, archivos_python: list) -> bool:
    """
    Crea un archivo integrador.py con el contenido de todos los archivos Python.

    Args:
        directorio: Directorio donde crear el archivo integrador
        archivos_python: Lista de rutas de archivos Python a integrar

    Returns:
        True si se creo exitosamente, False en caso contrario
    """
    if not archivos_python:
        return False

    ruta_integrador = os.path.join(directorio, 'integrador.py')

    try:
        with open(ruta_integrador, 'w', encoding='utf-8') as integrador:
            # Encabezado
            integrador.write('"""\n')
            integrador.write(f"Archivo integrador generado automaticamente\n")
            integrador.write(f"Directorio: {directorio}\n")
            integrador.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            integrador.write(f"Total de archivos integrados: {len(archivos_python)}\n")
            integrador.write('"""\n\n')

            # Integrar cada archivo
            for idx, archivo in enumerate(archivos_python, 1):
                nombre_archivo = os.path.basename(archivo)
                integrador.write(f"# {'=' * 80}\n")
                integrador.write(f"# ARCHIVO {idx}/{len(archivos_python)}: {nombre_archivo}\n")
                integrador.write(f"# Ruta: {archivo}\n")
                integrador.write(f"# {'=' * 80}\n\n")

                contenido = leer_contenido_archivo(archivo)
                integrador.write(contenido)
                integrador.write("\n\n")

        print(f"[OK] Integrador creado: {ruta_integrador}")
        print(f"     Archivos integrados: {len(archivos_python)}")
        return True

    except Exception as error:
        print(f"[!] Error al crear integrador en {directorio}: {error}")
        return False


def procesar_directorio_recursivo(directorio: str, nivel: int = 0, archivos_totales: list = None) -> list:
    """
    Procesa un directorio de forma recursiva, creando integradores en cada nivel.
    Utiliza DFS (Depth-First Search) para llegar primero a los niveles mas profundos.

    Args:
        directorio: Directorio a procesar
        nivel: Nivel de profundidad actual (para logging)
        archivos_totales: Lista acumulativa de todos los archivos procesados

    Returns:
        Lista de todos los archivos Python procesados en el arbol
    """
    if archivos_totales is None:
        archivos_totales = []

    indentacion = "  " * nivel
    print(f"{indentacion}[INFO] Procesando nivel {nivel}: {os.path.basename(directorio)}")

    # Obtener subdirectorios
    subdirectorios = obtener_subdirectorios(directorio)

    # Primero, procesar recursivamente todos los subdirectorios (DFS)
    for subdir in subdirectorios:
        procesar_directorio_recursivo(subdir, nivel + 1, archivos_totales)

    # Despues de procesar subdirectorios, procesar archivos del nivel actual
    archivos_python = obtener_archivos_python(directorio)

    if archivos_python:
        print(f"{indentacion}[+] Encontrados {len(archivos_python)} archivo(s) Python")
        crear_archivo_integrador(directorio, archivos_python)
        # Agregar archivos a la lista total
        archivos_totales.extend(archivos_python)
    else:
        print(f"{indentacion}[INFO] No hay archivos Python en este nivel")

    return archivos_totales


def crear_integrador_final(directorio_raiz: str, archivos_totales: list) -> bool:
    """
    Crea un archivo integradorFinal.py con TODO el codigo fuente de todas las ramas.

    Args:
        directorio_raiz: Directorio donde crear el archivo integrador final
        archivos_totales: Lista completa de todos los archivos Python procesados

    Returns:
        True si se creo exitosamente, False en caso contrario
    """
    if not archivos_totales:
        print("[!] No hay archivos para crear el integrador final")
        return False

    ruta_integrador_final = os.path.join(directorio_raiz, 'integradorFinal.py')

    # Organizar archivos por directorio para mejor estructura
    archivos_por_directorio = {}
    for archivo in archivos_totales:
        directorio = os.path.dirname(archivo)
        if directorio not in archivos_por_directorio:
            archivos_por_directorio[directorio] = []
        archivos_por_directorio[directorio].append(archivo)

    try:
        with open(ruta_integrador_final, 'w', encoding='utf-8') as integrador_final:
            # Encabezado principal
            integrador_final.write('"""\n')
            integrador_final.write("INTEGRADOR FINAL - CONSOLIDACION COMPLETA DEL PROYECTO\n")
            integrador_final.write("=" * 76 + "\n")
            integrador_final.write(f"Directorio raiz: {directorio_raiz}\n")
            integrador_final.write(f"Fecha de generacion: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            integrador_final.write(f"Total de archivos integrados: {len(archivos_totales)}\n")
            integrador_final.write(f"Total de directorios procesados: {len(archivos_por_directorio)}\n")
            integrador_final.write("=" * 76 + "\n")
            integrador_final.write('"""\n\n')

            # Tabla de contenidos
            integrador_final.write("# " + "=" * 78 + "\n")
            integrador_final.write("# TABLA DE CONTENIDOS\n")
            integrador_final.write("# " + "=" * 78 + "\n\n")

            contador_global = 1
            for directorio in sorted(archivos_por_directorio.keys()):
                dir_relativo = os.path.relpath(directorio, directorio_raiz)
                integrador_final.write(f"# DIRECTORIO: {dir_relativo}\n")
                for archivo in sorted(archivos_por_directorio[directorio]):
                    nombre_archivo = os.path.basename(archivo)
                    integrador_final.write(f"#   {contador_global}. {nombre_archivo}\n")
                    contador_global += 1
                integrador_final.write("#\n")

            integrador_final.write("\n\n")

            # Contenido completo organizado por directorio
            contador_global = 1
            for directorio in sorted(archivos_por_directorio.keys()):
                dir_relativo = os.path.relpath(directorio, directorio_raiz)

                # Separador de directorio
                integrador_final.write("\n" + "#" * 80 + "\n")
                integrador_final.write(f"# DIRECTORIO: {dir_relativo}\n")
                integrador_final.write("#" * 80 + "\n\n")

                # Procesar cada archivo del directorio
                for archivo in sorted(archivos_por_directorio[directorio]):
                    nombre_archivo = os.path.basename(archivo)

                    integrador_final.write(f"# {'=' * 78}\n")
                    integrador_final.write(f"# ARCHIVO {contador_global}/{len(archivos_totales)}: {nombre_archivo}\n")
                    integrador_final.write(f"# Directorio: {dir_relativo}\n")
                    integrador_final.write(f"# Ruta completa: {archivo}\n")
                    integrador_final.write(f"# {'=' * 78}\n\n")

                    contenido = leer_contenido_archivo(archivo)
                    integrador_final.write(contenido)
                    integrador_final.write("\n\n")

                    contador_global += 1

            # Footer
            integrador_final.write("\n" + "#" * 80 + "\n")
            integrador_final.write("# FIN DEL INTEGRADOR FINAL\n")
            integrador_final.write(f"# Total de archivos: {len(archivos_totales)}\n")
            integrador_final.write(f"# Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            integrador_final.write("#" * 80 + "\n")

        print(f"\n[OK] Integrador final creado: {ruta_integrador_final}")
        print(f"     Total de archivos integrados: {len(archivos_totales)}")
        print(f"     Total de directorios procesados: {len(archivos_por_directorio)}")

        # Mostrar tamanio del archivo
        tamanio = os.path.getsize(ruta_integrador_final)
        if tamanio < 1024:
            tamanio_str = f"{tamanio} bytes"
        elif tamanio < 1024 * 1024:
            tamanio_str = f"{tamanio / 1024:.2f} KB"
        else:
            tamanio_str = f"{tamanio / (1024 * 1024):.2f} MB"
        print(f"     Tamanio del archivo: {tamanio_str}")

        return True

    except Exception as error:
        print(f"[!] Error al crear integrador final: {error}")
        return False


def integrar_arbol_directorios(directorio_raiz: str) -> None:
    """
    Inicia el proceso de integracion para todo el arbol de directorios.

    Args:
        directorio_raiz: Directorio raiz desde donde comenzar
    """
    print("\n" + "=" * 80)
    print("INICIANDO INTEGRACION DE ARCHIVOS PYTHON")
    print("=" * 80)
    print(f"Directorio raiz: {directorio_raiz}\n")

    # Procesar directorios y obtener lista de todos los archivos
    archivos_totales = procesar_directorio_recursivo(directorio_raiz)

    print("\n" + "=" * 80)
    print("INTEGRACION POR NIVELES COMPLETADA")
    print("=" * 80)

    # Crear integrador final con todos los archivos
    if archivos_totales:
        print("\n" + "=" * 80)
        print("CREANDO INTEGRADOR FINAL")
        print("=" * 80)
        crear_integrador_final(directorio_raiz, archivos_totales)

    print("\n" + "=" * 80)
    print("PROCESO COMPLETO FINALIZADO")
    print("=" * 80)


def main():
    """Funcion principal del script."""
    # Obtener el directorio raiz del proyecto (donde esta este script)
    directorio_raiz = os.path.dirname(os.path.abspath(__file__))

    # Verificar argumentos de linea de comandos
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()

        if comando == "integrar":
            # Modo de integracion de archivos
            if len(sys.argv) > 2:
                directorio_objetivo = sys.argv[2]
                if not os.path.isabs(directorio_objetivo):
                    directorio_objetivo = os.path.join(directorio_raiz, directorio_objetivo)
            else:
                directorio_objetivo = directorio_raiz

            if not os.path.isdir(directorio_objetivo):
                print(f"[!] El directorio no existe: {directorio_objetivo}")
                return 1

            integrar_arbol_directorios(directorio_objetivo)
            return 0

        elif comando == "help" or comando == "--help" or comando == "-h":
            print("Uso: python buscar_paquete.py [COMANDO] [OPCIONES]")
            print("")
            print("Comandos disponibles:")
            print("  (sin argumentos)     Busca el paquete python_forestacion")
            print("  integrar [DIR]       Integra archivos Python en el arbol de directorios")
            print("                       DIR: directorio raiz (por defecto: directorio actual)")
            print("  help                 Muestra esta ayuda")
            print("")
            print("Ejemplos:")
            print("  python buscar_paquete.py")
            print("  python buscar_paquete.py integrar")
            print("  python buscar_paquete.py integrar python_forestacion")
            return 0

        else:
            print(f"[!] Comando desconocido: {comando}")
            print("    Use 'python buscar_paquete.py help' para ver los comandos disponibles")
            return 1

    # Modo por defecto: buscar paquete
    print(f"[INFO] Buscando desde: {directorio_raiz}")
    print(f"[INFO] Buscando paquete: python_forestacion")
    print("")

    # Buscar el paquete
    paquetes = buscar_paquete(directorio_raiz, "python_forestacion")

    print("")
    if paquetes:
        print(f"[OK] Se encontraron {len(paquetes)} paquete(s):")
        for paquete in paquetes:
            print(f"  - {paquete}")

            # Mostrar estructura basica del paquete
            print(f"    Contenido:")
            try:
                contenido = os.listdir(paquete)
                for item in sorted(contenido)[:10]:  # Mostrar primeros 10 items
                    ruta_item = os.path.join(paquete, item)
                    if os.path.isdir(ruta_item):
                        print(f"      [DIR]  {item}")
                    else:
                        print(f"      [FILE] {item}")
                if len(contenido) > 10:
                    print(f"      ... y {len(contenido) - 10} items mas")
            except PermissionError:
                print(f"      [!] Sin permisos para leer el directorio")
    else:
        print("[!] No se encontro el paquete python_forestacion")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

# ================================================================================
# ARCHIVO 2/3: constantes.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./constantes.py
# ================================================================================


INTERVALO_SENSOR_PESO = 8.0
INTERVALO_SENSOR_TEMP = 6.0
INTERVALO_RACIONES = 10.0
INTERVALO_REPORTES = 15.0
INTERVALO_BACKUP = 40.0

# ================================================================================
# ARCHIVO 3/3: main.py
# Ruta: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./main.py
# ================================================================================

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════╗
║          ESTANCIA CARNES FINAS - Sistema de Gestión de Feedlot        ║
║                    Desarrollado por: Guadalupe Yañez                  ║
╚═══════════════════════════════════════════════════════════════════════╝

Sistema automatizado completo con:
- Patrón Singleton, Factory, Observer, Strategy
- Programación concurrente (Threading)
- Persistencia de datos (.dat y .csv)
- Sistema de logging completo
- Observador de salud avanzado
- Módulo veterinario profesional

Versión: 2.0 - Con módulos avanzados
"""

import time
import sys
import os

# Servicios principales
from servicios.feedlot_service import FeedlotSystem
from servicios.racion_service import RacionService
from servicios.reporte_service import ReporteService

# Servicios avanzados (NUEVOS)
from servicios.persistencia_service import PersistenciaService
from servicios.log_service import LogService

# Patrones
from patrones.factory import AnimalFactory
from patrones.salud_observer import SaludObserver

# Estrategias
from estrategias.racion_intensiva import RacionIntensiva
from estrategias.racion_mantenimiento import RacionMantenimiento

# Entidades
from entidades.veterinario import Veterinario


def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_banner():
    """Muestra el banner inicial del sistema"""
    print("\n" + "="*70)
    print("🐄" + " "*10 + "ESTANCIA CARNES FINAS" + " "*10 + "🐄")
    print(" "*6 + "Sistema Inteligente de Gestión de Feedlot")
    print("="*70)
    print(" Ubicación: Mendoza, Argentina")
    print(" Desarrollado por: Guadalupe Yañez")
    print(" Calidad Premium en Engorde de Ganado")
    print(" Versión 2.0 - Con módulos avanzados")
    print("="*70 + "\n")


def mostrar_info_patrones():
    """Muestra información sobre los patrones y módulos"""
    print(" PATRONES DE DISEÑO:")
    print("-"*70)
    print("✓ Singleton: FeedlotSystem (instancia única)")
    print("✓ Factory: AnimalFactory (creación automática)")
    print("✓ Observer: SaludObserver + ObservadorAlerta (notificaciones)")
    print("✓ Strategy: Raciones (Normal, Intensiva, Mantenimiento)")
    print("-"*70)
    print(" PROGRAMACIÓN CONCURRENTE:")
    print("-"*70)
    print("✓ Hilos de sensores (peso y temperatura)")
    print("✓ Servicio de raciones automático")
    print("✓ Servicio de reportes periódicos")
    print("-"*70)
    print(" MÓDULOS AVANZADOS:")
    print("-"*70)
    print("✓ Persistencia: Guardar/Cargar estado (.dat)")
    print("✓ Logging: Bitácora completa de eventos")
    print("✓ Salud: Observador médico con acciones automáticas")
    print("✓ Veterinario: Profesional con diagnósticos")
    print("-"*70 + "\n")


def configurar_feedlot(log_service=None):
    """Configura el sistema con animales iniciales"""
    sistema = FeedlotSystem()
    
    if log_service:
        log_service.crear_seccion("CONFIGURACIÓN DEL FEEDLOT")
    
    print("  CONFIGURANDO FEEDLOT...")
    print("-"*70)
    
    # Animales a crear
    animales_config = [
        (1, "Ternero", 180.0),
        (2, "Novillo", 280.0),
        (3, "Novillo", 300.0),
        (4, "Toro", 450.0),
        (5, "Ternero", 200.0),
    ]
    
    print(f" Creando {len(animales_config)} animales...\n")
    
    for id_animal, tipo, peso in animales_config:
        animal, sensor_peso, sensor_temp = AnimalFactory.crear_animal_completo(
            id_animal, tipo, peso,
            intervalo_peso=8.0,
            intervalo_temp=6.0
        )
        
        sistema.agregar_animal(animal, numero_corral=1 if id_animal <= 3 else 2)
        sistema.agregar_sensor(sensor_peso)
        sistema.agregar_sensor(sensor_temp)
        
        if log_service:
            log_service.info(f"Animal {id_animal} ({tipo}) creado - Peso: {peso} kg")
    
    print("-"*70)
    print(f" Configuración completada")
    print(f"   • {len(sistema.animales)} animales")
    print(f"   • {len(sistema.sensores)} sensores")
    print(f"   • {len(sistema.corrales)} corrales")
    print("-"*70 + "\n")
    
    return sistema


def ejecutar_simulacion(duracion_segundos: int = 60, continuar: bool = False):
    """
    Ejecuta la simulación completa con todos los módulos.
    
    Args:
        duracion_segundos: Duración en segundos
        continuar: Si True, intenta cargar estado anterior
    """
    # Banner
    mostrar_banner()
    mostrar_info_patrones()
    
    # Inicializar servicios avanzados
    print("🔧 Inicializando servicios avanzados...")
    persistencia = PersistenciaService()
    log_service = LogService()
    log_service.ok("Sistema iniciado")
    print()
    
    # Configurar o cargar sistema
    if continuar:
        print(" Intentando cargar estado anterior...")
        estado = persistencia.cargar_estado()
        if estado:
            sistema = FeedlotSystem()
            persistencia.restaurar_sistema(sistema, estado)
            log_service.persistencia(f"Estado restaurado desde día {sistema.dia_actual}")
        else:
            print("  No se pudo cargar, iniciando nuevo sistema\n")
            sistema = configurar_feedlot(log_service)
    else:
        sistema = configurar_feedlot(log_service)
    
    # Crear servicios
    servicio_raciones = RacionService(sistema)
    servicio_reportes = ReporteService(sistema)
    
    # NUEVO: Crear observador de salud avanzado
    observador_salud = SaludObserver(log_service)
    for sensor in sistema.sensores:
        sensor.agregar_observador(observador_salud)
    
    # NUEVO: Crear veterinario
    veterinario = Veterinario("Dra. María González", "MP-8745", "Bovinos")
    log_service.info(f"Veterinario {veterinario.nombre} incorporado")
    print()
    
    # Configurar estrategias
    print("  CONFIGURANDO ESTRATEGIAS...")
    print("-"*70)
    servicio_raciones.asignar_estrategia(1, RacionIntensiva())
    servicio_raciones.asignar_estrategia(5, RacionIntensiva())
    servicio_raciones.asignar_estrategia(4, RacionMantenimiento())
    print(" Estrategias configuradas")
    print("-"*70 + "\n")
    
    log_service.info("Estrategias de alimentación configuradas")
    
    try:
        # Iniciar servicios
        sistema.iniciar_monitoreo()
        servicio_raciones.iniciar()
        servicio_reportes.iniciar()
        
        log_service.registrar_inicio_sistema(
            len(sistema.animales),
            len(sistema.sensores)
        )
        
        print(f"  SIMULACIÓN - Duración: {duracion_segundos}s")
        print(" Presiona Ctrl+C para detener\n")
        print("="*70 + "\n")
        
        tiempo_inicio = time.time()
        ultimo_estado = tiempo_inicio
        ultimo_chequeo_salud = tiempo_inicio
        ultimo_backup = tiempo_inicio
        
        # Ciclo principal
        while time.time() - tiempo_inicio < duracion_segundos:
            time.sleep(1)
            
            # Mostrar estado cada 20s
            if time.time() - ultimo_estado >= 20:
                sistema.mostrar_estado()
                ultimo_estado = time.time()
            
            # Chequeo veterinario cada 30s
            if time.time() - ultimo_chequeo_salud >= 30:
                print("\n [VETERINARIO] Ronda médica...")
                for animal in sistema.obtener_animales_alerta():
                    veterinario.revisar_animal(animal)
                    
                    # Aplicar tratamiento si es necesario
                    if animal.temperatura >= 39.5:
                        veterinario.aplicar_tratamiento(animal, 'antipiretrico')
                
                observador_salud.mostrar_estado_tratamientos()
                ultimo_chequeo_salud = time.time()
            
            # Backup automático cada 40s
            if time.time() - ultimo_backup >= 40:
                print("\n Creando backup automático...")
                persistencia.crear_backup(sistema)
                log_service.persistencia("Backup automático creado")
                ultimo_backup = time.time()
        
        print("\n Simulación completada\n")
        log_service.ok(f"Simulación completada - {duracion_segundos}s")
        
    except KeyboardInterrupt:
        print("\n\n SIMULACIÓN INTERRUMPIDA\n")
        log_service.warning("Simulación interrumpida por usuario")
    
    finally:
        # Detener servicios
        print(" Finalizando sistema...")
        print("-"*70)
        sistema.detener_monitoreo()
        servicio_raciones.detener()
        servicio_reportes.detener()
        print("-"*70 + "\n")
        
        time.sleep(1)
        
        # Mostrar estados finales
        sistema.listar_animales()
        sistema.listar_corrales()
        servicio_raciones.mostrar_resumen_estrategias()
        observador_salud.mostrar_estado_tratamientos()
        
        # Reporte final
        servicio_reportes.generar_reporte_final()
        
        # Informe veterinario
        print(observador_salud.generar_informe_veterinario())
        
        # Estadísticas del veterinario
        stats_vet = veterinario.obtener_estadisticas()
        print(f"   ESTADÍSTICAS - {veterinario}")
        print(f"   Animales atendidos: {stats_vet['animales_atendidos']}")
        print(f"   Tratamientos: {stats_vet['tratamientos_realizados']}")
        print(f"   Diagnósticos: {stats_vet['diagnosticos_realizados']}\n")
        
        # Guardar estado final
        print(" Guardando estado final...")
        persistencia.guardar_estado(sistema)
        persistencia.exportar_reporte_csv(sistema)
        persistencia.exportar_historico_animales(sistema)
        
        stats = sistema.obtener_estadisticas()
        log_service.registrar_fin_sistema(
            sistema.dia_actual,
            stats['ganancia_total']
        )
        
        # Finalizar log
        log_service.mostrar_resumen()
        log_service.finalizar_log()
        
        # Mensaje final
        print("\n" + "="*70)
        print(" SIMULACIÓN FINALIZADA")
        print("="*70)
        print(" Archivos generados:")
        print(f"   • Reportes: ./reportes/")
        print(f"   • CSV: ./reportes_csv/")
        print(f"   • Estados: ./data/")
        print(f"   • Logs: ./logs/")
        print("="*70 + "\n")


def menu_interactivo():
    """Menú interactivo mejorado"""
    limpiar_pantalla()
    mostrar_banner()
    
    print(" MENÚ PRINCIPAL")
    print("="*70)
    print("1.  Simulación rápida (30s)")
    print("2.  Simulación estándar (60s)")
    print("3.  Simulación extendida (120s)")
    print("4.  Configuración personalizada")
    print("5.  Continuar simulación anterior")
    print("6.  Ver archivos guardados")
    print("7.  Información de patrones")
    print("8.  Salir")
    print("="*70)
    
    try:
        opcion = input("\n Seleccione (1-8): ").strip()
        
        if opcion == "1":
            limpiar_pantalla()
            ejecutar_simulacion(30)
            
        elif opcion == "2":
            limpiar_pantalla()
            ejecutar_simulacion(60)
            
        elif opcion == "3":
            limpiar_pantalla()
            ejecutar_simulacion(120)
            
        elif opcion == "4":
            try:
                duracion = int(input("  Duración (1-600s): "))
                if 1 <= duracion <= 600:
                    limpiar_pantalla()
                    ejecutar_simulacion(duracion)
                else:
                    print(" Debe estar entre 1 y 600")
                    time.sleep(2)
                    menu_interactivo()
            except ValueError:
                print(" Número inválido")
                time.sleep(2)
                menu_interactivo()
        
        elif opcion == "5":
            limpiar_pantalla()
            print("\n Continuando simulación anterior...\n")
            time.sleep(1)
            ejecutar_simulacion(60, continuar=True)
        
        elif opcion == "6":
            limpiar_pantalla()
            mostrar_banner()
            persistencia = PersistenciaService()
            persistencia.listar_estados_guardados()
            input("\n Presiona ENTER para volver...")
            menu_interactivo()
        
        elif opcion == "7":
            limpiar_pantalla()
            mostrar_banner()
            mostrar_info_patrones()
            input("\n Presiona ENTER para volver...")
            menu_interactivo()
        
        elif opcion == "8":
            print("\n ¡Hasta pronto!")
            print(" Estancia Carnes Finas\n")
            sys.exit(0)
        
        else:
            print(" Opción inválida")
            time.sleep(2)
            menu_interactivo()
            
    except KeyboardInterrupt:
        print("\n\n ¡Hasta pronto!\n")
        sys.exit(0)


def main():
    """Función principal"""
    try:
        if len(sys.argv) > 1:
            try:
                duracion = int(sys.argv[1])
                if 1 <= duracion <= 600:
                    ejecutar_simulacion(duracion)
                else:
                    print(" Duración: 1-600 segundos")
                    print(" Uso: python main.py [segundos]")
            except ValueError:
                print(" Argumento inválido")
                print(" Uso: python main.py [segundos]")
                time.sleep(2)
                menu_interactivo()
        else:
            menu_interactivo()
            
    except Exception as e:
        print(f"\n Error crítico: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

