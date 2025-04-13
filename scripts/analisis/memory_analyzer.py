#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analizador de Memoria
Este script realiza un análisis básico de volcados de memoria
en busca de indicadores de compromiso.
"""

import volatility3
import argparse
import logging
from datetime import datetime
import json
import re
from volatility3.framework import interfaces, automagic, plugins
from volatility3.framework.configuration import requirements

class MemoryAnalyzer:
    def __init__(self, memory_file):
        """
        Inicializa el analizador de memoria
        
        Args:
            memory_file (str): Ruta al archivo de volcado de memoria
        """
        self.memory_file = memory_file
        self.results = {
            'fecha_analisis': datetime.now().isoformat(),
            'archivo': memory_file,
            'procesos': [],
            'conexiones': [],
            'archivos_mapeados': [],
            'indicadores': []
        }
        
    def analyze_processes(self):
        """Analiza los procesos en memoria"""
        try:
            # Configurar contexto de Volatility
            ctx = interfaces.context.Context()
            automagic.choose_automagic(automagic.available(ctx))
            
            # Cargar imagen de memoria
            layer = automagic.choose_automagic(automagic.available(ctx))
            layer.load(ctx, self.memory_file)
            
            # Obtener lista de procesos
            pslist = plugins.PsList()
            for process in pslist.run():
                self.results['procesos'].append({
                    'pid': process.pid,
                    'nombre': process.name,
                    'ruta': process.path,
                    'argumentos': process.command_line
                })
                
        except Exception as e:
            logging.error(f"Error al analizar procesos: {str(e)}")
            
    def analyze_connections(self):
        """Analiza las conexiones de red en memoria"""
        try:
            # Configurar contexto de Volatility
            ctx = interfaces.context.Context()
            automagic.choose_automagic(automagic.available(ctx))
            
            # Cargar imagen de memoria
            layer = automagic.choose_automagic(automagic.available(ctx))
            layer.load(ctx, self.memory_file)
            
            # Obtener conexiones de red
            netscan = plugins.Netscan()
            for connection in netscan.run():
                self.results['conexiones'].append({
                    'pid': connection.pid,
                    'protocolo': connection.protocol,
                    'ip_origen': connection.local_ip,
                    'puerto_origen': connection.local_port,
                    'ip_destino': connection.remote_ip,
                    'puerto_destino': connection.remote_port,
                    'estado': connection.state
                })
                
        except Exception as e:
            logging.error(f"Error al analizar conexiones: {str(e)}")
            
    def analyze_files(self):
        """Analiza los archivos mapeados en memoria"""
        try:
            # Configurar contexto de Volatility
            ctx = interfaces.context.Context()
            automagic.choose_automagic(automagic.available(ctx))
            
            # Cargar imagen de memoria
            layer = automagic.choose_automagic(automagic.available(ctx))
            layer.load(ctx, self.memory_file)
            
            # Obtener archivos mapeados
            handles = plugins.Handles()
            for handle in handles.run():
                if handle.type == 'File':
                    self.results['archivos_mapeados'].append({
                        'pid': handle.pid,
                        'nombre': handle.name,
                        'tipo': handle.type
                    })
                    
        except Exception as e:
            logging.error(f"Error al analizar archivos: {str(e)}")
            
    def search_indicators(self):
        """Busca indicadores de compromiso en memoria"""
        try:
            # Patrones de búsqueda
            patterns = [
                r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',
                r'[0-9a-fA-F]{32}',
                r'[0-9a-fA-F]{40}',
                r'[0-9a-fA-F]{64}'
            ]
            
            # Configurar contexto de Volatility
            ctx = interfaces.context.Context()
            automagic.choose_automagic(automagic.available(ctx))
            
            # Cargar imagen de memoria
            layer = automagic.choose_automagic(automagic.available(ctx))
            layer.load(ctx, self.memory_file)
            
            # Buscar patrones en memoria
            yarascan = plugins.YaraScan()
            for pattern in patterns:
                for match in yarascan.run(pattern=pattern):
                    self.results['indicadores'].append({
                        'tipo': 'Patrón',
                        'valor': match,
                        'offset': hex(match.offset)
                    })
                    
        except Exception as e:
            logging.error(f"Error al buscar indicadores: {str(e)}")
            
    def analyze(self):
        """Realiza el análisis completo de memoria"""
        self.analyze_processes()
        self.analyze_connections()
        self.analyze_files()
        self.search_indicators()
        
    def generate_report(self, output_file):
        """
        Genera un reporte con los resultados del análisis
        
        Args:
            output_file (str): Ruta al archivo de salida
        """
        try:
            with open(output_file, 'w') as f:
                json.dump(self.results, f, indent=4)
            logging.info(f"Reporte generado en {output_file}")
        except Exception as e:
            logging.error(f"Error al generar reporte: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Analizador de Memoria')
    parser.add_argument('memory_file', help='Ruta al archivo de volcado de memoria')
    parser.add_argument('--output', default='reporte_memoria.json', 
                       help='Ruta al archivo de salida')
    
    args = parser.parse_args()
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    analyzer = MemoryAnalyzer(args.memory_file)
    analyzer.analyze()
    analyzer.generate_report(args.output)

if __name__ == "__main__":
    main() 