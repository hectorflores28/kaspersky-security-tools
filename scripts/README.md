# Scripts de Automatización

Este directorio contiene los scripts de automatización para diversas tareas de ciberseguridad. Para una visión general del proyecto, consulta el [README principal](../README.md).

## Índice
1. [Estructura](#estructura)
2. [Utilidades Comunes](#utilidades-comunes)
3. [Scripts por Categoría](#scripts-por-categoría)
4. [Desarrollo de Nuevos Scripts](#desarrollo-de-nuevos-scripts)
5. [Próximos Pasos](#próximos-pasos)

## Estructura

```
scripts/
├── ad/               # Scripts de Active Directory
├── analisis/         # Scripts de análisis
├── brute_force/      # Scripts de fuerza bruta
├── detection/        # Scripts de detección
├── monitoring/       # Scripts de monitoreo
├── osint/            # Scripts de OSINT
├── phishing/         # Scripts de phishing
├── pup/              # Scripts de PUP y exploits
├── scanning/         # Scripts de escaneo
├── server/           # Scripts de seguridad de servidores
└── utilidades/       # Herramientas auxiliares
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

## Scripts por Categoría

### 1. Seguridad en Active Directory
- [laps_manager.py](ad/laps_manager.py): Gestión de contraseñas con LAPS
- [password_checker.py](ad/password_checker.py): Verificación de contraseñas con Have I Been Pwned
- [ad_auditor.py](ad/ad_auditor.py): Auditoría de Active Directory con PingCastle
- [admin_account_manager.py](ad/admin_account_manager.py): Gestión de cuentas de administrador local
- [pass_the_hash_detector.py](ad/pass_the_hash_detector.py): Detección de intentos de pass-the-hash

### 2. Análisis y Forense
- [file_system_analyzer.py](analisis/file_system_analyzer.py): Analiza el sistema de archivos en busca de indicadores de compromiso
- [registry_analyzer.py](analisis/registry_analyzer.py): Analiza el registro de Windows en busca de actividad maliciosa
- [network_traffic_analyzer.py](analisis/network_traffic_analyzer.py): Analiza el tráfico de red en busca de patrones sospechosos
- [service_monitor.py](analisis/service_monitor.py): Monitorea servicios en servidores Windows
- [server_hardening.py](analisis/server_hardening.py): Verifica y aplica configuraciones de seguridad en servidores
- [vulnerability_analyzer.py](analisis/vulnerability_analyzer.py): Analiza sistemas en busca de vulnerabilidades
- [email_analyzer.py](analisis/email_analyzer.py): Analiza correos electrónicos en busca de phishing
- [advanced_malware_analyzer.py](analisis/advanced_malware_analyzer.py): Analizador avanzado de malware
- [security_log_analyzer.py](analisis/security_log_analyzer.py): Analiza logs de seguridad
- [memory_analyzer.py](analisis/memory_analyzer.py): Analiza volcados de memoria
- [disk_analyzer.py](analisis/disk_analyzer.py): Análisis forense de discos duros
- [event_log_analyzer.py](analisis/event_log_analyzer.py): Análisis de registros de Windows
- [netflow_analyzer.py](analisis/netflow_analyzer.py): Análisis de tráfico de red
- [timeline_builder.py](analisis/timeline_builder.py): Construcción de líneas de tiempo
- [user_activity_analyzer.py](analisis/user_activity_analyzer.py): Análisis de actividad de usuarios

### 3. Phishing y OSINT
- [phishing_detector.py](phishing/phishing_detector.py): Detecta intentos de phishing en correos electrónicos
- [url_analyzer.py](phishing/url_analyzer.py): Analiza URLs maliciosas
- [osint_tools.py](osint/osint_tools.py): Herramientas de inteligencia de código abierto
- [dns_analyzer.py](osint/dns_analyzer.py): Analiza registros DNS y propagación
- [social_media_analyzer.py](osint/social_media_analyzer.py): Analiza presencia en redes sociales
- [leak_detector.py](osint/leak_detector.py): Detecta filtraciones de información
- [email_header_analyzer.py](phishing/email_header_analyzer.py): Analiza encabezados de correo
- [spf_dkim_verifier.py](phishing/spf_dkim_verifier.py): Verifica configuraciones SPF y DKIM
- [phishing_campaign_analyzer.py](phishing/phishing_campaign_analyzer.py): Analiza campañas de phishing
- [infrastructure_analyzer.py](phishing/infrastructure_analyzer.py): Analiza infraestructura maliciosa
- [osint_audit.py](osint/osint_audit.py): Realiza auditorías de seguridad con OSINT

### 4. Fuerza Bruta
- [john_brute.py](brute_force/john_brute.py): Fuerza bruta con John the Ripper
- [hydra_brute.py](brute_force/hydra_brute.py): Fuerza bruta con Hydra

### 5. Escaneo de Redes
- [nmap_scan.py](scanning/nmap_scan.py): Script base de Nmap
- [nmap_quick.py](scanning/nmap_quick.py): Escaneo rápido
- [nmap_completo.py](scanning/nmap_completo.py): Escaneo completo
- [nmap_os.py](scanning/nmap_os.py): Detección de SO

### 6. Detección de Amenazas
- [detector_malware.py](detection/detector_malware.py): Detector básico de malware
- [malware_detector.py](detection/malware_detector.py): Detector avanzado de malware

### 7. Monitoreo
- [monitor_procesos.py](monitoring/monitor_procesos.py): Monitoreo de procesos

### 8. Utilidades
- [dir_enum.py](utilidades/dir_enum.py): Enumeración de directorios
- [port_scanner.py](utilidades/port_scanner.py): Escáner de puertos
- [subdomain_enum.py](utilidades/subdomain_enum.py): Enumeración de subdominios
- [log_analyzer.py](utilidades/log_analyzer.py): Análisis de logs

### 9. PUP y Exploits
- [document_analyzer.py](pup/document_analyzer.py): Analiza documentos maliciosos
- [exploit_detector.py](pup/exploit_detector.py): Detecta exploits
- [kit_analyzer.py](pup/kit_analyzer.py): Analiza kits de exploits
- [behavior_analyzer.py](pup/behavior_analyzer.py): Analiza comportamiento de malware
- [riskware_detector.py](pup/riskware_detector.py): Detecta riskware
- [adware_remover.py](pup/adware_remover.py): Elimina adware
- [sandbox_analyzer.py](pup/sandbox_analyzer.py): Analiza malware en entornos de prueba
- [vm_detector.py](pup/vm_detector.py): Detecta máquinas virtuales
- [hash_analyzer.py](pup/hash_analyzer.py): Analiza hashes de archivos
- [process_monitor.py](pup/process_monitor.py): Monitorea procesos

### 10. Seguridad de Servidores
- [perimeter_analyzer.py](server/perimeter_analyzer.py): Analiza el perímetro de red
- [service_monitor.py](server/service_monitor.py): Monitorea servicios críticos
- [firewall_config.py](server/firewall_config.py): Configura reglas de firewall
- [app_control.py](server/app_control.py): Control de aplicaciones permitidas
- [event_monitor.py](server/event_monitor.py): Monitorea eventos de seguridad
- [network_analyzer.py](server/network_analyzer.py): Analiza la red interna
- [vulnerability_scanner.py](server/vulnerability_scanner.py): Escanea vulnerabilidades
- [service_detector.py](server/service_detector.py): Detecta servicios no estándar
- [attack_prevention.py](server/attack_prevention.py): Prevención de ataques externos
- [security_hardening.py](server/security_hardening.py): Hardening de servidores

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