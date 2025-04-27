#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de monitoreo de procesos
Este script monitorea los procesos en ejecución, DLLs cargadas,
handles y recursos, generando alertas basadas en patrones sospechosos.
"""

import psutil
import time
import logging
from datetime import datetime
import json
import os
import win32api
import win32process
import win32con
import win32security
import win32file
import ctypes
from ctypes import wintypes
import sys
from pathlib import Path

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
        self.dlls_sospechosas = [
            'kernel32.dll',
            'user32.dll',
            'ws2_32.dll',
            'advapi32.dll'
        ]
        
    def obtener_procesos(self):
        """Obtiene la lista de procesos actuales con información detallada"""
        procesos = {}
        for p in psutil.process_iter(['pid', 'name', 'exe', 'username', 'memory_info', 'cpu_percent']):
            try:
                procesos[p.info['pid']] = {
                    'nombre': p.info['name'],
                    'ruta': p.info['exe'],
                    'usuario': p.info['username'],
                    'memoria': p.info['memory_info'].rss,
                    'cpu': p.info['cpu_percent']
                }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return procesos
    
    def obtener_dlls_cargadas(self, pid):
        """Obtiene las DLLs cargadas por un proceso"""
        try:
            process = psutil.Process(pid)
            return process.memory_maps()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return []
    
    def analizar_handles(self, pid):
        """Analiza los handles abiertos por un proceso"""
        try:
            process = psutil.Process(pid)
            return process.num_handles()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return 0
    
    def detectar_proceso_inyectado(self, pid):
        """Detecta si un proceso tiene código inyectado"""
        try:
            process = psutil.Process(pid)
            memory_maps = process.memory_maps()
            
            # Verificar regiones de memoria con permisos inusuales
            for mmap in memory_maps:
                if 'EXECUTE' in mmap.perms and 'WRITE' in mmap.perms:
                    return True
                    
            # Verificar si el proceso tiene handles inusuales
            handles = self.analizar_handles(pid)
            if handles > 1000:  # Umbral arbitrario
                return True
                
            return False
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False
    
    def analizar_procesos(self, procesos):
        """
        Analiza los procesos en busca de patrones sospechosos
        
        Args:
            procesos (dict): Diccionario de procesos {pid: info}
        """
        alertas = []
        for pid, info in procesos.items():
            alerta = {
                'pid': pid,
                'nombre': info['nombre'],
                'timestamp': datetime.now().isoformat(),
                'tipo': [],
                'detalles': {}
            }
            
            # Verificar procesos sospechosos
            if info['nombre'].lower() in self.patrones_sospechosos:
                alerta['tipo'].append('proceso_sospechoso')
                alerta['detalles']['razon'] = 'Proceso en lista de sospechosos'
            
            # Verificar DLLs cargadas
            dlls = self.obtener_dlls_cargadas(pid)
            dlls_sospechosas = [dll for dll in dlls if any(s in dll.path.lower() for s in self.dlls_sospechosas)]
            if dlls_sospechosas:
                alerta['tipo'].append('dll_sospechosa')
                alerta['detalles']['dlls_sospechosas'] = [dll.path for dll in dlls_sospechosas]
            
            # Verificar inyección de código
            if self.detectar_proceso_inyectado(pid):
                alerta['tipo'].append('proceso_inyectado')
                alerta['detalles']['razon'] = 'Posible inyección de código detectada'
            
            # Verificar uso de recursos
            if info['memoria'] > 100 * 1024 * 1024:  # 100MB
                alerta['tipo'].append('uso_memoria_alto')
                alerta['detalles']['memoria'] = info['memoria']
            
            if info['cpu'] > 80:  # 80%
                alerta['tipo'].append('uso_cpu_alto')
                alerta['detalles']['cpu'] = info['cpu']
            
            if alerta['tipo']:
                alertas.append(alerta)
        
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