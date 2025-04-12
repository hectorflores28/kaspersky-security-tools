#!/usr/bin/env python3
import socket
import sys
from datetime import datetime

def scan_ports(target, start_port, end_port):
    print(f"\nEscaneando objetivo: {target}")
    print(f"Rango de puertos: {start_port}-{end_port}")
    print("-" * 50)
    
    start_time = datetime.now()
    
    try:
        for port in range(start_port, end_port + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            
            if result == 0:
                print(f"Puerto {port}: Abierto")
            sock.close()
            
    except KeyboardInterrupt:
        print("\nEscaneo interrumpido por el usuario")
        sys.exit()
    except socket.gaierror:
        print("No se pudo resolver el nombre de host")
        sys.exit()
    except socket.error:
        print("No se pudo conectar al servidor")
        sys.exit()
    
    end_time = datetime.now()
    print(f"\nEscaneo completado en: {end_time - start_time}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python port_scanner.py <host> <puerto_inicio> <puerto_fin>")
        print("Ejemplo: python port_scanner.py 192.168.1.1 1 1000")
        sys.exit()
    
    target = sys.argv[1]
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])
    
    scan_ports(target, start_port, end_port) 