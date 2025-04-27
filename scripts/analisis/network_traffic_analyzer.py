#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analizador de Tráfico de Red
Este script analiza el tráfico de red en busca de patrones sospechosos
y actividad maliciosa.
"""

import scapy.all as scapy
import logging
from datetime import datetime
import json
import argparse
from collections import defaultdict
import time
import sys
from pathlib import Path

class NetworkTrafficAnalyzer:
    def __init__(self, interface=None, output_file='network_analysis.json'):
        """
        Inicializa el analizador de tráfico de red
        
        Args:
            interface (str): Interfaz de red a monitorear
            output_file (str): Archivo de salida para los resultados
        """
        self.interface = interface
        self.output_file = output_file
        self.patrones_sospechosos = {
            'dns': ['tunneling', 'exfiltracion'],
            'http': ['cmd.exe', 'powershell.exe', 'wget', 'curl'],
            'tcp': ['port_scanning', 'brute_force']
        }
        self.resultados = {
            'fecha_analisis': datetime.now().isoformat(),
            'paquetes_analizados': 0,
            'alertas': [],
            'estadisticas': defaultdict(int)
        }
        
    def analizar_paquete(self, paquete):
        """Analiza un paquete de red en busca de patrones sospechosos"""
        alerta = None
        
        # Analizar paquetes DNS
        if paquete.haslayer(scapy.DNS):
            dns = paquete[scapy.DNS]
            if dns.qd:
                query = dns.qd.qname.decode('utf-8', errors='ignore')
                for patron in self.patrones_sospechosos['dns']:
                    if patron in query.lower():
                        alerta = {
                            'tipo': 'dns_sospechoso',
                            'detalles': {
                                'query': query,
                                'patron': patron
                            }
                        }
                        break
        
        # Analizar paquetes HTTP
        elif paquete.haslayer(scapy.TCP) and paquete.haslayer(scapy.Raw):
            raw = paquete[scapy.Raw].load.decode('utf-8', errors='ignore')
            for patron in self.patrones_sospechosos['http']:
                if patron in raw.lower():
                    alerta = {
                        'tipo': 'http_sospechoso',
                        'detalles': {
                            'contenido': raw,
                            'patron': patron
                        }
                    }
                    break
        
        # Analizar patrones TCP sospechosos
        elif paquete.haslayer(scapy.TCP):
            tcp = paquete[scapy.TCP]
            # Detectar escaneo de puertos
            if tcp.flags == 'S' and not paquete.haslayer(scapy.IP):
                self.resultados['estadisticas']['port_scanning'] += 1
                if self.resultados['estadisticas']['port_scanning'] > 100:
                    alerta = {
                        'tipo': 'port_scanning',
                        'detalles': {
                            'puerto': tcp.dport,
                            'intentos': self.resultados['estadisticas']['port_scanning']
                        }
                    }
        
        if alerta:
            alerta['timestamp'] = datetime.now().isoformat()
            alerta['src_ip'] = paquete[scapy.IP].src if paquete.haslayer(scapy.IP) else 'N/A'
            alerta['dst_ip'] = paquete[scapy.IP].dst if paquete.haslayer(scapy.IP) else 'N/A'
            self.resultados['alertas'].append(alerta)
    
    def capturar_paquetes(self, count=0, timeout=30):
        """
        Captura y analiza paquetes de red
        
        Args:
            count (int): Número de paquetes a capturar (0 para infinito)
            timeout (int): Tiempo máximo de captura en segundos
        """
        try:
            logging.info(f"Iniciando captura en interfaz {self.interface}")
            scapy.sniff(
                iface=self.interface,
                prn=self.analizar_paquete,
                count=count,
                timeout=timeout
            )
        except Exception as e:
            logging.error(f"Error en la captura: {str(e)}")
    
    def generar_reporte(self):
        """Genera un reporte con los resultados del análisis"""
        try:
            with open(self.output_file, 'w') as f:
                json.dump(self.resultados, f, indent=4)
            logging.info(f"Reporte generado en {self.output_file}")
        except Exception as e:
            logging.error(f"Error al generar reporte: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Analizador de Tráfico de Red')
    parser.add_argument('--interface', help='Interfaz de red a monitorear')
    parser.add_argument('--output', default='network_analysis.json',
                       help='Archivo de salida para los resultados')
    parser.add_argument('--count', type=int, default=0,
                       help='Número de paquetes a capturar (0 para infinito)')
    parser.add_argument('--timeout', type=int, default=30,
                       help='Tiempo máximo de captura en segundos')
    
    args = parser.parse_args()
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    analyzer = NetworkTrafficAnalyzer(args.interface, args.output)
    analyzer.capturar_paquetes(args.count, args.timeout)
    analyzer.generar_reporte()

if __name__ == "__main__":
    main() 