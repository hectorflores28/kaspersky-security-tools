#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de Escaneo Rápido con Nmap
Este script realiza un escaneo rápido de puertos y servicios.
"""

from nmap_scan import NmapScanner
import argparse

def main():
    parser = argparse.ArgumentParser(description='Script de Escaneo Rápido con Nmap')
    parser.add_argument('target', help='IP o dominio a escanear')
    
    args = parser.parse_args()
    
    # Argumentos para escaneo rápido
    argumentos = '-sS -T4 -F --top-ports 100'
    
    scanner = NmapScanner(args.target)
    
    # Ejecutar escaneo
    if scanner.ejecutar_escaneo(argumentos):
        scanner.mostrar_resultados()
    else:
        print("El escaneo falló")

if __name__ == "__main__":
    main() 