#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Verificador de Contraseñas con Have I Been Pwned

Este script verifica si una contraseña ha sido comprometida usando la API de Have I Been Pwned.
Implementa el método k-anonimity para proteger la privacidad de las contraseñas.
"""

import hashlib
import requests
from typing import Tuple, List
from scripts.utilidades.common import Logger, Config

class PasswordChecker:
    def __init__(self):
        self.logger = Logger("password_checker").get_logger()
        self.config = Config()
        self.api_url = "https://api.pwnedpasswords.com/range/"

    def get_sha1_hash(self, password: str) -> str:
        """Calcula el hash SHA-1 de una contraseña."""
        return hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    def check_password(self, password: str) -> Tuple[bool, int]:
        """
        Verifica si una contraseña ha sido comprometida.
        
        Args:
            password: La contraseña a verificar
            
        Returns:
            Tuple[bool, int]: (comprometida, número de veces encontrada)
        """
        try:
            # Calcular hash SHA-1
            password_hash = self.get_sha1_hash(password)
            prefix, suffix = password_hash[:5], password_hash[5:]
            
            # Realizar petición a la API
            response = requests.get(f"{self.api_url}{prefix}")
            response.raise_for_status()
            
            # Buscar el sufijo en la respuesta
            for line in response.text.splitlines():
                hash_suffix, count = line.split(':')
                if hash_suffix == suffix:
                    return True, int(count)
                    
            return False, 0
            
        except Exception as e:
            self.logger.error(f"Error al verificar contraseña: {e}")
            raise

    def check_password_file(self, file_path: str) -> List[Tuple[str, bool, int]]:
        """
        Verifica contraseñas desde un archivo de texto.
        
        Args:
            file_path: Ruta al archivo con contraseñas
            
        Returns:
            List[Tuple[str, bool, int]]: Lista de (contraseña, comprometida, veces encontrada)
        """
        results = []
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    password = line.strip()
                    if password:
                        compromised, count = self.check_password(password)
                        results.append((password, compromised, count))
        except Exception as e:
            self.logger.error(f"Error al leer archivo: {e}")
            raise
            
        return results

def main():
    import sys
    
    if len(sys.argv) != 2:
        print("Uso: python password_checker.py <archivo_contraseñas>")
        sys.exit(1)
        
    checker = PasswordChecker()
    file_path = sys.argv[1]
    
    try:
        results = checker.check_password_file(file_path)
        
        print("\nResultados de verificación:")
        print("-" * 50)
        for password, compromised, count in results:
            status = "COMPROMETIDA" if compromised else "SEGURA"
            print(f"Contraseña: {password}")
            print(f"Estado: {status}")
            if compromised:
                print(f"Veces encontrada: {count}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 