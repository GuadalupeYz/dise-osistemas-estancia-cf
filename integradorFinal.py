"""
INTEGRADOR FINAL - CONSOLIDACION COMPLETA DEL PROYECTO
============================================================================
Directorio raiz: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/.
Fecha de generacion: 2025-11-05 20:04:58
Total de archivos integrados: 26
Total de directorios procesados: 6
============================================================================
"""

# ==============================================================================
# TABLA DE CONTENIDOS
# ==============================================================================

# DIRECTORIO: .
#   1. buscar_paquete.py
#   2. constantes.py
#   3. main.py
#
# DIRECTORIO: entidades
#   4. __init__.py
#   5. animal.py
#   6. corral.py
#   7. sensor.py
#   8. veterinario.py
#
# DIRECTORIO: estrategias
#   9. __init__.py
#   10. estrategia_racion.py
#   11. racion_intensiva.py
#   12. racion_mantenimiento.py
#   13. racion_normal.py
#
# DIRECTORIO: excepciones
#   14. __init__.py
#   15. feedlot_exceptions.py
#
# DIRECTORIO: patrones
#   16. __init__.py
#   17. factory.py
#   18. observer.py
#   19. salud_observer.py
#   20. singleton.py
#
# DIRECTORIO: servicios
#   21. __init__.py
#   22. feedlot_service.py
#   23. log_service.py
#   24. persistencia_service.py
#   25. racion_service.py
#   26. reporte_service.py
#



################################################################################
# DIRECTORIO: .
################################################################################

# ==============================================================================
# ARCHIVO 1/26: buscar_paquete.py
# Directorio: .
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./buscar_paquete.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 2/26: constantes.py
# Directorio: .
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./constantes.py
# ==============================================================================


INTERVALO_SENSOR_PESO = 8.0
INTERVALO_SENSOR_TEMP = 6.0
INTERVALO_RACIONES = 10.0
INTERVALO_REPORTES = 15.0
INTERVALO_BACKUP = 40.0

# ==============================================================================
# ARCHIVO 3/26: main.py
# Directorio: .
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./main.py
# ==============================================================================

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


################################################################################
# DIRECTORIO: entidades
################################################################################

# ==============================================================================
# ARCHIVO 4/26: __init__.py
# Directorio: entidades
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./entidades/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 5/26: animal.py
# Directorio: entidades
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./entidades/animal.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 6/26: corral.py
# Directorio: entidades
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./entidades/corral.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 7/26: sensor.py
# Directorio: entidades
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./entidades/sensor.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 8/26: veterinario.py
# Directorio: entidades
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./entidades/veterinario.py
# ==============================================================================

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


################################################################################
# DIRECTORIO: estrategias
################################################################################

# ==============================================================================
# ARCHIVO 9/26: __init__.py
# Directorio: estrategias
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./estrategias/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 10/26: estrategia_racion.py
# Directorio: estrategias
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./estrategias/estrategia_racion.py
# ==============================================================================

"""
Patrón Strategy - Interfaz para estrategias de alimentación

El patrón Strategy define una familia de algoritmos (estrategias de alimentación),
los encapsula y los hace intercambiables. Permite que el algoritmo varíe
independientemente de los clientes que lo utilizan.
"""

from abc import ABC, abstractmethod

class EstrategiaRacion(ABC):
    """
    Interfaz abstracta para el patrón Strategy.
    
    Define el contrato que todas las estrategias de alimentación
    deben implementar.
    
    Cada estrategia concreta implementará su propio algoritmo
    de alimentación con diferentes incrementos de peso.
    """
    
    @abstractmethod
    def aplicar_racion(self, animal) -> float:
        """
        Aplica la estrategia de alimentación al animal.
        
        Este es el método principal que debe ser implementado
        por cada estrategia concreta.
        
        Args:
            animal: Objeto Animal al que se aplicará la ración
            
        Returns:
            float: Incremento de peso esperado en kg
        """
        pass
    
    @abstractmethod
    def obtener_nombre(self) -> str:
        """
        Retorna el nombre de la estrategia.
        
        Returns:
            str: Nombre descriptivo de la estrategia
        """
        pass
    
    @abstractmethod
    def obtener_descripcion(self) -> str:
        """
        Retorna una descripción detallada de la estrategia.
        
        Returns:
            str: Descripción de la estrategia y sus efectos
        """
        pass
    
    def obtener_costo_diario(self) -> float:
        """
        Retorna el costo diario estimado de la ración (opcional).
        
        Returns:
            float: Costo en pesos/día (puede ser sobrescrito)
        """
        return 0.0
    
    def es_adecuada_para(self, animal) -> bool:
        """
        Determina si esta estrategia es adecuada para el animal (opcional).
        
        Args:
            animal: Animal a evaluar
            
        Returns:
            bool: True si la estrategia es adecuada
        """
        return True
    
    def __str__(self):
        """Representación en string de la estrategia"""
        return self.obtener_nombre()
    
    def __repr__(self):
        """Representación para debugging"""
        return f"{self.__class__.__name__}()"

# ==============================================================================
# ARCHIVO 11/26: racion_intensiva.py
# Directorio: estrategias
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./estrategias/racion_intensiva.py
# ==============================================================================

"""
Estrategia de Ración Intensiva

Estrategia de alimentación de alto rendimiento para engorde acelerado.
"""

from estrategias.estrategia_racion import EstrategiaRacion

class RacionIntensiva(EstrategiaRacion):
    """
    Estrategia de alimentación intensiva.
    
    Aplicación:
    - Animales en fase de engorde acelerado
    - Preparación para faena en corto plazo
    - Máximo aprovechamiento del feedlot
    
    Incremento: +2.0 kg por ciclo de alimentación
    """
    
    def __init__(self):
        """Inicializa la estrategia intensiva"""
        self.incremento_base = 2.0
        self.costo_diario = 280.0  # Pesos argentinos (mayor costo)
    
    def aplicar_racion(self, animal) -> float:
        """
        Aplica ración intensiva al animal.
        
        Args:
            animal: Animal a alimentar
            
        Returns:
            float: Incremento de peso (2.0 kg)
        """
        incremento = self.incremento_base
        animal.actualizar_peso(incremento)
        animal.racion_actual = "Intensiva"
        return incremento
    
    def obtener_nombre(self) -> str:
        """Retorna el nombre de la estrategia"""
        return "Ración Intensiva"
    
    def obtener_descripcion(self) -> str:
        """Retorna descripción detallada"""
        return (f"Alimentación de alto rendimiento para engorde acelerado. "
                f"Incremento: +{self.incremento_base} kg/día. "
                f"Costo: ${self.costo_diario}/día. "
                f"Ideal para animales jóvenes en crecimiento.")
    
    def obtener_costo_diario(self) -> float:
        """Retorna el costo diario de la ración"""
        return self.costo_diario
    
    def es_adecuada_para(self, animal) -> bool:
        """
        Determina si es adecuada para el animal.
        
        Args:
            animal: Animal a evaluar
            
        Returns:
            bool: True si el animal está sano y tiene bajo/medio peso
        """
        # Adecuada para animales saludables con peso menor a 350 kg
        # (Terneros y Novillos en crecimiento)
        return not animal.esta_enfermo() and animal.peso < 350
    
    def calcular_rendimiento(self, animal) -> dict:
        """
        Calcula métricas de rendimiento para esta estrategia.
        
        Args:
            animal: Animal a analizar
            
        Returns:
            dict: Métricas de rendimiento
        """
        dias_estimados = (400 - animal.peso) / self.incremento_base
        costo_total = dias_estimados * self.costo_diario
        
        return {
            "dias_hasta_objetivo": dias_estimados,
            "costo_total_estimado": costo_total,
            "peso_objetivo": 400,
            "ganancia_diaria": self.incremento_base
        }
    
    def __str__(self):
        return f"Ración Intensiva (+{self.incremento_base} kg/día) "

# ==============================================================================
# ARCHIVO 12/26: racion_mantenimiento.py
# Directorio: estrategias
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./estrategias/racion_mantenimiento.py
# ==============================================================================

"""
Estrategia de Ración de Mantenimiento

Estrategia de alimentación mínima para animales enfermos o en recuperación.
"""

from estrategias.estrategia_racion import EstrategiaRacion

class RacionMantenimiento(EstrategiaRacion):
    """
    Estrategia de alimentación de mantenimiento.
    
    Aplicación:
    - Animales enfermos en recuperación
    - Animales con problemas de salud
    - Período de adaptación al feedlot
    - Situaciones de estrés
    
    Incremento: +0.3 kg por ciclo de alimentación
    """
    
    def __init__(self):
        """Inicializa la estrategia de mantenimiento"""
        self.incremento_base = 0.3
        self.costo_diario = 100.0  # Pesos argentinos (menor costo)
    
    def aplicar_racion(self, animal) -> float:
        """
        Aplica ración de mantenimiento al animal.
        
        Args:
            animal: Animal a alimentar
            
        Returns:
            float: Incremento de peso (0.3 kg)
        """
        incremento = self.incremento_base
        animal.actualizar_peso(incremento)
        animal.racion_actual = "Mantenimiento"
        return incremento
    
    def obtener_nombre(self) -> str:
        """Retorna el nombre de la estrategia"""
        return "Ración de Mantenimiento"
    
    def obtener_descripcion(self) -> str:
        """Retorna descripción detallada"""
        return (f"Alimentación mínima para recuperación y mantenimiento. "
                f"Incremento: +{self.incremento_base} kg/día. "
                f"Costo: ${self.costo_diario}/día. "
                f"Ideal para animales enfermos o en período de adaptación.")
    
    def obtener_costo_diario(self) -> float:
        """Retorna el costo diario de la ración"""
        return self.costo_diario
    
    def es_adecuada_para(self, animal) -> bool:
        """
        Determina si es adecuada para el animal.
        
        Args:
            animal: Animal a evaluar
            
        Returns:
            bool: True si el animal está enfermo o necesita cuidados
        """
        # Adecuada para animales enfermos o con fiebre
        return animal.esta_enfermo() or animal.temperatura >= 39.5
    
    def obtener_recomendaciones(self, animal) -> list:
        """
        Genera recomendaciones específicas para el animal.
        
        Args:
            animal: Animal a evaluar
            
        Returns:
            list: Lista de recomendaciones
        """
        recomendaciones = [
            "Mantener observación veterinaria constante",
            "Proporcionar agua fresca y abundante",
            "Aislar de animales saludables si es necesario",
            "Monitorear temperatura dos veces al día"
        ]
        
        if animal.temperatura >= 39.5:
            recomendaciones.append(" Administrar antipirético bajo supervisión")
            recomendaciones.append(" Control de temperatura cada 4 horas")
        
        if animal.temperatura < 37.0:
            recomendaciones.append(" Proporcionar abrigo y ambiente cálido")
            recomendaciones.append(" Aumentar calorías gradualmente")
        
        return recomendaciones
    
    def tiempo_recuperacion_estimado(self, animal) -> int:
        """
        Estima el tiempo de recuperación del animal.
        
        Args:
            animal: Animal a evaluar
            
        Returns:
            int: Días estimados de recuperación
        """
        if not animal.esta_enfermo():
            return 0
        
        # Estimación basada en la temperatura
        if animal.temperatura >= 40.0:
            return 7  # Fiebre alta: 1 semana
        elif animal.temperatura >= 39.5:
            return 3  # Fiebre moderada: 3 días
        elif animal.temperatura < 37.0:
            return 5  # Hipotermia: 5 días
        else:
            return 2  # Recuperación general
    
    def __str__(self):
        return f"Ración de Mantenimiento (+{self.incremento_base} kg/día) "

# ==============================================================================
# ARCHIVO 13/26: racion_normal.py
# Directorio: estrategias
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./estrategias/racion_normal.py
# ==============================================================================

"""
Estrategia de Ración Normal

Estrategia de alimentación estándar para animales en condiciones normales.
"""

from estrategias.estrategia_racion import EstrategiaRacion

class RacionNormal(EstrategiaRacion):
    """
    Estrategia de alimentación normal.
    
    Aplicación:
    - Animales en condiciones estándar
    - Engorde progresivo sin prisa
    - Costo-beneficio equilibrado
    
    Incremento: +1.0 kg por ciclo de alimentación
    """
    
    def __init__(self):
        """Inicializa la estrategia normal"""
        self.incremento_base = 1.0
        self.costo_diario = 150.0  # Pesos argentinos
    
    def aplicar_racion(self, animal) -> float:
        """
        Aplica ración normal al animal.
        
        Args:
            animal: Animal a alimentar
            
        Returns:
            float: Incremento de peso (1.0 kg)
        """
        incremento = self.incremento_base
        animal.actualizar_peso(incremento)
        animal.racion_actual = "Normal"
        return incremento
    
    def obtener_nombre(self) -> str:
        """Retorna el nombre de la estrategia"""
        return "Ración Normal"
    
    def obtener_descripcion(self) -> str:
        """Retorna descripción detallada"""
        return (f"Alimentación estándar para engorde progresivo. "
                f"Incremento: +{self.incremento_base} kg/día. "
                f"Costo: ${self.costo_diario}/día")
    
    def obtener_costo_diario(self) -> float:
        """Retorna el costo diario de la ración"""
        return self.costo_diario
    
    def es_adecuada_para(self, animal) -> bool:
        """
        Determina si es adecuada para el animal.
        
        Args:
            animal: Animal a evaluar
            
        Returns:
            bool: True si el animal está sano y en peso medio
        """
        # Adecuada para animales saludables en cualquier peso
        return not animal.esta_enfermo()
    
    def __str__(self):
        return f"Ración Normal (+{self.incremento_base} kg/día)"


################################################################################
# DIRECTORIO: excepciones
################################################################################

# ==============================================================================
# ARCHIVO 14/26: __init__.py
# Directorio: excepciones
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./excepciones/__init__.py
# ==============================================================================

"""
Módulo de excepciones personalizadas
"""

from .feedlot_exceptions import (
    FeedlotException,
    AnimalNoEncontradoException,
    CorralNoEncontradoException,
    CorralLlenoException,
    PersistenciaException,
    EstrategiaInvalidaException,
    SensorException
)

__all__ = [
    'FeedlotException',
    'AnimalNoEncontradoException',
    'CorralNoEncontradoException',
    'CorralLlenoException',
    'PersistenciaException',
    'EstrategiaInvalidaException',
    'SensorException'
]

# ==============================================================================
# ARCHIVO 15/26: feedlot_exceptions.py
# Directorio: excepciones
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./excepciones/feedlot_exceptions.py
# ==============================================================================

"""
Excepciones personalizadas del sistema de feedlot
"""

class FeedlotException(Exception):
    """Excepción base del sistema de feedlot"""
    pass


class AnimalNoEncontradoException(FeedlotException):
    """Se lanza cuando un animal no existe en el sistema"""
    pass


class CorralNoEncontradoException(FeedlotException):
    """Se lanza cuando un corral no existe en el sistema"""
    pass


class CorralLlenoException(FeedlotException):
    """Se lanza cuando un corral está en capacidad máxima"""
    pass


class PersistenciaException(FeedlotException):
    """Se lanza cuando hay error al guardar/cargar datos"""
    pass


class EstrategiaInvalidaException(FeedlotException):
    """Se lanza cuando una estrategia no es válida para el animal"""
    pass


class SensorException(FeedlotException):
    """Se lanza cuando hay error en los sensores"""
    pass


################################################################################
# DIRECTORIO: patrones
################################################################################

# ==============================================================================
# ARCHIVO 16/26: __init__.py
# Directorio: patrones
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./patrones/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 17/26: factory.py
# Directorio: patrones
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./patrones/factory.py
# ==============================================================================

"""
Patrón Factory - Creación de objetos

"""

from entidades.animal import Animal
from entidades.sensor import SensorPeso, SensorTemperatura
from typing import Tuple, List
import random
from excepciones.feedlot_exceptions import FeedlotException

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
            raise FeedlotException(f"Tipo de animal no válido: '{tipo}'. Tipos válidos: {tipos_validos}")
        
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

# ==============================================================================
# ARCHIVO 18/26: observer.py
# Directorio: patrones
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./patrones/observer.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 19/26: salud_observer.py
# Directorio: patrones
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./patrones/salud_observer.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 20/26: singleton.py
# Directorio: patrones
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./patrones/singleton.py
# ==============================================================================

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


################################################################################
# DIRECTORIO: servicios
################################################################################

# ==============================================================================
# ARCHIVO 21/26: __init__.py
# Directorio: servicios
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./servicios/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 22/26: feedlot_service.py
# Directorio: servicios
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./servicios/feedlot_service.py
# ==============================================================================

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
from excepciones.feedlot_exceptions import (
    AnimalNoEncontradoException,
    CorralLlenoException
)

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
    
        if animal.id in self.animales:
           raise AnimalNoEncontradoException(f"Animal #{animal.id} ya existe en el sistema")
    
        self.animales[animal.id] = animal
    
        if numero_corral not in self.corrales:
           self.corrales[numero_corral] = Corral(numero_corral)
  
        if self.corrales[numero_corral].agregar_animal(animal):
           print(f"✓ {animal} agregado al {self.corrales[numero_corral]}")
           return True
        else:
            raise CorralLlenoException(f"{self.corrales[numero_corral]} está lleno")
    
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
    

# ==============================================================================
# ARCHIVO 23/26: log_service.py
# Directorio: servicios
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./servicios/log_service.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 24/26: persistencia_service.py
# Directorio: servicios
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./servicios/persistencia_service.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 25/26: racion_service.py
# Directorio: servicios
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./servicios/racion_service.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 26/26: reporte_service.py
# Directorio: servicios
# Ruta completa: /home/guadalupe/Documentos/DiseñoSistemas/tp2/dise-osistemas-estancia-cf/./servicios/reporte_service.py
# ==============================================================================

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


################################################################################
# FIN DEL INTEGRADOR FINAL
# Total de archivos: 26
# Generado: 2025-11-05 20:04:58
################################################################################
