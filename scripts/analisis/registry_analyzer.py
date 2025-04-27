#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analizador Forense del Registro de Windows
Este script analiza el registro de Windows en busca de indicadores
de compromiso y actividad maliciosa.
"""

import winreg
import logging
from datetime import datetime
import json
import argparse
import os
import sys
from pathlib import Path

class RegistryAnalyzer:
    def __init__(self, output_file='registry_analysis.json'):
        """
        Inicializa el analizador del registro
        
        Args:
            output_file (str): Archivo de salida para los resultados
        """
        self.output_file = output_file
        self.claves_sospechosas = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce",
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run",
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon",
            r"SYSTEM\CurrentControlSet\Services"
        ]
        self.patrones_sospechosos = [
            'cmd.exe',
            'powershell.exe',
            'wscript.exe',
            'cscript.exe',
            'mshta.exe',
            'regsvr32.exe',
            'rundll32.exe'
        ]
        self.resultados = {
            'fecha_analisis': datetime.now().isoformat(),
            'claves_analizadas': [],
            'alertas': []
        }
        
    def analizar_clave(self, clave, subclave):
        """
        Analiza una clave del registro en busca de patrones sospechosos
        
        Args:
            clave (str): Ruta de la clave del registro
            subclave (str): Nombre de la subclave
        """
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, clave) as key:
                try:
                    i = 0
                    while True:
                        try:
                            nombre, valor, tipo = winreg.EnumValue(key, i)
                            if any(patron in valor.lower() for patron in self.patrones_sospechosos):
                                alerta = {
                                    'tipo': 'valor_sospechoso',
                                    'clave': clave,
                                    'nombre': nombre,
                                    'valor': valor,
                                    'timestamp': datetime.now().isoformat()
                                }
                                self.resultados['alertas'].append(alerta)
                            i += 1
                        except WindowsError:
                            break
                except WindowsError:
                    pass
        except WindowsError:
            logging.error(f"No se pudo abrir la clave: {clave}")
    
    def analizar_servicios(self):
        """Analiza los servicios del sistema en busca de anomalías"""
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services") as key:
                i = 0
                while True:
                    try:
                        nombre_servicio = winreg.EnumKey(key, i)
                        try:
                            with winreg.OpenKey(key, nombre_servicio) as servicio:
                                try:
                                    imagen_path = winreg.QueryValueEx(servicio, "ImagePath")[0]
                                    if any(patron in imagen_path.lower() for patron in self.patrones_sospechosos):
                                        alerta = {
                                            'tipo': 'servicio_sospechoso',
                                            'nombre': nombre_servicio,
                                            'imagen_path': imagen_path,
                                            'timestamp': datetime.now().isoformat()
                                        }
                                        self.resultados['alertas'].append(alerta)
                                except WindowsError:
                                    pass
                        except WindowsError:
                            pass
                        i += 1
                    except WindowsError:
                        break
        except WindowsError:
            logging.error("No se pudo abrir la clave de servicios")
    
    def analizar_registro(self):
        """Analiza el registro completo"""
        for clave in self.claves_sospechosas:
            self.analizar_clave(clave, '')
        self.analizar_servicios()
    
    def generar_reporte(self):
        """Genera un reporte con los resultados del análisis"""
        try:
            with open(self.output_file, 'w') as f:
                json.dump(self.resultados, f, indent=4)
            logging.info(f"Reporte generado en {self.output_file}")
        except Exception as e:
            logging.error(f"Error al generar reporte: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Analizador Forense del Registro de Windows')
    parser.add_argument('--output', default='registry_analysis.json',
                       help='Archivo de salida para los resultados')
    
    args = parser.parse_args()
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    analyzer = RegistryAnalyzer(args.output)
    analyzer.analizar_registro()
    analyzer.generar_reporte()

if __name__ == "__main__":
    main() 