#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analizador de Logs de Seguridad
Este script analiza logs de seguridad en busca de patrones sospechosos
y genera reportes de eventos relevantes.
"""

import re
import json
import logging
from datetime import datetime
import argparse
from collections import defaultdict

class SecurityLogAnalyzer:
    def __init__(self, log_file):
        """
        Inicializa el analizador de logs
        
        Args:
            log_file (str): Ruta al archivo de log
        """
        self.log_file = log_file
        self.patterns = {
            'intentos_fallidos': r'Failed password',
            'acceso_exitoso': r'Accepted password',
            'escalada_privilegios': r'sudo:.*COMMAND=',
            'puertos_escaneados': r'Port scan detected',
            'ataques_brute_force': r'Too many authentication failures'
        }
        self.results = defaultdict(list)
        
    def analyze_line(self, line):
        """
        Analiza una línea de log en busca de patrones
        
        Args:
            line (str): Línea de log a analizar
        """
        for type, pattern in self.patterns.items():
            if re.search(pattern, line, re.IGNORECASE):
                self.results[type].append({
                    'timestamp': datetime.now().isoformat(),
                    'linea': line.strip(),
                    'tipo': type
                })
                
    def analyze_file(self):
        """Analiza el archivo de log completo"""
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    self.analyze_line(line)
        except Exception as e:
            logging.error(f"Error al analizar archivo: {str(e)}")
            
    def generate_report(self, output_file):
        """
        Genera un reporte con los resultados del análisis
        
        Args:
            output_file (str): Ruta al archivo de salida
        """
        report = {
            'fecha_analisis': datetime.now().isoformat(),
            'archivo_analizado': self.log_file,
            'resultados': dict(self.results)
        }
        
        try:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=4)
            logging.info(f"Reporte generado en {output_file}")
        except Exception as e:
            logging.error(f"Error al generar reporte: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Analizador de Logs de Seguridad')
    parser.add_argument('log_file', help='Ruta al archivo de log')
    parser.add_argument('--output', default='reporte_analisis.json', 
                       help='Ruta al archivo de salida')
    
    args = parser.parse_args()
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    analyzer = SecurityLogAnalyzer(args.log_file)
    analyzer.analyze_file()
    analyzer.generate_report(args.output)

if __name__ == "__main__":
    main() 