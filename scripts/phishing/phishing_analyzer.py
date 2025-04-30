#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analizador de Phishing

Este script proporciona herramientas para el análisis de intentos de phishing,
incluyendo detección de URLs sospechosas y análisis de contenido de correos electrónicos.
"""

import re
import json
import logging
import requests
import urllib.parse
from datetime import datetime
from typing import Dict, List, Optional
import dns.resolver
from bs4 import BeautifulSoup
import whois
import socket

class PhishingAnalyzer:
    def __init__(self):
        """Inicializa el analizador de phishing."""
        self.logger = self._setup_logging()
        self.suspicious_patterns = [
            r'login',
            r'password',
            r'account',
            r'verify',
            r'secure',
            r'update',
            r'confirm',
            r'bank',
            r'paypal',
            r'credit',
            r'card'
        ]
        
    def _setup_logging(self) -> logging.Logger:
        """Configura el sistema de logging."""
        logger = logging.getLogger('phishing_analyzer')
        logger.setLevel(logging.INFO)
        
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        fh = logging.FileHandler(f'logs/phishing_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        fh.setLevel(logging.INFO)
        
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger

    def analyze_url(self, url: str) -> Dict:
        """Analiza una URL en busca de indicadores de phishing."""
        self.logger.info(f"Analizando URL: {url}")
        results = {
            'url': url,
            'domain': None,
            'ip_address': None,
            'whois_info': None,
            'dns_records': None,
            'suspicious_keywords': [],
            'redirects': [],
            'ssl_info': None,
            'risk_score': 0
        }
        
        try:
            # Parsear URL
            parsed_url = urllib.parse.urlparse(url)
            results['domain'] = parsed_url.netloc
            
            # Obtener IP
            ip = socket.gethostbyname(parsed_url.netloc)
            results['ip_address'] = ip
            
            # Obtener información WHOIS
            try:
                w = whois.whois(parsed_url.netloc)
                results['whois_info'] = {
                    'registrar': w.registrar,
                    'creation_date': str(w.creation_date),
                    'expiration_date': str(w.expiration_date)
                }
            except Exception as e:
                self.logger.warning(f"Error al obtener WHOIS: {str(e)}")
            
            # Obtener registros DNS
            try:
                dns_records = {}
                for record_type in ['A', 'MX', 'NS', 'TXT']:
                    try:
                        answers = dns.resolver.resolve(parsed_url.netloc, record_type)
                        dns_records[record_type] = [str(rdata) for rdata in answers]
                    except:
                        continue
                results['dns_records'] = dns_records
            except Exception as e:
                self.logger.warning(f"Error al obtener registros DNS: {str(e)}")
            
            # Buscar palabras clave sospechosas
            for pattern in self.suspicious_patterns:
                if re.search(pattern, url, re.IGNORECASE):
                    results['suspicious_keywords'].append(pattern)
            
            # Seguir redirecciones
            try:
                response = requests.get(url, allow_redirects=True, timeout=10)
                results['redirects'] = [r.url for r in response.history]
                
                # Analizar contenido HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                forms = soup.find_all('form')
                if forms:
                    results['risk_score'] += 20
                
                # Buscar campos de contraseña
                password_fields = soup.find_all('input', {'type': 'password'})
                if password_fields:
                    results['risk_score'] += 30
                
            except Exception as e:
                self.logger.warning(f"Error al analizar contenido: {str(e)}")
            
            # Calcular puntaje de riesgo
            if results['suspicious_keywords']:
                results['risk_score'] += len(results['suspicious_keywords']) * 10
            if len(results['redirects']) > 2:
                results['risk_score'] += 20
            if results['whois_info'] and results['whois_info']['creation_date']:
                creation_date = datetime.strptime(results['whois_info']['creation_date'], '%Y-%m-%d %H:%M:%S')
                if (datetime.now() - creation_date).days < 30:
                    results['risk_score'] += 30
            
        except Exception as e:
            self.logger.error(f"Error al analizar URL: {str(e)}")
            
        return results

    def analyze_email(self, email_content: str) -> Dict:
        """Analiza el contenido de un correo electrónico en busca de phishing."""
        self.logger.info("Analizando contenido de correo electrónico")
        results = {
            'suspicious_keywords': [],
            'links': [],
            'attachments': [],
            'risk_score': 0
        }
        
        try:
            # Buscar palabras clave sospechosas
            for pattern in self.suspicious_patterns:
                if re.search(pattern, email_content, re.IGNORECASE):
                    results['suspicious_keywords'].append(pattern)
            
            # Buscar URLs
            url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            urls = re.findall(url_pattern, email_content)
            results['links'] = urls
            
            # Buscar archivos adjuntos
            attachment_pattern = r'filename="([^"]+)"'
            attachments = re.findall(attachment_pattern, email_content)
            results['attachments'] = attachments
            
            # Calcular puntaje de riesgo
            results['risk_score'] = len(results['suspicious_keywords']) * 10
            results['risk_score'] += len(results['links']) * 5
            results['risk_score'] += len(results['attachments']) * 15
            
        except Exception as e:
            self.logger.error(f"Error al analizar correo electrónico: {str(e)}")
            
        return results

    def export_results(self, data: Dict, output_file: str) -> None:
        """Exporta los resultados del análisis a un archivo JSON."""
        try:
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=4)
            self.logger.info(f"Resultados exportados a {output_file}")
        except Exception as e:
            self.logger.error(f"Error al exportar resultados: {str(e)}")

def main():
    """Función principal del script."""
    analyzer = PhishingAnalyzer()
    
    # Ejemplo de análisis de URL
    url = "https://example.com/login"
    url_results = analyzer.analyze_url(url)
    analyzer.export_results(url_results, f'url_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    
    # Ejemplo de análisis de correo electrónico
    email_content = """
    Estimado usuario,
    
    Su cuenta necesita ser verificada. Por favor, haga clic en el siguiente enlace:
    https://example.com/verify?token=123
    
    Atentamente,
    El Equipo de Soporte
    """
    email_results = analyzer.analyze_email(email_content)
    analyzer.export_results(email_results, f'email_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')

if __name__ == "__main__":
    main() 