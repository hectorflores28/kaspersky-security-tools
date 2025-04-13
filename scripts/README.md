# Scripts de Automatización

Este directorio contiene los scripts de automatización para diversas tareas de ciberseguridad. Para una visión general del proyecto, consulta el [README principal](../README.md).

## Estructura

- `monitoring/`: Scripts para monitoreo de sistemas y redes
- `analisis/`: Scripts para análisis forense y de seguridad
- `automation/`: Scripts para automatización de tareas
- `utilidades/`: Scripts de utilidad general
- `brute_force/`: Scripts para ataques de fuerza bruta
- `scanning/`: Scripts para escaneo de redes y sistemas
- `detection/`: Scripts para detección de amenazas

## Scripts Disponibles

### Análisis y Forense
- [vulnerability_analyzer.py](analisis/vulnerability_analyzer.py): Analiza sistemas en busca de vulnerabilidades conocidas, incluyendo análisis de puertos, servicios y configuraciones
- [advanced_malware_analyzer.py](analisis/advanced_malware_analyzer.py): Analizador avanzado de malware con reglas YARA, análisis estático y dinámico
- [memory_analyzer.py](analisis/memory_analyzer.py): Analiza volcados de memoria en busca de indicadores de compromiso y procesos maliciosos
- [security_log_analyzer.py](analisis/security_log_analyzer.py): Analiza logs de seguridad en busca de patrones sospechosos y eventos de seguridad
- [server_hardening.py](analisis/server_hardening.py): Verifica y aplica configuraciones de seguridad en servidores Windows
- [email_analyzer.py](analisis/email_analyzer.py): Analiza correos electrónicos en busca de patrones de phishing y malware
- [service_monitor.py](analisis/service_monitor.py): Monitorea servicios y procesos en sistemas Windows

### Fuerza Bruta
- [john_brute.py](brute_force/john_brute.py): Realiza ataques de fuerza bruta con John the Ripper en archivos de hashes
  - Soporte para múltiples formatos de hash
  - Uso de wordlists personalizadas
  - Identificación automática de formato
- [hydra_brute.py](brute_force/hydra_brute.py): Realiza ataques de fuerza bruta con Hydra en diferentes servicios
  - Soporte para SSH, FTP, HTTP, HTTPS, SMB, RDP, Telnet
  - Configuración flexible de parámetros
  - Monitoreo en tiempo real

### Escaneo de Redes
- [nmap_scan.py](scanning/nmap_scan.py): Script base para escaneos con Nmap, proporciona funcionalidad común
  - Manejo de resultados en XML
  - Logging detallado
  - Interfaz unificada
- [nmap_quick.py](scanning/nmap_quick.py): Escaneo rápido de puertos y servicios
  - Top 100 puertos
  - Modo sigiloso
  - Resultados rápidos
- [nmap_completo.py](scanning/nmap_completo.py): Escaneo exhaustivo de puertos, servicios y vulnerabilidades
  - Escaneo de todos los puertos
  - Detección de servicios
  - Análisis de vulnerabilidades
- [nmap_os.py](scanning/nmap_os.py): Detección de sistema operativo
  - Fingerprinting de SO
  - Detección de versión
  - Análisis de servicios

### Detección de Amenazas
- [detector_malware.py](detection/detector_malware.py): Detector básico de malware con análisis de firmas y comportamiento
- [malware_detector.py](utilidades/malware_detector.py): Detector avanzado de malware con análisis heurístico

### Monitoreo
- [monitor_procesos.py](monitoring/monitor_procesos.py): Monitorea procesos en ejecución y detecta anomalías
  - Monitoreo en tiempo real
  - Detección de procesos sospechosos
  - Alertas configurables

### Utilidades
- [dir_enum.py](utilidades/dir_enum.py): Enumeración de directorios web con soporte para wordlists
- [port_scanner.py](utilidades/port_scanner.py): Escáner básico de puertos con detección de servicios
- [subdomain_enum.py](utilidades/subdomain_enum.py): Enumeración de subdominios con verificación de existencia
- [log_analyzer.py](utilidades/log_analyzer.py): Analizador de logs con detección de patrones sospechosos

## Requisitos

Los scripts requieren las siguientes dependencias:
- Python 3.8+
- Dependencias listadas en [requirements.txt](utilidades/requirements.txt)
- Herramientas externas:
  - John the Ripper
  - Hydra
  - Nmap
  - YARA (para análisis de malware)
  - Volatility (para análisis de memoria)

## Uso

Cada script incluye su propia documentación y ejemplos de uso. Los scripts principales incluyen:

### John the Ripper
```bash
python john_brute.py archivo_hashes.txt --wordlist wordlist.txt
```

### Hydra
```bash
python hydra_brute.py target.com ssh wordlist.txt --username admin --port 22
```

### Nmap
```bash
# Escaneo rápido
python nmap_quick.py target.com

# Escaneo completo
python nmap_completo.py target.com

# Detección de SO
python nmap_os.py target.com
```

### Análisis de Malware
```bash
python advanced_malware_analyzer.py muestra.exe --rules reglas_yara
```

### Análisis de Logs
```bash
python security_log_analyzer.py security.log
```

## Contribución

1. Seguir las guías de estilo
2. Documentar los cambios
3. Probar las modificaciones
4. Actualizar la documentación 