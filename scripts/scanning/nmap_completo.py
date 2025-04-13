#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de Escaneo Completo con Nmap
Este script realiza un escaneo exhaustivo de puertos, servicios y vulnerabilidades.
"""

from nmap_scan import NmapScanner
import argparse

def main():
    parser = argparse.ArgumentParser(description='Script de Escaneo Completo con Nmap')
    parser.add_argument('target', help='IP o dominio a escanear')
    
    args = parser.parse_args()
    
    # Argumentos para escaneo completo
    argumentos = '-sV -sS -sC -A -T4 -p- --script=vuln'
    
    scanner = NmapScanner(args.target)
    
    # Ejecutar escaneo
    if scanner.ejecutar_escaneo(argumentos):
        scanner.mostrar_resultados()
    else:
        print("El escaneo falló")

if __name__ == "__main__":
    main() 