#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de monitoreo de procesos
Este script monitorea los procesos en ejecución y genera alertas
basadas en patrones sospechosos.
"""

import psutil
import time
import logging
from datetime import datetime
import json
import os

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitor_procesos.log'),
        logging.StreamHandler()
    ]
)

class MonitorProcesos:
    def __init__(self, intervalo=5):
        """
        Inicializa el monitor de procesos
        
        Args:
            intervalo (int): Intervalo de monitoreo en segundos
        """
        self.intervalo = intervalo
        self.procesos_previos = set()
        self.patrones_sospechosos = [
            'cmd.exe',
            'powershell.exe',
            'wscript.exe',
            'cscript.exe',
            'mshta.exe'
        ]
        
    def obtener_procesos(self):
        """Obtiene la lista de procesos actuales"""
        return {p.pid: p.name() for p in psutil.process_iter(['pid', 'name'])}
    
    def analizar_procesos(self, procesos):
        """
        Analiza los procesos en busca de patrones sospechosos
        
        Args:
            procesos (dict): Diccionario de procesos {pid: nombre}
        """
        alertas = []
        for pid, nombre in procesos.items():
            if nombre.lower() in self.patrones_sospechosos:
                alertas.append({
                    'pid': pid,
                    'nombre': nombre,
                    'timestamp': datetime.now().isoformat(),
                    'tipo': 'proceso_sospechoso'
                })
        return alertas
    
    def monitorear(self):
        """Inicia el monitoreo continuo de procesos"""
        logging.info("Iniciando monitoreo de procesos...")
        
        while True:
            try:
                procesos_actuales = self.obtener_procesos()
                alertas = self.analizar_procesos(procesos_actuales)
                
                if alertas:
                    for alerta in alertas:
                        logging.warning(f"Alerta: {json.dumps(alerta)}")
                
                self.procesos_previos = set(procesos_actuales.keys())
                time.sleep(self.intervalo)
                
            except Exception as e:
                logging.error(f"Error en el monitoreo: {str(e)}")
                time.sleep(self.intervalo)

if __name__ == "__main__":
    monitor = MonitorProcesos()
    monitor.monitorear() 