#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Monitor de Servicios
Este script monitorea servicios críticos en servidores Windows y Linux.
"""

import os
import sys
import logging
import json
import psutil
import platform
import subprocess
from datetime import datetime

class ServiceMonitor:
    def __init__(self):
        self.logger = self._setup_logging()
        self.os_type = platform.system().lower()

    def _setup_logging(self):
        """Configura el sistema de logging."""
        log_dir = os.path.join(os.path.dirname(__file__), '../../logs')
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, f'service_monitor_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def get_services(self):
        """Obtiene la lista de servicios según el sistema operativo."""
        if self.os_type == 'windows':
            return self._get_windows_services()
        else:
            return self._get_linux_services()

    def _get_windows_services(self):
        """Obtiene servicios en Windows."""
        try:
            output = subprocess.check_output(['sc', 'query', 'type=', 'service', 'state=', 'all'], 
                                          universal_newlines=True)
            services = []
            current_service = {}
            
            for line in output.split('\n'):
                line = line.strip()
                if line.startswith('SERVICE_NAME:'):
                    if current_service:
                        services.append(current_service)
                    current_service = {'name': line.split(':', 1)[1].strip()}
                elif line.startswith('DISPLAY_NAME:'):
                    current_service['display_name'] = line.split(':', 1)[1].strip()
                elif line.startswith('STATE:'):
                    current_service['state'] = line.split(':', 1)[1].strip()
                elif line.startswith('START_TYPE:'):
                    current_service['start_type'] = line.split(':', 1)[1].strip()

            if current_service:
                services.append(current_service)

            return services
        except Exception as e:
            self.logger.error(f"Error al obtener servicios de Windows: {str(e)}")
            return []

    def _get_linux_services(self):
        """Obtiene servicios en Linux."""
        try:
            output = subprocess.check_output(['systemctl', 'list-units', '--type=service', '--all'],
                                          universal_newlines=True)
            services = []
            
            for line in output.split('\n'):
                if '.service' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        services.append({
                            'name': parts[0],
                            'load': parts[1],
                            'active': parts[2],
                            'sub': parts[3],
                            'description': ' '.join(parts[4:])
                        })

            return services
        except Exception as e:
            self.logger.error(f"Error al obtener servicios de Linux: {str(e)}")
            return []

    def check_service_health(self, service_name):
        """Verifica la salud de un servicio específico."""
        try:
            if self.os_type == 'windows':
                output = subprocess.check_output(['sc', 'query', service_name], 
                                              universal_newlines=True)
                return 'RUNNING' in output
            else:
                output = subprocess.check_output(['systemctl', 'is-active', service_name],
                                              universal_newlines=True)
                return output.strip() == 'active'
        except Exception as e:
            self.logger.error(f"Error al verificar salud del servicio {service_name}: {str(e)}")
            return False

    def get_service_metrics(self, service_name):
        """Obtiene métricas de un servicio."""
        metrics = {
            'cpu_percent': 0,
            'memory_percent': 0,
            'threads': 0,
            'connections': 0
        }

        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                if service_name.lower() in proc.info['name'].lower():
                    metrics['cpu_percent'] = proc.info['cpu_percent']
                    metrics['memory_percent'] = proc.info['memory_percent']
                    metrics['threads'] = proc.num_threads()
                    metrics['connections'] = len(proc.connections())
                    break
        except Exception as e:
            self.logger.error(f"Error al obtener métricas del servicio {service_name}: {str(e)}")

        return metrics

    def export_results(self, results, filename=None):
        """Exporta los resultados a un archivo JSON."""
        if not filename:
            filename = f'service_monitor_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=4)
            self.logger.info(f"Resultados exportados a {filename}")
        except Exception as e:
            self.logger.error(f"Error al exportar resultados: {str(e)}")

def main():
    # Ejemplo de uso
    monitor = ServiceMonitor()
    
    # Obtener lista de servicios
    services = monitor.get_services()
    
    # Verificar servicios críticos
    critical_services = ['mysql', 'apache2', 'nginx', 'postgresql']
    service_status = {}
    
    for service in critical_services:
        if monitor.check_service_health(service):
            service_status[service] = {
                'status': 'running',
                'metrics': monitor.get_service_metrics(service)
            }
        else:
            service_status[service] = {
                'status': 'stopped',
                'metrics': {}
            }
    
    # Exportar resultados
    results = {
        'services': services,
        'critical_services': service_status,
        'timestamp': datetime.now().isoformat()
    }
    monitor.export_results(results)

if __name__ == "__main__":
    main() 