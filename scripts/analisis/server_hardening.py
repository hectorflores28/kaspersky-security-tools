#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de Hardening de Servidores
Este script automatiza el proceso de hardening de servidores Windows,
implementando configuraciones de seguridad recomendadas.
"""

import os
import sys
import json
import logging
import subprocess
import winreg
import win32security
import win32net
import win32netcon
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
import concurrent.futures
import argparse

class ServerHardening:
    def __init__(self, server_name: str):
        """
        Inicializa el analizador de hardening
        
        Args:
            server_name (str): Nombre o IP del servidor a analizar
        """
        self.server_name = server_name
        self.results = {
            'informacion_basica': {},
            'configuraciones': {},
            'vulnerabilidades': [],
            'recomendaciones': [],
            'riesgo': 0
        }
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def verificar_servicios(self) -> Dict[str, Any]:
        """
        Verifica los servicios en ejecución y sus configuraciones
        
        Returns:
            Dict[str, Any]: Información de servicios
        """
        try:
            servicios = {}
            output = subprocess.check_output(['sc', 'query'], text=True)
            
            for line in output.split('\n'):
                if 'SERVICE_NAME' in line:
                    service_name = line.split(':')[1].strip()
                    try:
                        # Obtener información detallada del servicio
                        service_info = subprocess.check_output(
                            ['sc', 'qc', service_name], 
                            text=True
                        )
                        
                        # Extraer configuración
                        config = {
                            'tipo_inicio': None,
                            'cuenta': None,
                            'dependencias': []
                        }
                        
                        for info_line in service_info.split('\n'):
                            if 'START_TYPE' in info_line:
                                config['tipo_inicio'] = info_line.split(':')[1].strip()
                            elif 'SERVICE_START_NAME' in info_line:
                                config['cuenta'] = info_line.split(':')[1].strip()
                            elif 'DEPENDENCIES' in info_line:
                                config['dependencias'] = [
                                    dep.strip() for dep in 
                                    info_line.split(':')[1].split(',')
                                ]
                                
                        servicios[service_name] = config
                    except:
                        logging.warning(f"No se pudo obtener información del servicio {service_name}")
                        
            self.results['configuraciones']['servicios'] = servicios
            return servicios
        except Exception as e:
            logging.error(f"Error al verificar servicios: {str(e)}")
            return {}
            
    def verificar_politicas(self) -> Dict[str, Any]:
        """
        Verifica las políticas de seguridad del servidor
        
        Returns:
            Dict[str, Any]: Información de políticas
        """
        try:
            politicas = {}
            
            # Verificar políticas de contraseñas
            output = subprocess.check_output(
                ['net', 'accounts'], 
                text=True
            )
            
            politicas['cuentas'] = {}
            for line in output.split('\n'):
                if 'Minimum password age' in line:
                    politicas['cuentas']['edad_minima'] = line.split(':')[1].strip()
                elif 'Maximum password age' in line:
                    politicas['cuentas']['edad_maxima'] = line.split(':')[1].strip()
                elif 'Minimum password length' in line:
                    politicas['cuentas']['longitud_minima'] = line.split(':')[1].strip()
                    
            # Verificar políticas de auditoría
            output = subprocess.check_output(
                ['auditpol', '/get', '/category:*'], 
                text=True
            )
            
            politicas['auditoria'] = {}
            for line in output.split('\n'):
                if 'Success' in line or 'Failure' in line:
                    categoria = line.split('  ')[0].strip()
                    estado = line.split('  ')[-1].strip()
                    politicas['auditoria'][categoria] = estado
                    
            self.results['configuraciones']['politicas'] = politicas
            return politicas
        except Exception as e:
            logging.error(f"Error al verificar políticas: {str(e)}")
            return {}
            
    def verificar_usuarios(self) -> Dict[str, Any]:
        """
        Verifica los usuarios y grupos del servidor
        
        Returns:
            Dict[str, Any]: Información de usuarios y grupos
        """
        try:
            usuarios = {}
            
            # Obtener lista de usuarios
            output = subprocess.check_output(
                ['net', 'user'], 
                text=True
            )
            
            usuarios['lista'] = []
            for line in output.split('\n'):
                if line.strip() and not line.startswith('The command completed'):
                    usuarios['lista'].append(line.strip())
                    
            # Verificar grupos administrativos
            output = subprocess.check_output(
                ['net', 'localgroup', 'Administrators'], 
                text=True
            )
            
            usuarios['administradores'] = []
            for line in output.split('\n'):
                if line.strip() and not line.startswith('The command completed'):
                    usuarios['administradores'].append(line.strip())
                    
            self.results['configuraciones']['usuarios'] = usuarios
            return usuarios
        except Exception as e:
            logging.error(f"Error al verificar usuarios: {str(e)}")
            return {}
            
    def buscar_vulnerabilidades(self) -> List[Dict[str, Any]]:
        """
        Busca vulnerabilidades conocidas en la configuración
        
        Returns:
            List[Dict[str, Any]]: Lista de vulnerabilidades encontradas
        """
        try:
            vulnerabilidades = []
            
            # Verificar servicios con cuentas privilegiadas
            for servicio, config in self.results['configuraciones'].get('servicios', {}).items():
                if config['cuenta'] in ['LocalSystem', 'NT AUTHORITY\\SYSTEM']:
                    vulnerabilidades.append({
                        'tipo': 'Servicio Privilegiado',
                        'servicio': servicio,
                        'cuenta': config['cuenta'],
                        'severidad': 'Media',
                        'descripcion': 'Servicio ejecutándose con privilegios elevados'
                    })
                    
            # Verificar políticas de contraseñas débiles
            politicas = self.results['configuraciones'].get('politicas', {})
            if politicas.get('cuentas', {}).get('longitud_minima', '0') < '8':
                vulnerabilidades.append({
                    'tipo': 'Política de Contraseñas Débil',
                    'configuracion': 'longitud_minima',
                    'valor_actual': politicas['cuentas']['longitud_minima'],
                    'severidad': 'Alta',
                    'descripcion': 'Longitud mínima de contraseña insuficiente'
                })
                
            # Verificar usuarios administrativos
            usuarios = self.results['configuraciones'].get('usuarios', {})
            if len(usuarios.get('administradores', [])) > 2:
                vulnerabilidades.append({
                    'tipo': 'Exceso de Administradores',
                    'cantidad': len(usuarios['administradores']),
                    'severidad': 'Media',
                    'descripcion': 'Demasiados usuarios con privilegios administrativos'
                })
                
            self.results['vulnerabilidades'] = vulnerabilidades
            return vulnerabilidades
        except Exception as e:
            logging.error(f"Error al buscar vulnerabilidades: {str(e)}")
            return []
            
    def generar_recomendaciones(self) -> List[Dict[str, Any]]:
        """
        Genera recomendaciones de hardening basadas en los hallazgos
        
        Returns:
            List[Dict[str, Any]]: Lista de recomendaciones
        """
        try:
            recomendaciones = []
            
            # Recomendaciones para servicios
            for servicio, config in self.results['configuraciones'].get('servicios', {}).items():
                if config['cuenta'] in ['LocalSystem', 'NT AUTHORITY\\SYSTEM']:
                    recomendaciones.append({
                        'categoria': 'Servicios',
                        'accion': 'Cambiar cuenta de servicio',
                        'servicio': servicio,
                        'recomendacion': f'Cambiar la cuenta del servicio {servicio} a una cuenta con menos privilegios'
                    })
                    
            # Recomendaciones para políticas
            politicas = self.results['configuraciones'].get('politicas', {})
            if politicas.get('cuentas', {}).get('longitud_minima', '0') < '8':
                recomendaciones.append({
                    'categoria': 'Políticas',
                    'accion': 'Aumentar longitud mínima de contraseña',
                    'valor_actual': politicas['cuentas']['longitud_minima'],
                    'valor_recomendado': '8',
                    'recomendacion': 'Establecer longitud mínima de contraseña a 8 caracteres'
                })
                
            # Recomendaciones para usuarios
            usuarios = self.results['configuraciones'].get('usuarios', {})
            if len(usuarios.get('administradores', [])) > 2:
                recomendaciones.append({
                    'categoria': 'Usuarios',
                    'accion': 'Reducir administradores',
                    'cantidad_actual': len(usuarios['administradores']),
                    'recomendacion': 'Reducir el número de usuarios administrativos al mínimo necesario'
                })
                
            self.results['recomendaciones'] = recomendaciones
            return recomendaciones
        except Exception as e:
            logging.error(f"Error al generar recomendaciones: {str(e)}")
            return []
            
    def calcular_riesgo(self) -> int:
        """
        Calcula el nivel de riesgo basado en las vulnerabilidades encontradas
        
        Returns:
            int: Nivel de riesgo (0-100)
        """
        try:
            riesgo = 0
            
            # Riesgo por vulnerabilidades
            for vuln in self.results['vulnerabilidades']:
                if vuln['severidad'] == 'Alta':
                    riesgo += 30
                elif vuln['severidad'] == 'Media':
                    riesgo += 20
                else:
                    riesgo += 10
                    
            # Riesgo por servicios privilegiados
            servicios = self.results['configuraciones'].get('servicios', {})
            riesgo += sum(1 for config in servicios.values() 
                        if config['cuenta'] in ['LocalSystem', 'NT AUTHORITY\\SYSTEM']) * 10
            
            # Riesgo por políticas débiles
            politicas = self.results['configuraciones'].get('politicas', {})
            if politicas.get('cuentas', {}).get('longitud_minima', '0') < '8':
                riesgo += 20
                
            # Limitar riesgo a 100
            riesgo = min(riesgo, 100)
            
            self.results['riesgo'] = riesgo
            return riesgo
        except Exception as e:
            logging.error(f"Error al calcular riesgo: {str(e)}")
            return 0
            
    def generar_reporte(self, output_file: str):
        """
        Genera un reporte con los resultados del análisis
        
        Args:
            output_file (str): Ruta base para los archivos de salida
        """
        try:
            # Agregar metadatos al reporte
            reporte = {
                'fecha_analisis': datetime.now().isoformat(),
                'servidor': self.server_name,
                'resultados': self.results
            }
            
            # Guardar reporte en JSON
            with open(output_file + '.json', 'w') as f:
                json.dump(reporte, f, indent=4)
                
            # Guardar reporte en CSV
            df = pd.DataFrame([{
                'servidor': reporte['servidor'],
                'fecha': reporte['fecha_analisis'],
                'riesgo': reporte['resultados']['riesgo'],
                'vulnerabilidades': len(reporte['resultados']['vulnerabilidades']),
                'recomendaciones': len(reporte['resultados']['recomendaciones']),
                'servicios_privilegiados': sum(1 for config in reporte['resultados']['configuraciones'].get('servicios', {}).values() 
                                            if config['cuenta'] in ['LocalSystem', 'NT AUTHORITY\\SYSTEM'])
            }])
            df.to_csv(output_file + '.csv', index=False)
            
            logging.info(f"Reporte generado en {output_file}.json y {output_file}.csv")
        except Exception as e:
            logging.error(f"Error al generar reporte: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Analizador de Hardening de Servidores')
    parser.add_argument('server', help='Nombre o IP del servidor a analizar')
    parser.add_argument('--output', default='reporte_hardening', 
                       help='Ruta base para los archivos de salida')
    
    args = parser.parse_args()
    
    analyzer = ServerHardening(args.server)
    
    # Realizar análisis
    servicios = analyzer.verificar_servicios()
    politicas = analyzer.verificar_politicas()
    usuarios = analyzer.verificar_usuarios()
    vulnerabilidades = analyzer.buscar_vulnerabilidades()
    recomendaciones = analyzer.generar_recomendaciones()
    riesgo = analyzer.calcular_riesgo()
    
    # Generar reporte
    analyzer.generar_reporte(args.output)

if __name__ == "__main__":
    main() 