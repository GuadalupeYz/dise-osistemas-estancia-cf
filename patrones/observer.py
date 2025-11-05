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