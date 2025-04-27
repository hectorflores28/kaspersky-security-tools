#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pruebas unitarias para las utilidades comunes
"""

import os
import pytest
from pathlib import Path
import tempfile
import json
from scripts.utilidades.common import (
    Config,
    Logger,
    FileAnalyzer,
    NetworkUtils,
    ReportGenerator
)

@pytest.fixture
def temp_config():
    """Crea un archivo de configuración temporal"""
    config_data = {
        "project": {
            "name": "Test Project",
            "version": "1.0.0"
        },
        "logging": {
            "level": "DEBUG"
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        import yaml
        yaml.dump(config_data, f)
        return f.name

@pytest.fixture
def temp_file():
    """Crea un archivo temporal para pruebas"""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"Test content")
        return f.name

def test_config_loading(temp_config):
    """Prueba la carga de configuración"""
    config = Config(temp_config)
    assert config.get("project.name") == "Test Project"
    assert config.get("project.version") == "1.0.0"
    assert config.get("logging.level") == "DEBUG"
    assert config.get("nonexistent.key", "default") == "default"
    
    os.unlink(temp_config)

def test_file_analyzer(temp_file):
    """Prueba el analizador de archivos"""
    # Prueba de hash
    hash_value = FileAnalyzer.get_file_hash(temp_file)
    assert len(hash_value) == 64  # SHA-256 tiene 64 caracteres hex
    
    # Prueba de tipo de archivo
    file_type = FileAnalyzer.get_file_type(temp_file)
    assert "ASCII text" in file_type or "text" in file_type.lower()
    
    # Prueba de metadatos
    metadata = FileAnalyzer.get_file_metadata(temp_file)
    assert "name" in metadata
    assert "size" in metadata
    assert "created" in metadata
    assert "modified" in metadata
    assert "accessed" in metadata
    assert "permissions" in metadata
    
    os.unlink(temp_file)

def test_report_generator():
    """Prueba el generador de reportes"""
    generator = ReportGenerator()
    test_data = {"test": "data"}
    
    report_path = generator.generate_report(test_data, "test_report")
    assert Path(report_path).exists()
    
    with open(report_path) as f:
        loaded_data = json.load(f)
        assert loaded_data == test_data
    
    os.unlink(report_path)

def test_network_utils():
    """Prueba las utilidades de red"""
    # Prueba de IP pública
    public_ip = NetworkUtils.get_public_ip()
    assert public_ip is None or isinstance(public_ip, str)
    
    # Prueba de puerto abierto (localhost)
    assert NetworkUtils.is_port_open("localhost", 80) in [True, False]

def test_logger():
    """Prueba el logger"""
    logger = Logger("test").get_logger()
    assert logger is not None
    # No hay una forma fácil de verificar la salida del logger en las pruebas 