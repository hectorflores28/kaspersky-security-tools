#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de Detección de Sistema Operativo con Nmap
Este script realiza un escaneo para identificar el sistema operativo del objetivo.
"""

from nmap_scan import NmapScanner
import argparse

def main():
    parser = argparse.ArgumentParser(description='Script de Detección de SO con Nmap')
    parser.add_argument('target', help='IP o dominio a escanear')
    
    args = parser.parse_args()
    
    # Argumentos para detección de SO
    argumentos = '-O -sV -T4'
    
    scanner = NmapScanner(args.target)
    
    # Ejecutar escaneo
    if scanner.ejecutar_escaneo(argumentos):
        scanner.mostrar_resultados()
    else:
        print("El escaneo falló")

if __name__ == "__main__":
    main() 