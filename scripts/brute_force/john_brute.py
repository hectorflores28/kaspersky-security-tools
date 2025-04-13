#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de Fuerza Bruta con John the Ripper
Este script automatiza el uso de John the Ripper para realizar ataques de fuerza bruta
en archivos de hashes o contraseñas.
"""

import os
import sys
import subprocess
import logging
import argparse
from typing import List, Optional
from datetime import datetime

class JohnBrute:
    def __init__(self, hash_file: str, wordlist: Optional[str] = None):
        """
        Inicializa el ataque de fuerza bruta
        
        Args:
            hash_file (str): Ruta al archivo de hashes
            wordlist (str, optional): Ruta al archivo de wordlist
        """
        self.hash_file = hash_file
        self.wordlist = wordlist
        self.results_file = f"john_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def identificar_formato(self) -> str:
        """
        Identifica el formato de los hashes en el archivo
        
        Returns:
            str: Formato identificado
        """
        try:
            result = subprocess.run(
                ['john', '--format=auto', '--list=formats', self.hash_file],
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except Exception as e:
            logging.error(f"Error al identificar formato: {str(e)}")
            return "unknown"
            
    def ejecutar_ataque(self, formato: str) -> bool:
        """
        Ejecuta el ataque de fuerza bruta
        
        Args:
            formato (str): Formato de los hashes
            
        Returns:
            bool: True si el ataque fue exitoso
        """
        try:
            cmd = ['john', f'--format={formato}', self.hash_file]
            
            if self.wordlist:
                cmd.extend(['--wordlist', self.wordlist])
            
            # Ejecutar John the Ripper
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
            subprocess.run(['john', '--show', self.hash_file, '>', self.results_file], shell=True)
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
    parser = argparse.ArgumentParser(description='Script de Fuerza Bruta con John the Ripper')
    parser.add_argument('hash_file', help='Archivo con los hashes a crackear')
    parser.add_argument('--wordlist', help='Archivo de wordlist a utilizar')
    
    args = parser.parse_args()
    
    if not os.path.isfile(args.hash_file):
        logging.error(f"El archivo {args.hash_file} no existe")
        sys.exit(1)
        
    if args.wordlist and not os.path.isfile(args.wordlist):
        logging.error(f"El archivo de wordlist {args.wordlist} no existe")
        sys.exit(1)
    
    brute = JohnBrute(args.hash_file, args.wordlist)
    
    # Identificar formato
    formato = brute.identificar_formato()
    logging.info(f"Formato identificado: {formato}")
    
    # Ejecutar ataque
    if brute.ejecutar_ataque(formato):
        brute.mostrar_resultados()
    else:
        logging.error("El ataque falló")

if __name__ == "__main__":
    main() 