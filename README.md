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

## Scripts Desarrollados

Para una descripción detallada de cada script, consulta el [README de scripts](scripts/README.md).

### Seguridad en Active Directory
- [laps_manager.py](scripts/ad/laps_manager.py): Gestión de contraseñas con LAPS
- [password_checker.py](scripts/ad/password_checker.py): Verificación de contraseñas con Have I Been Pwned
- [ad_auditor.py](scripts/ad/ad_auditor.py): Auditoría de Active Directory con PingCastle
- [admin_account_manager.py](scripts/ad/admin_account_manager.py): Gestión de cuentas de administrador local
- [pass_the_hash_detector.py](scripts/ad/pass_the_hash_detector.py): Detección de intentos de pass-the-hash

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
- [disk_analyzer.py](scripts/analisis/disk_analyzer.py): Análisis forense de discos duros
- [event_log_analyzer.py](scripts/analisis/event_log_analyzer.py): Análisis de registros de Windows
- [netflow_analyzer.py](scripts/analisis/netflow_analyzer.py): Análisis de tráfico de red
- [timeline_builder.py](scripts/analisis/timeline_builder.py): Construcción de líneas de tiempo
- [user_activity_analyzer.py](scripts/analisis/user_activity_analyzer.py): Análisis de actividad de usuarios

### Phishing y OSINT
- [phishing_detector.py](scripts/phishing/phishing_detector.py): Detecta intentos de phishing en correos electrónicos
- [url_analyzer.py](scripts/phishing/url_analyzer.py): Analiza URLs maliciosas
- [osint_tools.py](scripts/osint/osint_tools.py): Herramientas de inteligencia de código abierto
- [dns_analyzer.py](scripts/osint/dns_analyzer.py): Analiza registros DNS y propagación
- [social_media_analyzer.py](scripts/osint/social_media_analyzer.py): Analiza presencia en redes sociales
- [leak_detector.py](scripts/osint/leak_detector.py): Detecta filtraciones de información
- [email_header_analyzer.py](scripts/phishing/email_header_analyzer.py): Analiza encabezados de correo
- [spf_dkim_verifier.py](scripts/phishing/spf_dkim_verifier.py): Verifica configuraciones SPF y DKIM
- [phishing_campaign_analyzer.py](scripts/phishing/phishing_campaign_analyzer.py): Analiza campañas de phishing
- [infrastructure_analyzer.py](scripts/phishing/infrastructure_analyzer.py): Analiza infraestructura maliciosa
- [osint_audit.py](scripts/osint/osint_audit.py): Realiza auditorías de seguridad con OSINT

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
- [malware_detector.py](scripts/detection/malware_detector.py): Detector avanzado de malware

### Monitoreo
- [monitor_procesos.py](scripts/monitoring/monitor_procesos.py): Monitoreo de procesos

### Utilidades
- [dir_enum.py](scripts/utilidades/dir_enum.py): Enumeración de directorios
- [port_scanner.py](scripts/utilidades/port_scanner.py): Escáner de puertos
- [subdomain_enum.py](scripts/utilidades/subdomain_enum.py): Enumeración de subdominios
- [log_analyzer.py](scripts/utilidades/log_analyzer.py): Análisis de logs

### PUP y Exploits
- [document_analyzer.py](scripts/pup/document_analyzer.py): Analiza documentos maliciosos
- [exploit_detector.py](scripts/pup/exploit_detector.py): Detecta exploits
- [kit_analyzer.py](scripts/pup/kit_analyzer.py): Analiza kits de exploits
- [behavior_analyzer.py](scripts/pup/behavior_analyzer.py): Analiza comportamiento de malware
- [riskware_detector.py](scripts/pup/riskware_detector.py): Detecta riskware
- [adware_remover.py](scripts/pup/adware_remover.py): Elimina adware
- [sandbox_analyzer.py](scripts/pup/sandbox_analyzer.py): Analiza malware en entornos de prueba
- [vm_detector.py](scripts/pup/vm_detector.py): Detecta máquinas virtuales
- [hash_analyzer.py](scripts/pup/hash_analyzer.py): Analiza hashes de archivos
- [process_monitor.py](scripts/pup/process_monitor.py): Monitorea procesos

### Seguridad de Servidores
- [perimeter_analyzer.py](scripts/server/perimeter_analyzer.py): Analiza el perímetro de red
- [service_monitor.py](scripts/server/service_monitor.py): Monitorea servicios críticos
- [firewall_config.py](scripts/server/firewall_config.py): Configura reglas de firewall
- [app_control.py](scripts/server/app_control.py): Control de aplicaciones permitidas
- [event_monitor.py](scripts/server/event_monitor.py): Monitorea eventos de seguridad
- [network_analyzer.py](scripts/server/network_analyzer.py): Analiza la red interna
- [vulnerability_scanner.py](scripts/server/vulnerability_scanner.py): Escanea vulnerabilidades
- [service_detector.py](scripts/server/service_detector.py): Detecta servicios no estándar
- [attack_prevention.py](scripts/server/attack_prevention.py): Prevención de ataques externos
- [security_hardening.py](scripts/server/security_hardening.py): Hardening de servidores

## Estructura del Proyecto
```
kaspersky-security-tools/
├── documentacion/          # Documentación detallada
│   ├── analisis/          # Guías de análisis
│   ├── herramientas/      # Manuales de herramientas
│   ├── playbooks/         # Procedimientos y guías
│   └── casos/            # Casos de estudio
├── scripts/               # Scripts de automatización
│   ├── ad/               # Scripts de Active Directory
│   ├── analisis/         # Scripts de análisis
│   ├── brute_force/      # Scripts de fuerza bruta
│   ├── detection/        # Scripts de detección
│   ├── monitoring/       # Scripts de monitoreo
│   ├── osint/            # Scripts de OSINT
│   ├── phishing/         # Scripts de phishing
│   ├── pup/              # Scripts de PUP y exploits
│   ├── scanning/         # Scripts de escaneo
│   ├── server/           # Scripts de seguridad de servidores
│   └── utilidades/       # Herramientas auxiliares
├── playbooks/            # Playbooks de respuesta
│   ├── incidentes/       # Respuesta a incidentes
│   ├── forense/         # Análisis forense
│   └── monitoreo/       # Procedimientos de monitoreo
├── herramientas/         # Herramientas personalizadas
│   ├── analisis/        # Herramientas de análisis
│   ├── monitoreo/       # Herramientas de monitoreo
│   └── seguridad/       # Herramientas de seguridad
├── casos/               # Casos de estudio
│   ├── malware/        # Casos de malware
│   ├── phishing/       # Casos de phishing
│   └── forense/        # Casos forenses
├── logs/               # Registros y logs
│   ├── analisis/      # Logs de análisis
│   ├── monitoreo/     # Logs de monitoreo
│   └── errores/       # Registros de errores
├── config/            # Archivos de configuración
│   ├── herramientas/  # Configuración de herramientas
│   └── scripts/       # Configuración de scripts
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

## Próximos Pasos
1. Desarrollar scripts de hardening para servidores
2. Implementar sistema de monitoreo de servicios
3. Crear playbooks de respuesta a incidentes
4. Desarrollar sistema de monitoreo de red con ntopng
5. Crear base de datos de firmas de malware
6. Mejorar capacidades de detección de phishing
7. Expandir herramientas de OSINT

## Contribución
Las contribuciones son bienvenidas. Por favor, asegúrate de:
1. Seguir las guías de estilo
2. Documentar los cambios
3. Probar las modificaciones
4. Actualizar la documentación correspondiente

## Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.
