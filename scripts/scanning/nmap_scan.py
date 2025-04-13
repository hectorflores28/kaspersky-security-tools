#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script Base para Escaneos con Nmap
Este script proporciona una interfaz base para diferentes tipos de escaneos con Nmap.
"""

import os
import sys
import subprocess
import logging
import argparse
from typing import List, Dict, Any
from datetime import datetime

class NmapScanner:
    def __init__(self, target: str):
        """
        Inicializa el escáner Nmap
        
        Args:
            target (str): IP o dominio a escanear
        """
        self.target = target
        self.results_file = f"nmap_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def ejecutar_escaneo(self, argumentos: str) -> bool:
        """
        Ejecuta un escaneo con Nmap
        
        Args:
            argumentos (str): Argumentos para el escaneo
            
        Returns:
            bool: True si el escaneo fue exitoso
        """
        try:
            cmd = ['nmap', *argumentos.split(), '-oX', self.results_file, self.target]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Monitorear salida
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    logging.info(output.strip())
                    
            return True
            
        except Exception as e:
            logging.error(f"Error durante el escaneo: {str(e)}")
            return False
            
    def mostrar_resultados(self):
        """Muestra los resultados del escaneo"""
        try:
            with open(self.results_file, 'r') as f:
                print("\nResultados del escaneo:")
                print("-" * 50)
                print(f.read())
        except Exception as e:
            logging.error(f"Error al mostrar resultados: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Script Base para Escaneos con Nmap')
    parser.add_argument('target', help='IP o dominio a escanear')
    parser.add_argument('--arguments', default='-sV -sS -T4', 
                       help='Argumentos para Nmap')
    
    args = parser.parse_args()
    
    scanner = NmapScanner(args.target)
    
    # Ejecutar escaneo
    if scanner.ejecutar_escaneo(args.arguments):
        scanner.mostrar_resultados()
    else:
        logging.error("El escaneo falló")

if __name__ == "__main__":
    main() 