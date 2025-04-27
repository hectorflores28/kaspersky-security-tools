# Herramientas de Seguridad Kaspersky Business Hub

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Kaspersky](https://img.shields.io/badge/Kaspersky-Business_Hub-orange.svg)
![Nmap](https://img.shields.io/badge/Nmap-7.80+-green.svg)
![John](https://img.shields.io/badge/John_the_Ripper-1.9.0+-yellow.svg)
![Hydra](https://img.shields.io/badge/Hydra-9.3+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

Este proyecto tiene como objetivo documentar y analizar los conceptos, herramientas y técnicas aprendidas en los cursos de Kaspersky Business Hub, con un enfoque en la escalabilidad y automatización de procesos de seguridad.

## Objetivos
- Documentar implementaciones de seguridad
- Registrar ajustes y configuraciones necesarias
- Mantener un seguimiento de pendientes y mejoras
- Compilar información sobre herramientas de ciberseguridad
- Analizar casos prácticos y soluciones
- Desarrollar scripts de automatización
- Crear playbooks de respuesta a incidentes

## Áreas de Enfoque
- Seguridad en Active Directory
- Aspectos investigativos básicos
- Software malicioso
  - Análisis heurístico
  - Detección de anomalías
  - Análisis de procesos
  - Inyección de código
  - Redes de bots
  - Fuerza bruta
- Phishing y OSINT
- PuP y exploits
- Seguridad de servidores

## Herramientas Principales
- Process Hacker
- Process Explorer
- Event Log Explorer
- Autopsy
- ntopng
- Fiddler
- Autoruns
- FTK Imager
- LAPS (Local Administrator Password Solution)

## Scripts Desarrollados
Para una descripción detallada de cada script, consulta el [README de scripts](scripts/README.md).

### Análisis y Forense
- [vulnerability_analyzer.py](scripts/README.md#análisis-y-forense): Análisis de vulnerabilidades
- [advanced_malware_analyzer.py](scripts/README.md#análisis-y-forense): Análisis avanzado de malware
- [memory_analyzer.py](scripts/README.md#análisis-y-forense): Análisis de memoria
- [security_log_analyzer.py](scripts/README.md#análisis-y-forense): Análisis de logs
- [server_hardening.py](scripts/README.md#análisis-y-forense): Hardening de servidores
- [email_analyzer.py](scripts/README.md#análisis-y-forense): Análisis de correos
- [service_monitor.py](scripts/README.md#análisis-y-forense): Monitoreo de servicios

### Fuerza Bruta
- [john_brute.py](scripts/README.md#fuerza-bruta): Fuerza bruta con John the Ripper
- [hydra_brute.py](scripts/README.md#fuerza-bruta): Fuerza bruta con Hydra

### Escaneo de Redes
- [nmap_scan.py](scripts/README.md#escaneo-de-redes): Script base de Nmap
- [nmap_quick.py](scripts/README.md#escaneo-de-redes): Escaneo rápido
- [nmap_completo.py](scripts/README.md#escaneo-de-redes): Escaneo completo
- [nmap_os.py](scripts/README.md#escaneo-de-redes): Detección de SO

### Detección de Amenazas
- [detector_malware.py](scripts/README.md#detección-de-amenazas): Detector básico de malware
- [malware_detector.py](scripts/README.md#detección-de-amenazas): Detector avanzado de malware

### Monitoreo
- [monitor_procesos.py](scripts/README.md#monitoreo): Monitoreo de procesos

### Utilidades
- [dir_enum.py](scripts/README.md#utilidades): Enumeración de directorios
- [port_scanner.py](scripts/README.md#utilidades): Escáner de puertos
- [subdomain_enum.py](scripts/README.md#utilidades): Enumeración de subdominios
- [log_analyzer.py](scripts/README.md#utilidades): Análisis de logs

## Estructura del Proyecto
- `documentacion/`: Guías y manuales
  - `malware/`: Documentación sobre software malicioso
- `scripts/`: Scripts de automatización
  - `utilidades/`: Scripts de utilidad
    - `malware_detector.py`
    - `log_analyzer.py`
    - `port_scanner.py`
    - `dir_enum.py`
    - `subdomain_enum.py`
  - `analisis/`: Scripts de análisis
    - `email_analyzer.py`
    - `vulnerability_analyzer.py`
    - `memory_analyzer.py`
    - `security_log_analyzer.py`
    - `server_hardening.py`
  - `brute_force/`: Scripts de fuerza bruta
    - `john_brute.py`
    - `hydra_brute.py`
  - `scanning/`: Scripts de escaneo
    - `nmap_scan.py`
    - `nmap_quick.py`
    - `nmap_completo.py`
    - `nmap_os.py`
  - `monitoring/`: Scripts de monitoreo
    - `monitor_procesos.py`
  - `detection/`: Scripts de detección
    - `detector_malware.py`
- `playbooks/`: Playbooks de respuesta a incidentes
- `herramientas/`: Herramientas personalizadas
- `casos/`: Casos de estudio y análisis
- `logs/`: Registros y análisis

## Estado Actual
- ✅ Seguridad en Active Directory (Completado)
- ✅ Aspectos Investigativos Básicos (Completado)
- ✅ Software Malicioso (Completado)
  - ✅ Análisis heurístico
  - ✅ Detección de anomalías
  - ✅ Análisis de procesos
  - ✅ Inyección de código
  - ✅ Redes de bots
  - ✅ Fuerza bruta
- ✅ Phishing y OSINT (Completado)
  - ✅ Script de análisis de correos
  - ✅ Detección de indicadores de phishing
- ✅ PuP y Exploits (Completado)
  - ✅ Script de análisis de vulnerabilidades
  - ✅ Detección de exploits conocidos
- 🔄 Seguridad de Servidores (En progreso)
  - ✅ Script de análisis de memoria
  - ⏳ Scripts de hardening
  - ⏳ Monitoreo de servicios

## Próximos Pasos
1. Desarrollar scripts de hardening para servidores
2. Implementar sistema de monitoreo de servicios
3. Crear playbooks de respuesta a incidentes
4. Desarrollar sistema de monitoreo de red con ntopng
5. Crear base de datos de firmas de malware

## Contribución
Las contribuciones son bienvenidas. Por favor, asegúrate de:
1. Seguir las guías de estilo
2. Documentar los cambios
3. Probar las modificaciones
4. Actualizar la documentación correspondiente

## Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.