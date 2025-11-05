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