# Scripts de Automatización

Este directorio contiene los scripts de automatización para diversas tareas de ciberseguridad. Para una visión general del proyecto, consulta el [README principal](../README.md).

## Estructura

```
scripts/
└── utilidades/           # Utilidades comunes
    └── common.py        # Módulo de utilidades compartidas
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

2. Implementar pruebas unitarias para cada script

3. Crear documentación detallada de uso

4. Desarrollar una interfaz de línea de comandos unificada 