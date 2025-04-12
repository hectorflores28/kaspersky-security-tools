#!/usr/bin/env python3
import re
import sys
from collections import Counter
from datetime import datetime

def analyze_logs(log_file):
    print(f"\nAnalizando archivo: {log_file}")
    print("-" * 50)
    
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    error_pattern = r'ERROR|error|Error'
    
    ip_addresses = []
    errors = []
    
    try:
        with open(log_file, 'r') as f:
            for line in f:
                # Buscar direcciones IP
                ips = re.findall(ip_pattern, line)
                ip_addresses.extend(ips)
                
                # Buscar errores
                if re.search(error_pattern, line):
                    errors.append(line.strip())
    
        # Análisis de IPs
        ip_counter = Counter(ip_addresses)
        print("\nTop 10 IPs más frecuentes:")
        for ip, count in ip_counter.most_common(10):
            print(f"{ip}: {count} ocurrencias")
            
        # Análisis de errores
        print("\nErrores encontrados:")
        for error in errors[:10]:  # Mostrar solo los primeros 10 errores
            print(f"- {error}")
            
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {log_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error durante el análisis: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python log_analyzer.py <archivo_log>")
        print("Ejemplo: python log_analyzer.py access.log")
        sys.exit(1)
        
    log_file = sys.argv[1]
    analyze_logs(log_file) 