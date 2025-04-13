#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analizador de Correos Electrónicos
Este script analiza correos electrónicos en busca de indicadores de phishing,
incluyendo análisis de headers, URLs, adjuntos y contenido.
"""

import os
import sys
import json
import logging
import email
import re
import urllib.parse
import dns.resolver
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
import hashlib
import magic
import requests
from bs4 import BeautifulSoup

class EmailAnalyzer:
    def __init__(self, email_path: str):
        """
        Inicializa el analizador de correos
        
        Args:
            email_path (str): Ruta al archivo de correo
        """
        self.email_path = email_path
        self.results = {
            'informacion_basica': {},
            'headers': {},
            'contenido': {},
            'urls': [],
            'adjuntos': [],
            'indicadores_phishing': [],
            'riesgo': 0
        }
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def cargar_correo(self) -> Optional[email.message.Message]:
        """
        Carga el correo desde el archivo
        
        Returns:
            Optional[email.message.Message]: Objeto de correo o None si hay error
        """
        try:
            with open(self.email_path, 'r', encoding='utf-8') as f:
                return email.message_from_file(f)
        except Exception as e:
            logging.error(f"Error al cargar correo: {str(e)}")
            return None
            
    def analizar_headers(self, msg: email.message.Message) -> Dict[str, Any]:
        """
        Analiza los headers del correo
        
        Args:
            msg (email.message.Message): Objeto de correo
            
        Returns:
            Dict[str, Any]: Información de los headers
        """
        try:
            headers = {
                'from': msg.get('From', ''),
                'to': msg.get('To', ''),
                'subject': msg.get('Subject', ''),
                'date': msg.get('Date', ''),
                'return_path': msg.get('Return-Path', ''),
                'received': msg.get_all('Received', []),
                'spf': msg.get('Received-SPF', ''),
                'dkim': msg.get('DKIM-Signature', ''),
                'dmarc': msg.get('Authentication-Results', '')
            }
            
            self.results['headers'] = headers
            return headers
        except Exception as e:
            logging.error(f"Error al analizar headers: {str(e)}")
            return {}
            
    def analizar_contenido(self, msg: email.message.Message) -> Dict[str, Any]:
        """
        Analiza el contenido del correo
        
        Args:
            msg (email.message.Message): Objeto de correo
            
        Returns:
            Dict[str, Any]: Información del contenido
        """
        try:
            contenido = {
                'texto_plano': '',
                'html': '',
                'urls': [],
                'palabras_clave': []
            }
            
            # Extraer texto plano y HTML
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    contenido['texto_plano'] += part.get_payload(decode=True).decode('utf-8', errors='ignore')
                elif part.get_content_type() == 'text/html':
                    contenido['html'] += part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    
            # Extraer URLs
            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 
                            contenido['texto_plano'] + contenido['html'])
            contenido['urls'] = list(set(urls))
            
            # Buscar palabras clave de phishing
            palabras_clave = [
                'urgente', 'importante', 'verificar', 'cuenta', 'contraseña',
                'seguridad', 'banco', 'paypal', 'amazon', 'microsoft',
                'actualizar', 'confirmar', 'suspender', 'bloquear'
            ]
            
            texto_completo = contenido['texto_plano'].lower() + contenido['html'].lower()
            contenido['palabras_clave'] = [word for word in palabras_clave if word in texto_completo]
            
            self.results['contenido'] = contenido
            return contenido
        except Exception as e:
            logging.error(f"Error al analizar contenido: {str(e)}")
            return {}
            
    def analizar_urls(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Analiza las URLs encontradas en el correo
        
        Args:
            urls (List[str]): Lista de URLs a analizar
            
        Returns:
            List[Dict[str, Any]]: Información de las URLs
        """
        try:
            urls_info = []
            for url in urls:
                parsed = urllib.parse.urlparse(url)
                info = {
                    'url': url,
                    'dominio': parsed.netloc,
                    'ruta': parsed.path,
                    'parametros': parsed.query,
                    'es_phishing': False,
                    'motivos': []
                }
                
                # Verificar dominio
                try:
                    dns.resolver.resolve(parsed.netloc, 'A')
                except:
                    info['motivos'].append('Dominio no resuelvable')
                    info['es_phishing'] = True
                    
                # Verificar longitud de URL
                if len(url) > 100:
                    info['motivos'].append('URL muy larga')
                    info['es_phishing'] = True
                    
                # Verificar caracteres especiales
                if '%' in url or '@' in url:
                    info['motivos'].append('Caracteres sospechosos en URL')
                    info['es_phishing'] = True
                    
                urls_info.append(info)
                
            self.results['urls'] = urls_info
            return urls_info
        except Exception as e:
            logging.error(f"Error al analizar URLs: {str(e)}")
            return []
            
    def analizar_adjuntos(self, msg: email.message.Message) -> List[Dict[str, Any]]:
        """
        Analiza los archivos adjuntos del correo
        
        Args:
            msg (email.message.Message): Objeto de correo
            
        Returns:
            List[Dict[str, Any]]: Información de los adjuntos
        """
        try:
            adjuntos = []
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                    
                filename = part.get_filename()
                if filename:
                    adjunto = {
                        'nombre': filename,
                        'tipo': part.get_content_type(),
                        'tamano': len(part.get_payload(decode=True)),
                        'hash_md5': hashlib.md5(part.get_payload(decode=True)).hexdigest(),
                        'es_sospechoso': False,
                        'motivos': []
                    }
                    
                    # Verificar extensiones sospechosas
                    extensiones_sospechosas = ['.exe', '.bat', '.cmd', '.ps1', '.vbs', '.js', '.jar']
                    if any(filename.lower().endswith(ext) for ext in extensiones_sospechosas):
                        adjunto['motivos'].append('Extensión sospechosa')
                        adjunto['es_sospechoso'] = True
                        
                    adjuntos.append(adjunto)
                    
            self.results['adjuntos'] = adjuntos
            return adjuntos
        except Exception as e:
            logging.error(f"Error al analizar adjuntos: {str(e)}")
            return []
            
    def buscar_indicadores_phishing(self) -> List[str]:
        """
        Busca indicadores de phishing en el correo
        
        Returns:
            List[str]: Lista de indicadores encontrados
        """
        try:
            indicadores = []
            
            # Verificar headers
            if not self.results['headers'].get('spf'):
                indicadores.append('Falta verificación SPF')
            if not self.results['headers'].get('dkim'):
                indicadores.append('Falta firma DKIM')
                
            # Verificar URLs
            for url in self.results['urls']:
                if url['es_phishing']:
                    indicadores.append(f"URL sospechosa: {url['url']}")
                    
            # Verificar adjuntos
            for adjunto in self.results['adjuntos']:
                if adjunto['es_sospechoso']:
                    indicadores.append(f"Adjunto sospechoso: {adjunto['nombre']}")
                    
            # Verificar contenido
            if len(self.results['contenido'].get('palabras_clave', [])) > 3:
                indicadores.append('Múltiples palabras clave de phishing')
                
            self.results['indicadores_phishing'] = indicadores
            return indicadores
        except Exception as e:
            logging.error(f"Error al buscar indicadores de phishing: {str(e)}")
            return []
            
    def calcular_riesgo(self) -> int:
        """
        Calcula el nivel de riesgo del correo
        
        Returns:
            int: Nivel de riesgo (0-100)
        """
        try:
            riesgo = 0
            
            # Riesgo por indicadores de phishing
            riesgo += len(self.results['indicadores_phishing']) * 10
            
            # Riesgo por URLs sospechosas
            riesgo += sum(1 for url in self.results['urls'] if url['es_phishing']) * 15
            
            # Riesgo por adjuntos sospechosos
            riesgo += sum(1 for adjunto in self.results['adjuntos'] if adjunto['es_sospechoso']) * 20
            
            # Riesgo por palabras clave
            riesgo += len(self.results['contenido'].get('palabras_clave', [])) * 5
            
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
            output_file (str): Ruta al archivo de salida
        """
        try:
            # Agregar metadatos al reporte
            reporte = {
                'fecha_analisis': datetime.now().isoformat(),
                'correo_analizado': self.email_path,
                'resultados': self.results
            }
            
            # Guardar reporte en JSON
            with open(output_file + '.json', 'w') as f:
                json.dump(reporte, f, indent=4)
                
            # Guardar reporte en CSV
            df = pd.DataFrame([{
                'correo': reporte['correo_analizado'],
                'fecha': reporte['fecha_analisis'],
                'riesgo': reporte['resultados']['riesgo'],
                'indicadores': len(reporte['resultados']['indicadores_phishing']),
                'urls_sospechosas': sum(1 for url in reporte['resultados']['urls'] if url['es_phishing']),
                'adjuntos_sospechosos': sum(1 for adjunto in reporte['resultados']['adjuntos'] if adjunto['es_sospechoso'])
            }])
            df.to_csv(output_file + '.csv', index=False)
            
            logging.info(f"Reporte generado en {output_file}.json y {output_file}.csv")
        except Exception as e:
            logging.error(f"Error al generar reporte: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Analizador de Correos Electrónicos')
    parser.add_argument('email', help='Ruta al archivo de correo')
    parser.add_argument('--output', default='reporte_correo', 
                       help='Ruta base para los archivos de salida')
    
    args = parser.parse_args()
    
    if not os.path.isfile(args.email):
        logging.error(f"El archivo {args.email} no existe")
        sys.exit(1)
        
    analyzer = EmailAnalyzer(args.email)
    
    # Cargar y analizar correo
    msg = analyzer.cargar_correo()
    if not msg:
        sys.exit(1)
        
    analyzer.analizar_headers(msg)
    analyzer.analizar_contenido(msg)
    analyzer.analizar_urls(analyzer.results['contenido']['urls'])
    analyzer.analizar_adjuntos(msg)
    analyzer.buscar_indicadores_phishing()
    analyzer.calcular_riesgo()
    
    # Generar reporte
    analyzer.generar_reporte(args.output)

if __name__ == "__main__":
    main() 