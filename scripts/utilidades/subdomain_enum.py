#!/usr/bin/env python3
import requests
import sys
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

def check_subdomain(subdomain, domain):
    url = f"http://{subdomain}.{domain}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"[+] Encontrado: {url}")
    except requests.RequestException:
        pass

def main():
    if len(sys.argv) != 3:
        print("Uso: python subdomain_enum.py <dominio> <wordlist>")
        print("Ejemplo: python subdomain_enum.py example.com subdomains.txt")
        sys.exit(1)

    domain = sys.argv[1]
    wordlist_file = sys.argv[2]

    try:
        with open(wordlist_file, 'r') as f:
            subdomains = [line.strip() for line in f]
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {wordlist_file}")
        sys.exit(1)

    print(f"\nIniciando enumeración de subdominios para: {domain}")
    print("-" * 50)

    with ThreadPoolExecutor(max_workers=10) as executor:
        for subdomain in subdomains:
            executor.submit(check_subdomain, subdomain, domain)

if __name__ == "__main__":
    main() 