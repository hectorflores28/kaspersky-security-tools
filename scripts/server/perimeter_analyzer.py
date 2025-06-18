#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analizador de Perímetro de Red
Este script realiza un análisis del perímetro de red utilizando Nmap y Shodan.
"""

import os
import sys
import logging
import json
import nmap
import shodan
from datetime import datetime

class PerimeterAnalyzer:
    def __init__(self, shodan_api_key=None):
        self.logger = self._setup_logging()
        self.nm = nmap.PortScanner()
        self.shodan_api = shodan.Shodan(shodan_api_key) if shodan_api_key else None

    def _setup_logging(self):
        """Configura el sistema de logging."""
        log_dir = os.path.join(os.path.dirname(__file__), '../../logs')
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, f'perimeter_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def scan_with_nmap(self, target, ports=None, arguments='-sV -sS -T4'):
        """Realiza un escaneo con Nmap."""
        try:
            self.logger.info(f"Iniciando escaneo Nmap de {target}")
            self.nm.scan(target, ports, arguments)
            return self.nm.analyse_nmap_xml_scan()
        except Exception as e:
            self.logger.error(f"Error en escaneo Nmap: {str(e)}")
            return None

    def search_with_shodan(self, query):
        """Realiza búsquedas en Shodan."""
        if not self.shodan_api:
            self.logger.warning("API key de Shodan no configurada")
            return None

        try:
            self.logger.info(f"Buscando en Shodan: {query}")
            results = self.shodan_api.search(query)
            return results
        except Exception as e:
            self.logger.error(f"Error en búsqueda Shodan: {str(e)}")
            return None

    def analyze_vulnerabilities(self, scan_results):
        """Analiza vulnerabilidades en los resultados del escaneo."""
        vulnerabilities = []
        if not scan_results:
            return vulnerabilities

        for host in scan_results.get('scan', {}).values():
            for port in host.get('tcp', {}).values():
                if port.get('state') == 'open':
                    vuln_info = {
                        'host': host.get('addresses', {}).get('ipv4'),
                        'port': port.get('portid'),
                        'service': port.get('name'),
                        'version': port.get('version'),
                        'risk_level': self._assess_risk(port)
                    }
                    vulnerabilities.append(vuln_info)

        return vulnerabilities

    def _assess_risk(self, port_info):
        """Evalúa el nivel de riesgo de un puerto."""
        risk_level = 'LOW'
        service = port_info.get('name', '').lower()
        version = port_info.get('version', '').lower()

        # Servicios de alto riesgo
        high_risk_services = ['ftp', 'telnet', 'rsh', 'rlogin', 'rexec']
        if service in high_risk_services:
            risk_level = 'HIGH'

        # Versiones antiguas o vulnerables
        if 'old' in version or 'deprecated' in version:
            risk_level = 'HIGH'

        return risk_level

    def export_results(self, results, filename=None):
        """Exporta los resultados a un archivo JSON."""
        if not filename:
            filename = f'perimeter_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=4)
            self.logger.info(f"Resultados exportados a {filename}")
        except Exception as e:
            self.logger.error(f"Error al exportar resultados: {str(e)}")

def main():
    # Ejemplo de uso
    analyzer = PerimeterAnalyzer()
    
    # Escaneo de red
    target = "192.168.1.0/24"  # Ejemplo de red
    scan_results = analyzer.scan_with_nmap(target)
    
    # Análisis de vulnerabilidades
    vulnerabilities = analyzer.analyze_vulnerabilities(scan_results)
    
    # Exportar resultados
    results = {
        'scan_results': scan_results,
        'vulnerabilities': vulnerabilities,
        'timestamp': datetime.now().isoformat()
    }
    analyzer.export_results(results)

if __name__ == "__main__":
    main() 