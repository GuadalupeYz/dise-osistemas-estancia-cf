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