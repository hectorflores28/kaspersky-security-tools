#!/usr/bin/env python3
import socket
import sys
from datetime import datetime

def scan_ports(target, start_port, end_port):
    print(f"\nScanning target: {target}")
    print(f"Port range: {start_port}-{end_port}")
    print("-" * 50)
    
    start_time = datetime.now()
    
    try:
        for port in range(start_port, end_port + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            
            if result == 0:
                print(f"Port {port}: Open")
            sock.close()
            
    except KeyboardInterrupt:
        print("\nScan interrupted by user")
        sys.exit()
    except socket.gaierror:
        print("Could not resolve hostname")
        sys.exit()
    except socket.error:
        print("Could not connect to server")
        sys.exit()
    
    end_time = datetime.now()
    print(f"\nScan completed in: {end_time - start_time}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python port_scanner.py <host> <start_port> <end_port>")
        print("Example: python port_scanner.py 192.168.1.1 1 1000")
        sys.exit()
    
    target = sys.argv[1]
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])
    
    scan_ports(target, start_port, end_port) 