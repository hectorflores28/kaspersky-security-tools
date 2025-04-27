#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utilidades comunes para el proyecto
Este módulo contiene funciones y clases utilizadas por múltiples scripts.
"""

import os
import sys
import json
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import hashlib
import magic
import requests
from rich.console import Console
from rich.logging import RichHandler
from loguru import logger

class Config:
    """Clase para manejar la configuración del proyecto"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Carga la configuración desde el archivo YAML"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error al cargar la configuración: {e}")
            return {}
            
    def get(self, key: str, default: Any = None) -> Any:
        """Obtiene un valor de configuración"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
                
        return value

class Logger:
    """Clase para manejar el logging del proyecto"""
    
    def __init__(self, name: str):
        self.name = name
        self._setup_logger()
        
    def _setup_logger(self):
        """Configura el logger con Rich"""
        logger.remove()
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="INFO"
        )
        
    def get_logger(self):
        """Retorna el logger configurado"""
        return logger.bind(name=self.name)

class FileAnalyzer:
    """Clase para análisis básico de archivos"""
    
    @staticmethod
    def get_file_hash(file_path: str, algorithm: str = "sha256") -> str:
        """Calcula el hash de un archivo"""
        hash_func = getattr(hashlib, algorithm)()
        
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
                
        return hash_func.hexdigest()
        
    @staticmethod
    def get_file_type(file_path: str) -> str:
        """Determina el tipo de archivo usando python-magic"""
        return magic.from_file(file_path)
        
    @staticmethod
    def get_file_metadata(file_path: str) -> Dict[str, Any]:
        """Obtiene metadatos básicos de un archivo"""
        path = Path(file_path)
        stat = path.stat()
        
        return {
            "name": path.name,
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
            "permissions": oct(stat.st_mode)[-3:]
        }

class NetworkUtils:
    """Clase para utilidades de red"""
    
    @staticmethod
    def is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
        """Verifica si un puerto está abierto"""
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        try:
            result = sock.connect_ex((host, port))
            return result == 0
        except Exception:
            return False
        finally:
            sock.close()
            
    @staticmethod
    def get_public_ip() -> Optional[str]:
        """Obtiene la IP pública"""
        try:
            response = requests.get('https://api.ipify.org?format=json')
            return response.json().get('ip')
        except Exception:
            return None

class ReportGenerator:
    """Clase para generar reportes"""
    
    def __init__(self, output_dir: str = "data/reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_report(self, data: Dict[str, Any], filename: str) -> str:
        """Genera un reporte en formato JSON"""
        report_path = self.output_dir / f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_path, 'w') as f:
            json.dump(data, f, indent=2)
            
        return str(report_path) 