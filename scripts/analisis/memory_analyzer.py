#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analizador de Memoria Forense

Este script proporciona herramientas para el análisis forense de memoria,
incluyendo análisis de procesos, DLLs cargadas y conexiones de red.
"""

import os
import sys
import psutil
import logging
from datetime import datetime
from typing import Dict, List, Optional
import json

class MemoryAnalyzer:
    def __init__(self):
        """Inicializa el analizador de memoria."""
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Configura el sistema de logging."""
        logger = logging.getLogger('memory_analyzer')
        logger.setLevel(logging.INFO)
        
        # Crear directorio de logs si no existe
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        # Configurar handler para archivo
        fh = logging.FileHandler(f'logs/memory_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        fh.setLevel(logging.INFO)
        
        # Configurar handler para consola
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formato del log
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger

    def analyze_processes(self) -> List[Dict]:
        """Analiza los procesos en ejecución."""
        self.logger.info("Iniciando análisis de procesos...")
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent', 'cpu_percent']):
            try:
                process_info = proc.info
                process_info['connections'] = self._get_process_connections(proc.pid)
                process_info['dlls'] = self._get_process_dlls(proc.pid)
                processes.append(process_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
                
        self.logger.info(f"Análisis de procesos completado. Procesos encontrados: {len(processes)}")
        return processes

    def _get_process_connections(self, pid: int) -> List[Dict]:
        """Obtiene las conexiones de red de un proceso."""
        try:
            connections = []
            for conn in psutil.Process(pid).connections():
                connections.append({
                    'local_address': conn.laddr,
                    'remote_address': conn.raddr if conn.raddr else None,
                    'status': conn.status,
                    'type': conn.type
                })
            return connections
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return []

    def _get_process_dlls(self, pid: int) -> List[str]:
        """Obtiene las DLLs cargadas por un proceso."""
        try:
            # En Windows, podemos usar wmic para obtener las DLLs
            if sys.platform == 'win32':
                import subprocess
                cmd = f'wmic process where processid={pid} list modules'
                output = subprocess.check_output(cmd, shell=True).decode()
                dlls = [line.split()[0] for line in output.split('\n')[1:] if line.strip()]
                return dlls
            return []
        except Exception as e:
            self.logger.error(f"Error al obtener DLLs del proceso {pid}: {str(e)}")
            return []

    def export_results(self, data: List[Dict], output_file: str) -> None:
        """Exporta los resultados del análisis a un archivo JSON."""
        try:
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=4)
            self.logger.info(f"Resultados exportados a {output_file}")
        except Exception as e:
            self.logger.error(f"Error al exportar resultados: {str(e)}")

def main():
    """Función principal del script."""
    analyzer = MemoryAnalyzer()
    
    # Analizar procesos
    processes = analyzer.analyze_processes()
    
    # Exportar resultados
    output_file = f'memory_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    analyzer.export_results(processes, output_file)

if __name__ == "__main__":
    main() 