#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analizador de Sistemas de Archivos
Este script analiza el sistema de archivos en busca de indicadores
de compromiso y actividad maliciosa.
"""

import os
import logging
from datetime import datetime
import json
import argparse
import hashlib
import stat
import time
from pathlib import Path
import magic

class FileSystemAnalyzer:
    def __init__(self, directorio, output_file='filesystem_analysis.json'):
        """
        Inicializa el analizador de sistema de archivos
        
        Args:
            directorio (str): Directorio a analizar
            output_file (str): Archivo de salida para los resultados
        """
        self.directorio = directorio
        self.output_file = output_file
        self.extensiones_sospechosas = [
            '.exe', '.dll', '.bat', '.cmd', '.ps1', '.vbs',
            '.js', '.jse', '.wsf', '.wsh', '.msi', '.scr'
        ]
        self.patrones_sospechosos = [
            'cmd.exe',
            'powershell.exe',
            'wscript.exe',
            'cscript.exe',
            'mshta.exe'
        ]
        self.resultados = {
            'fecha_analisis': datetime.now().isoformat(),
            'directorio': directorio,
            'archivos_analizados': [],
            'alertas': []
        }
        
    def calcular_hash(self, archivo):
        """Calcula el hash MD5 de un archivo"""
        try:
            with open(archivo, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            logging.error(f"Error al calcular hash de {archivo}: {str(e)}")
            return None
    
    def analizar_permisos(self, archivo):
        """Analiza los permisos de un archivo"""
        try:
            st = os.stat(archivo)
            permisos = {
                'usuario': st.st_uid,
                'grupo': st.st_gid,
                'modo': oct(st.st_mode)[-3:],
                'tamaño': st.st_size,
                'ultimo_acceso': datetime.fromtimestamp(st.st_atime).isoformat(),
                'ultima_modificacion': datetime.fromtimestamp(st.st_mtime).isoformat()
            }
            return permisos
        except Exception as e:
            logging.error(f"Error al analizar permisos de {archivo}: {str(e)}")
            return None
    
    def analizar_archivo(self, archivo):
        """Analiza un archivo en busca de indicadores sospechosos"""
        try:
            info = {
                'ruta': str(archivo),
                'nombre': archivo.name,
                'hash': self.calcular_hash(archivo),
                'permisos': self.analizar_permisos(archivo),
                'tipo': magic.from_file(str(archivo)),
                'sospechoso': False,
                'razones': []
            }
            
            # Verificar extensión sospechosa
            if archivo.suffix.lower() in self.extensiones_sospechosas:
                info['sospechoso'] = True
                info['razones'].append('Extensión sospechosa')
            
            # Verificar nombre sospechoso
            if any(patron in archivo.name.lower() for patron in self.patrones_sospechosos):
                info['sospechoso'] = True
                info['razones'].append('Nombre sospechoso')
            
            # Verificar permisos inusuales
            if info['permisos'] and info['permisos']['modo'] in ['777', '666']:
                info['sospechoso'] = True
                info['razones'].append('Permisos inusuales')
            
            # Verificar archivos ocultos
            if archivo.name.startswith('.'):
                info['sospechoso'] = True
                info['razones'].append('Archivo oculto')
            
            self.resultados['archivos_analizados'].append(info)
            
            if info['sospechoso']:
                alerta = {
                    'tipo': 'archivo_sospechoso',
                    'archivo': str(archivo),
                    'razones': info['razones'],
                    'timestamp': datetime.now().isoformat()
                }
                self.resultados['alertas'].append(alerta)
                
        except Exception as e:
            logging.error(f"Error al analizar archivo {archivo}: {str(e)}")
    
    def analizar_directorio(self):
        """Analiza todos los archivos en el directorio"""
        try:
            for root, _, files in os.walk(self.directorio):
                for file in files:
                    archivo = Path(root) / file
                    self.analizar_archivo(archivo)
        except Exception as e:
            logging.error(f"Error al analizar directorio: {str(e)}")
    
    def generar_reporte(self):
        """Genera un reporte con los resultados del análisis"""
        try:
            with open(self.output_file, 'w') as f:
                json.dump(self.resultados, f, indent=4)
            logging.info(f"Reporte generado en {self.output_file}")
        except Exception as e:
            logging.error(f"Error al generar reporte: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Analizador de Sistemas de Archivos')
    parser.add_argument('directorio', help='Directorio a analizar')
    parser.add_argument('--output', default='filesystem_analysis.json',
                       help='Archivo de salida para los resultados')
    
    args = parser.parse_args()
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    analyzer = FileSystemAnalyzer(args.directorio, args.output)
    analyzer.analizar_directorio()
    analyzer.generar_reporte()

if __name__ == "__main__":
    main() 