# Scripts de Automatización

Este directorio contiene los scripts de automatización para diversas tareas de ciberseguridad. Para una visión general del proyecto, consulta el [README principal](../README.md).

## Estructura

```
scripts/
├── utilidades/           # Utilidades comunes
│   └── common.py        # Módulo de utilidades compartidas
├── phishing/            # Scripts de phishing
│   ├── phishing_detector.py
│   └── url_analyzer.py
└── osint/               # Scripts de OSINT
    ├── osint_tools.py
    ├── dns_analyzer.py
    ├── social_media_analyzer.py
    └── leak_detector.py
```

## Utilidades Comunes

El módulo `common.py` proporciona funcionalidades básicas utilizadas por todos los scripts:

### Configuración
```python
from scripts.utilidades.common import Config

# Cargar configuración
config = Config()
value = config.get("seccion.clave", "valor_por_defecto")
```

### Logging
```python
from scripts.utilidades.common import Logger

# Configurar logging
logger = Logger("mi_script").get_logger()
logger.info("Mensaje informativo")
logger.error("Mensaje de error")
```

### Análisis de Archivos
```python
from scripts.utilidades.common import FileAnalyzer

# Calcular hash
hash_value = FileAnalyzer.get_file_hash("archivo.txt")

# Obtener tipo de archivo
file_type = FileAnalyzer.get_file_type("archivo.txt")

# Obtener metadatos
metadata = FileAnalyzer.get_file_metadata("archivo.txt")
```

### Utilidades de Red
```python
from scripts.utilidades.common import NetworkUtils

# Verificar puerto
is_open = NetworkUtils.is_port_open("localhost", 80)

# Obtener IP pública
public_ip = NetworkUtils.get_public_ip()
```

### Generación de Reportes
```python
from scripts.utilidades.common import ReportGenerator

# Generar reporte
generator = ReportGenerator()
report_path = generator.generate_report({"data": "value"}, "mi_reporte")
```

## Scripts de Phishing

### phishing_detector.py
```python
from scripts.phishing.phishing_detector import PhishingDetector

# Analizar correo electrónico
detector = PhishingDetector()
result = detector.analyze_email("correo.eml")

# Verificar indicadores de phishing
if result.is_phishing:
    print(f"Correo detectado como phishing: {result.reason}")
```

### url_analyzer.py
```python
from scripts.phishing.url_analyzer import URLAnalyzer

# Analizar URL
analyzer = URLAnalyzer()
result = analyzer.analyze_url("https://ejemplo.com")

# Verificar si es maliciosa
if result.is_malicious:
    print(f"URL maliciosa detectada: {result.threat_type}")
```

## Scripts de OSINT

### osint_tools.py
```python
from scripts.osint.osint_tools import OSINTTools

# Inicializar herramientas OSINT
tools = OSINTTools()

# Buscar información de dominio
domain_info = tools.search_domain("ejemplo.com")

# Analizar redes sociales
social_info = tools.analyze_social_media("usuario")
```

### dns_analyzer.py
```python
from scripts.osint.dns_analyzer import DNSAnalyzer

# Analizar registros DNS
analyzer = DNSAnalyzer()
records = analyzer.get_dns_records("ejemplo.com")

# Verificar propagación
propagation = analyzer.check_propagation("ejemplo.com")
```

### social_media_analyzer.py
```python
from scripts.osint.social_media_analyzer import SocialMediaAnalyzer

# Analizar presencia en redes sociales
analyzer = SocialMediaAnalyzer()
profiles = analyzer.find_profiles("usuario")

# Analizar actividad
activity = analyzer.analyze_activity("usuario")
```

### leak_detector.py
```python
from scripts.osint.leak_detector import LeakDetector

# Verificar filtraciones
detector = LeakDetector()
leaks = detector.check_leaks("usuario@ejemplo.com")

# Analizar impacto
impact = detector.analyze_impact(leaks)
```

## Desarrollo de Nuevos Scripts

Al desarrollar nuevos scripts, se recomienda:

1. Utilizar las utilidades comunes proporcionadas
2. Seguir las guías de estilo del proyecto
3. Incluir pruebas unitarias
4. Documentar el código
5. Manejar errores apropiadamente
6. Usar el sistema de logging

### Ejemplo de Script

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Nombre del Script
Descripción detallada del script
"""

from scripts.utilidades.common import Config, Logger, FileAnalyzer

def main():
    # Configuración
    config = Config()
    logger = Logger("mi_script").get_logger()
    
    try:
        # Lógica del script
        logger.info("Iniciando script")
        
        # Ejemplo de uso de utilidades
        metadata = FileAnalyzer.get_file_metadata("archivo.txt")
        logger.info(f"Metadatos: {metadata}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## Próximos Pasos

1. Desarrollar scripts específicos para cada área:
   - Análisis forense
   - Monitoreo de red
   - Detección de malware
   - Escaneo de vulnerabilidades
   - Detección de phishing
   - Herramientas OSINT

2. Implementar pruebas unitarias para cada script

3. Crear documentación detallada de uso

4. Desarrollar una interfaz de línea de comandos unificada 