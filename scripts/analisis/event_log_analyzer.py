#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analizador de Registros de Windows

Este script analiza los registros de eventos de Windows para detectar actividades sospechosas
y construir líneas de tiempo de eventos de seguridad.
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Tuple
from scripts.utilidades.common import Logger, Config

class EventLogAnalyzer:
    def __init__(self):
        self.logger = Logger("event_log_analyzer").get_logger()
        self.config = Config()
        
        # IDs de eventos importantes
        self.security_events = {
            '4624': 'Inicio de sesión exitoso',
            '4625': 'Inicio de sesión fallido',
            '4634': 'Cierre de sesión',
            '4648': 'Inicio de sesión con credenciales explícitas',
            '4672': 'Asignación de privilegios especiales',
            '4673': 'Operación con privilegios especiales',
            '4768': 'Solicitud de ticket Kerberos (TGT)',
            '4769': 'Solicitud de ticket de servicio Kerberos (TGS)'
        }

    def parse_event(self, event_xml: str) -> Dict:
        """Parsea un evento XML de Windows."""
        try:
            root = ET.fromstring(event_xml)
            event_data = {}
            
            # Extraer información básica
            event_data['EventID'] = root.find('.//EventID').text
            event_data['TimeCreated'] = root.find('.//TimeCreated').get('SystemTime')
            event_data['Computer'] = root.find('.//Computer').text
            
            # Extraer datos específicos
            data = root.findall('.//Data')
            for item in data:
                name = item.get('Name')
                if name:
                    event_data[name] = item.text
                    
            return event_data
            
        except Exception as e:
            self.logger.error(f"Error al parsear evento: {e}")
            return {}

    def analyze_logon_events(self, events: List[Dict]) -> List[Dict]:
        """Analiza eventos de inicio de sesión."""
        suspicious_events = []
        
        for event in events:
            if event['EventID'] in ['4624', '4625']:
                # Verificar inicio de sesión remoto
                if event.get('LogonType') == '10':  # RDP
                    suspicious_events.append({
                        'timestamp': event['TimeCreated'],
                        'user': event.get('TargetUserName'),
                        'ip': event.get('IpAddress'),
                        'type': 'Inicio de sesión remoto'
                    })
                
                # Verificar múltiples intentos fallidos
                if event['EventID'] == '4625':
                    suspicious_events.append({
                        'timestamp': event['TimeCreated'],
                        'user': event.get('TargetUserName'),
                        'ip': event.get('IpAddress'),
                        'type': 'Intento de inicio de sesión fallido'
                    })
                    
        return suspicious_events

    def analyze_privilege_events(self, events: List[Dict]) -> List[Dict]:
        """Analiza eventos de privilegios."""
        suspicious_events = []
        
        for event in events:
            if event['EventID'] in ['4672', '4673']:
                suspicious_events.append({
                    'timestamp': event['TimeCreated'],
                    'user': event.get('SubjectUserName'),
                    'privilege': event.get('PrivilegeList'),
                    'type': 'Uso de privilegios especiales'
                })
                
        return suspicious_events

    def build_timeline(self, events: List[Dict]) -> List[Dict]:
        """Construye una línea de tiempo de eventos."""
        timeline = []
        
        for event in events:
            if event['EventID'] in self.security_events:
                timeline.append({
                    'timestamp': event['TimeCreated'],
                    'event_id': event['EventID'],
                    'description': self.security_events[event['EventID']],
                    'user': event.get('TargetUserName') or event.get('SubjectUserName'),
                    'computer': event['Computer']
                })
                
        # Ordenar por timestamp
        timeline.sort(key=lambda x: x['timestamp'])
        return timeline

    def analyze_log_file(self, log_file: str) -> Dict:
        """
        Analiza un archivo de registro de eventos.
        
        Args:
            log_file: Ruta al archivo de registro (.evtx)
            
        Returns:
            Dict: Resultados del análisis
        """
        try:
            # Aquí iría el código para leer el archivo .evtx
            # Por ahora simulamos algunos eventos
            events = [
                {
                    'EventID': '4624',
                    'TimeCreated': '2024-01-01T12:00:00Z',
                    'Computer': 'WORKSTATION1',
                    'TargetUserName': 'admin',
                    'LogonType': '10',
                    'IpAddress': '192.168.1.100'
                }
            ]
            
            results = {
                'suspicious_logons': self.analyze_logon_events(events),
                'privilege_events': self.analyze_privilege_events(events),
                'timeline': self.build_timeline(events)
            }
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error al analizar archivo de registro: {e}")
            raise

def main():
    import sys
    
    if len(sys.argv) != 2:
        print("Uso: python event_log_analyzer.py <archivo_registro>")
        sys.exit(1)
        
    analyzer = EventLogAnalyzer()
    log_file = sys.argv[1]
    
    try:
        results = analyzer.analyze_log_file(log_file)
        
        print("\nResultados del análisis:")
        print("-" * 50)
        
        print("\nEventos sospechosos de inicio de sesión:")
        for event in results['suspicious_logons']:
            print(f"Fecha: {event['timestamp']}")
            print(f"Usuario: {event['user']}")
            print(f"IP: {event['ip']}")
            print(f"Tipo: {event['type']}")
            print("-" * 30)
            
        print("\nEventos de privilegios:")
        for event in results['privilege_events']:
            print(f"Fecha: {event['timestamp']}")
            print(f"Usuario: {event['user']}")
            print(f"Privilegios: {event['privilege']}")
            print("-" * 30)
            
        print("\nLínea de tiempo de eventos:")
        for event in results['timeline']:
            print(f"Fecha: {event['timestamp']}")
            print(f"Evento: {event['description']}")
            print(f"Usuario: {event['user']}")
            print(f"Computadora: {event['computer']}")
            print("-" * 30)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 