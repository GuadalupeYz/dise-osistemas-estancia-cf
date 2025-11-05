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