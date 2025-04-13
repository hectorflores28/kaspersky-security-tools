#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de Monitoreo de Servicios
Este script monitorea servicios en servidores Windows,
detectando cambios, anomalías y comportamientos sospechosos.
"""

import os
import sys
import json
import logging
import subprocess
import time
import psutil
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
import concurrent.futures
import argparse
import win32service
import win32serviceutil
import win32event
import servicemanager

class ServiceMonitor:
    def __init__(self, server_name: str, interval: int = 60):
        """
        Inicializa el monitor de servicios
        
        Args:
            server_name (str): Nombre o IP del servidor a monitorear
            interval (int): Intervalo de monitoreo en segundos
        """
        self.server_name = server_name
        self.interval = interval
        self.baseline = {}
        self.results = {
            'informacion_basica': {},
            'servicios': {},
            'alertas': [],
            'estadisticas': {},
            'timestamp': None
        }
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def obtener_estado_servicios(self) -> Dict[str, Any]:
        """
        Obtiene el estado actual de los servicios
        
        Returns:
            Dict[str, Any]: Estado de los servicios
        """
        try:
            servicios = {}
            output = subprocess.check_output(['sc', 'query'], text=True)
            
            for line in output.split('\n'):
                if 'SERVICE_NAME' in line:
                    service_name = line.split(':')[1].strip()
                    try:
                        # Obtener información detallada del servicio
                        service_info = subprocess.check_output(
                            ['sc', 'qc', service_name], 
                            text=True
                        )
                        
                        # Extraer estado y configuración
                        estado = {
                            'nombre': service_name,
                            'estado': None,
                            'tipo_inicio': None,
                            'cuenta': None,
                            'pid': None,
                            'consumo_recursos': None
                        }
                        
                        for info_line in service_info.split('\n'):
                            if 'STATE' in info_line:
                                estado['estado'] = info_line.split(':')[1].strip()
                            elif 'START_TYPE' in info_line:
                                estado['tipo_inicio'] = info_line.split(':')[1].strip()
                            elif 'SERVICE_START_NAME' in info_line:
                                estado['cuenta'] = info_line.split(':')[1].strip()
                                
                        # Obtener PID y consumo de recursos
                        try:
                            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                                if proc.info['name'] == service_name:
                                    estado['pid'] = proc.info['pid']
                                    estado['consumo_recursos'] = {
                                        'cpu': proc.info['cpu_percent'],
                                        'memoria': proc.info['memory_percent']
                                    }
                                    break
                        except:
                            pass
                            
                        servicios[service_name] = estado
                    except:
                        logging.warning(f"No se pudo obtener información del servicio {service_name}")
                        
            return servicios
        except Exception as e:
            logging.error(f"Error al obtener estado de servicios: {str(e)}")
            return {}
            
    def establecer_baseline(self):
        """
        Establece la línea base de servicios
        """
        try:
            self.baseline = self.obtener_estado_servicios()
            logging.info("Línea base de servicios establecida")
        except Exception as e:
            logging.error(f"Error al establecer línea base: {str(e)}")
            
    def detectar_cambios(self) -> List[Dict[str, Any]]:
        """
        Detecta cambios en los servicios comparando con la línea base
        
        Returns:
            List[Dict[str, Any]]: Lista de cambios detectados
        """
        try:
            cambios = []
            estado_actual = self.obtener_estado_servicios()
            
            # Verificar servicios nuevos o eliminados
            servicios_baseline = set(self.baseline.keys())
            servicios_actuales = set(estado_actual.keys())
            
            for servicio in servicios_actuales - servicios_baseline:
                cambios.append({
                    'tipo': 'Servicio Nuevo',
                    'servicio': servicio,
                    'detalles': estado_actual[servicio]
                })
                
            for servicio in servicios_baseline - servicios_actuales:
                cambios.append({
                    'tipo': 'Servicio Eliminado',
                    'servicio': servicio,
                    'detalles': self.baseline[servicio]
                })
                
            # Verificar cambios en servicios existentes
            for servicio in servicios_baseline & servicios_actuales:
                if self.baseline[servicio] != estado_actual[servicio]:
                    cambios.append({
                        'tipo': 'Cambio en Servicio',
                        'servicio': servicio,
                        'estado_anterior': self.baseline[servicio],
                        'estado_actual': estado_actual[servicio]
                    })
                    
            return cambios
        except Exception as e:
            logging.error(f"Error al detectar cambios: {str(e)}")
            return []
            
    def analizar_anomalias(self) -> List[Dict[str, Any]]:
        """
        Analiza anomalías en los servicios
        
        Returns:
            List[Dict[str, Any]]: Lista de anomalías detectadas
        """
        try:
            anomalias = []
            estado_actual = self.obtener_estado_servicios()
            
            for servicio, info in estado_actual.items():
                # Verificar consumo excesivo de recursos
                if info.get('consumo_recursos'):
                    if info['consumo_recursos']['cpu'] > 80:
                        anomalias.append({
                            'tipo': 'Alto Consumo de CPU',
                            'servicio': servicio,
                            'valor': info['consumo_recursos']['cpu'],
                            'umbral': 80
                        })
                    if info['consumo_recursos']['memoria'] > 80:
                        anomalias.append({
                            'tipo': 'Alto Consumo de Memoria',
                            'servicio': servicio,
                            'valor': info['consumo_recursos']['memoria'],
                            'umbral': 80
                        })
                        
                # Verificar servicios con cuentas privilegiadas
                if info['cuenta'] in ['LocalSystem', 'NT AUTHORITY\\SYSTEM']:
                    anomalias.append({
                        'tipo': 'Servicio Privilegiado',
                        'servicio': servicio,
                        'cuenta': info['cuenta']
                    })
                    
            return anomalias
        except Exception as e:
            logging.error(f"Error al analizar anomalías: {str(e)}")
            return []
            
    def monitorear(self):
        """
        Ejecuta el ciclo de monitoreo
        """
        try:
            while True:
                # Actualizar timestamp
                self.results['timestamp'] = datetime.now().isoformat()
                
                # Obtener estado actual
                self.results['servicios'] = self.obtener_estado_servicios()
                
                # Detectar cambios
                cambios = self.detectar_cambios()
                if cambios:
                    self.results['alertas'].extend([{
                        'tipo': 'Cambio',
                        'timestamp': self.results['timestamp'],
                        'detalles': cambio
                    } for cambio in cambios])
                    
                # Analizar anomalías
                anomalias = self.analizar_anomalias()
                if anomalias:
                    self.results['alertas'].extend([{
                        'tipo': 'Anomalía',
                        'timestamp': self.results['timestamp'],
                        'detalles': anomalia
                    } for anomalia in anomalias])
                    
                # Calcular estadísticas
                self.results['estadisticas'] = {
                    'total_servicios': len(self.results['servicios']),
                    'servicios_activos': sum(1 for s in self.results['servicios'].values() 
                                          if s['estado'] == 'RUNNING'),
                    'alertas_activas': len(self.results['alertas']),
                    'cambios_detectados': len(cambios),
                    'anomalias_detectadas': len(anomalias)
                }
                
                # Generar reporte
                self.generar_reporte('reporte_monitoreo')
                
                # Esperar intervalo
                time.sleep(self.interval)
                
        except KeyboardInterrupt:
            logging.info("Monitoreo detenido por el usuario")
        except Exception as e:
            logging.error(f"Error en el ciclo de monitoreo: {str(e)}")
            
    def generar_reporte(self, output_file: str):
        """
        Genera un reporte con los resultados del monitoreo
        
        Args:
            output_file (str): Ruta base para los archivos de salida
        """
        try:
            # Agregar metadatos al reporte
            reporte = {
                'fecha_analisis': self.results['timestamp'],
                'servidor': self.server_name,
                'resultados': self.results
            }
            
            # Guardar reporte en JSON
            with open(output_file + '.json', 'w') as f:
                json.dump(reporte, f, indent=4)
                
            # Guardar reporte en CSV
            df = pd.DataFrame([{
                'servidor': reporte['servidor'],
                'fecha': reporte['fecha_analisis'],
                'total_servicios': reporte['resultados']['estadisticas']['total_servicios'],
                'servicios_activos': reporte['resultados']['estadisticas']['servicios_activos'],
                'alertas_activas': reporte['resultados']['estadisticas']['alertas_activas'],
                'cambios_detectados': reporte['resultados']['estadisticas']['cambios_detectados'],
                'anomalias_detectadas': reporte['resultados']['estadisticas']['anomalias_detectadas']
            }])
            df.to_csv(output_file + '.csv', index=False)
            
            logging.info(f"Reporte generado en {output_file}.json y {output_file}.csv")
        except Exception as e:
            logging.error(f"Error al generar reporte: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Monitor de Servicios')
    parser.add_argument('server', help='Nombre o IP del servidor a monitorear')
    parser.add_argument('--interval', type=int, default=60,
                       help='Intervalo de monitoreo en segundos')
    
    args = parser.parse_args()
    
    monitor = ServiceMonitor(args.server, args.interval)
    monitor.establecer_baseline()
    monitor.monitorear()

if __name__ == "__main__":
    main() 