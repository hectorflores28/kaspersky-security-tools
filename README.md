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
  - Implementación de LAPS (Local Administrator Password Solution)
  - Auditoría con PingCastle
  - Verificación de contraseñas con Have I Been Pwned
  - Cumplimiento con NIST 800-63B
  - Gestión de cuentas de administrador local
  - Prevención de pass-the-hash
- Aspectos investigativos básicos
  - Investigación forense digital
  - Análisis de memoria RAM y disco duro
  - Análisis de registros de Windows
  - Análisis de tráfico de red con Netflow
  - Identificación de usuarios y actividad
  - Análisis de sistema de archivos
  - Construcción de líneas de tiempo
- Software malicioso
  - Análisis heurístico
  - Detección de anomalías
  - Análisis de procesos
  - Inyección de código
  - Redes de bots
  - Fuerza bruta
- Phishing y OSINT
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
- PuP y exploits
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
- PingCastle
- Have I Been Pwned API
- CyberChef
- Recon-ng (OSINT)
- Shodan
- BuiltWith
- HackerTarget
- FreeGeoIP
- Belkasoft Live RAM Capturer
- Sleuth Kit
- Netflow Analyzer
- PhishTank
- VirusTotal
- TrueURL
- DNS Checker
- WhatsMyDNS
- Site24x7 DNS Tools
- Process Monitor
- AVZ
- Cuckoo Sandbox
- Malwr.com
- Hashdeep
- Wireshark
- IDA Pro
- OllyDbg
- x64dbg

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
- `documentacion/`: Guías y manuales
  - `malware/`: Documentación sobre software malicioso
  - `phishing/`: Documentación sobre phishing y OSINT
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
  - `phishing/`: Scripts de phishing
    - `phishing_detector.py`
    - `url_analyzer.py`
  - `osint/`: Scripts de OSINT
    - `osint_tools.py`
    - `dns_analyzer.py`
    - `social_media_analyzer.py`
    - `leak_detector.py`
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
  - `pup/`: Scripts de PUP y exploits
    - `document_analyzer.py`
    - `exploit_detector.py`
    - `kit_analyzer.py`
    - `behavior_analyzer.py`
    - `riskware_detector.py`
    - `adware_remover.py`
    - `sandbox_analyzer.py`
    - `vm_detector.py`
    - `hash_analyzer.py`
    - `process_monitor.py`

## Estado Actual
- ✅ Seguridad en Active Directory (Completado)
  - ✅ Implementación de LAPS
  - ✅ Auditoría con PingCastle
  - ✅ Verificación de contraseñas con Have I Been Pwned
  - ✅ Cumplimiento con NIST 800-63B
  - ✅ Gestión de cuentas de administrador local
  - ✅ Prevención de pass-the-hash
- ✅ Aspectos Investigativos Básicos (Completado)
  - ✅ Investigación forense digital
  - ✅ Análisis de memoria y disco
  - ✅ Análisis de registros de Windows
  - ✅ Análisis de tráfico de red
  - ✅ Identificación de usuarios
  - ✅ Análisis de sistema de archivos
  - ✅ Construcción de líneas de tiempo
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
  - ✅ Herramientas de OSINT
  - ✅ Análisis de URLs maliciosas
  - ✅ Detección de filtraciones
- ✅ PuP y Exploits (Completado)
  - ✅ Script de análisis de vulnerabilidades
  - ✅ Detección de exploits conocidos
- 🔄 Seguridad de Servidores (En progreso)
  - ✅ Script de análisis de memoria
  - ✅ Scripts de hardening
  - ✅ Monitoreo de servicios
  - ✅ Protección del perímetro
  - ✅ Análisis de red interna
  - ✅ Control de aplicaciones
  - ✅ Configuración de firewall
  - ✅ Monitoreo de eventos
  - ✅ Detección de servicios no estándar
  - ✅ Prevención de ataques externos

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