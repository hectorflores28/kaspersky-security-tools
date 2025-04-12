#!/usr/bin/env python3
import requests
import sys
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

def check_directory(url, directory):
    full_url = urljoin(url, directory)
    try:
        response = requests.get(full_url, timeout=5)
        if response.status_code == 200:
            print(f"[+] Encontrado: {full_url}")
        elif response.status_code == 403:
            print(f"[!] Prohibido: {full_url}")
    except requests.RequestException:
        pass

def main():
    if len(sys.argv) != 3:
        print("Uso: python dir_enum.py <url> <wordlist>")
        print("Ejemplo: python dir_enum.py http://example.com wordlist.txt")
        sys.exit(1)

    url = sys.argv[1]
    wordlist_file = sys.argv[2]

    try:
        with open(wordlist_file, 'r') as f:
            directories = [line.strip() for line in f]
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {wordlist_file}")
        sys.exit(1)

    print(f"\nIniciando enumeración de directorios en: {url}")
    print("-" * 50)

    with ThreadPoolExecutor(max_workers=10) as executor:
        for directory in directories:
            executor.submit(check_directory, url, directory)

if __name__ == "__main__":
    main() 