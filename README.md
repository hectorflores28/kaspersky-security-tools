# Herramientas de Seguridad Kaspersky Business Hub

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Kaspersky](https://img.shields.io/badge/Kaspersky-Business_Hub-orange.svg)
![Nmap](https://img.shields.io/badge/Nmap-7.80+-green.svg)
![John](https://img.shields.io/badge/John_the_Ripper-1.9.0+-yellow.svg)
![Hydra](https://img.shields.io/badge/Hydra-9.3+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

Este proyecto tiene como objetivo documentar y analizar los conceptos, herramientas y técnicas aprendidas en los cursos de Kaspersky Business Hub, con un enfoque en la escalabilidad y automatización de procesos de seguridad.

## Índice
1. [Objetivos](#objetivos)
2. [Áreas de Enfoque](#áreas-de-enfoque)
3. [Herramientas Principales](#herramientas-principales)
4. [Scripts Desarrollados](#scripts-desarrollados)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Estado Actual](#estado-actual)
7. [Próximos Pasos](#próximos-pasos)
8. [Contribución](#contribución)
9. [Licencia](#licencia)

## Objetivos
- Documentar implementaciones de seguridad
- Registrar ajustes y configuraciones necesarias
- Mantener un seguimiento de pendientes y mejoras
- Compilar información sobre herramientas de ciberseguridad
- Analizar casos prácticos y soluciones
- Desarrollar scripts de automatización
- Crear playbooks de respuesta a incidentes

## Áreas de Enfoque

### 1. Seguridad en Active Directory
- Implementación de LAPS (Local Administrator Password Solution)
- Auditoría con PingCastle
- Verificación de contraseñas con Have I Been Pwned
- Cumplimiento con NIST 800-63B
- Gestión de cuentas de administrador local
- Prevención de pass-the-hash

### 2. Aspectos Investigativos Básicos
- Investigación forense digital
- Análisis de memoria RAM y disco duro
- Análisis de registros de Windows
- Análisis de tráfico de red con Netflow
- Identificación de usuarios y actividad
- Análisis de sistema de archivos
- Construcción de líneas de tiempo

### 3. Software Malicioso
- Análisis heurístico
- Detección de anomalías
- Análisis de procesos
- Inyección de código
- Redes de bots
- Fuerza bruta

### 4. Phishing y OSINT
- Detección de phishing por correo electrónico
- Análisis de enlaces maliciosos
- Inteligencia de código abierto
- Auditorías de seguridad con OSINT
- Análisis de encabezados de correo
- Verificación de SPF y DKIM
- Detección de campañas de phishing
- Análisis de infraestructura maliciosa
- Herramientas de OSINT (Recon-ng, Shodan)
- Verificación de URLs y dominios

### 5. PuP y Exploits
- Análisis de documentos maliciosos
- Detección de exploits
- Análisis de kits de exploits
- Medidas preventivas
- Análisis de comportamiento
- Detección de riskware
- Análisis de adware
- Herramientas de análisis automático
- Entornos de prueba
- Detección de máquinas virtuales

### 6. Seguridad de Servidores
- Protección del perímetro
- Análisis de red interna
- Control de aplicaciones
- Configuración de firewall
- Monitoreo de eventos
- Detección de servicios no estándar
- Prevención de ataques externos
- Hardening de servidores
- Gestión de vulnerabilidades
- Higiene cibernética

## Herramientas Principales

### Análisis
- Process Hacker
- Process Explorer
- Event Log Explorer
- Autopsy
- FTK Imager

### Monitoreo
- ntopng
- Zabbix
- Wireshark
- Fiddler

### Seguridad
- LAPS
- PingCastle
- Autoruns
- YARA

### OSINT
- Recon-ng
- Shodan
- BuiltWith
- HackerTarget

### Seguridad en Active Directory
- [password_checker.py](scripts/ad/password_checker.py): Verificación de contraseñas con Have I Been Pwned

### Análisis y Forense
- [file_system_analyzer.py](scripts/analisis/file_system_analyzer.py): Analiza el sistema de archivos en busca de indicadores de compromiso
- [registry_analyzer.py](scripts/analisis/registry_analyzer.py): Analiza el registro de Windows en busca de actividad maliciosa
- [network_traffic_analyzer.py](scripts/analisis/network_traffic_analyzer.py): Analiza el tráfico de red en busca de patrones sospechosos
- [service_monitor.py](scripts/analisis/service_monitor.py): Monitorea servicios en servidores Windows
- [server_hardening.py](scripts/analisis/server_hardening.py): Verifica y aplica configuraciones de seguridad en servidores
- [vulnerability_analyzer.py](scripts/analisis/vulnerability_analyzer.py): Analiza sistemas en busca de vulnerabilidades
- [email_analyzer.py](scripts/analisis/email_analyzer.py): Analiza correos electrónicos en busca de phishing
- [advanced_malware_analyzer.py](scripts/analisis/advanced_malware_analyzer.py): Analizador avanzado de malware
- [security_log_analyzer.py](scripts/analisis/security_log_analyzer.py): Analiza logs de seguridad
- [memory_analyzer.py](scripts/analisis/memory_analyzer.py): Analiza volcados de memoria
- [event_log_analyzer.py](scripts/analisis/event_log_analyzer.py): Análisis de registros de Windows

### Phishing y OSINT
- [phishing_analyzer.py](scripts/phishing/phishing_analyzer.py): Realiza auditorías incluyendo detección de URLs sospechosas y análisis de contenido de correos electrónicos.

### Fuerza Bruta
- [john_brute.py](scripts/brute_force/john_brute.py): Fuerza bruta con John the Ripper
- [hydra_brute.py](scripts/brute_force/hydra_brute.py): Fuerza bruta con Hydra

### Escaneo de Redes
- [nmap_scan.py](scripts/scanning/nmap_scan.py): Script base de Nmap
- [nmap_quick.py](scripts/scanning/nmap_quick.py): Escaneo rápido
- [nmap_completo.py](scripts/scanning/nmap_completo.py): Escaneo completo
- [nmap_os.py](scripts/scanning/nmap_os.py): Detección de SO

### Detección de Amenazas
- [detector_malware.py](scripts/detection/detector_malware.py): Detector básico de malware

### Monitoreo
- [monitor_procesos.py](scripts/monitoring/monitor_procesos.py): Monitoreo de procesos

### Utilidades
- [dir_enum.py](scripts/utilidades/dir_enum.py): Enumeración de directorios
- [port_scanner.py](scripts/utilidades/port_scanner.py): Escáner de puertos
- [subdomain_enum.py](scripts/utilidades/subdomain_enum.py): Enumeración de subdominios
- [log_analyzer.py](scripts/utilidades/log_analyzer.py): Análisis de logs

### Seguridad de Servidores
- [perimeter_analyzer.py](scripts/server/perimeter_analyzer.py): Analiza el perímetro de red
- [service_monitor.py](scripts/server/service_monitor.py): Monitorea servicios críticos
- [firewall_config.py](scripts/server/firewall_config.py): Configura reglas de firewall
- [app_control.py](scripts/server/app_control.py): Control de aplicaciones permitidas

### Web-Scrapping
- [qanda.py](scripts/web_scrapping/qanda.py): Web Scrapping utilizando Qanda

## Estructura del Proyecto
```
kaspersky-security-tools/
├── documentacion/          # Documentación detallada
│   ├── active_directory/  # Seguridad de Active Directory
│   ├── exploits/          # Exploits
│   ├── investigación/     # Investigación Forense
│   ├── malware/           # Software Malicioso
│   ├── phishing/          # Phishing OSINT
│   └── servidores/        # Seguridad de Servidores
├── scripts/               # Scripts de automatización
│   ├── ad/               # Scripts de Active Directory
│   ├── analisis/         # Scripts de Análisis
│   ├── brute_force/      # Scripts de Fuerza Bruta
│   ├── detection/        # Scripts de Detección
│   ├── monitoring/       # Scripts de Monitoreo
│   ├── phishing/         # Scripts de Phishing
│   ├── scanning/         # Scripts de Escaneo
│   ├── server/           # Scripts de Seguridad de servidores
│   ├── utilidades/       # Herramientas auxiliares
│   └── web_scrapping/    # Herramientas de analisis web
├── config/            # Archivos de configuración
└── tests/            # Pruebas y validaciones
    ├── unitarios/    # Pruebas unitarias
    └── integracion/  # Pruebas de integración
```

## Estado Actual
- ✅ Seguridad en Active Directory (Completado)
- ✅ Aspectos Investigativos Básicos (Completado)
- ✅ Software Malicioso (Completado)
- ✅ Phishing y OSINT (Completado)
- ✅ PuP y Exploits (Completado)
- ✅ Seguridad de Servidores (Completado)

## Contribución
Las contribuciones son bienvenidas. Por favor, asegúrate de:
1. Seguir las guías de estilo
2. Documentar los cambios
3. Probar las modificaciones
4. Actualizar la documentación correspondiente

## Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.
