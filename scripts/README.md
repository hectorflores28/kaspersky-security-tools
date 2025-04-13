# Scripts de Automatización

Este directorio contiene los scripts de automatización para diversas tareas de ciberseguridad.

## Estructura

- `monitoreo/`: Scripts para monitoreo de sistemas y redes
- `analisis/`: Scripts para análisis forense y de seguridad
- `automatizacion/`: Scripts para automatización de tareas
- `utilidades/`: Scripts de utilidad general
- `brute_force/`: Scripts para ataques de fuerza bruta
- `scanning/`: Scripts para escaneo de redes y sistemas

## Scripts Disponibles

### Análisis y Detección
- `analisis/vulnerability_analyzer.py`: Analiza sistemas en busca de vulnerabilidades conocidas
- `analisis/advanced_malware_analyzer.py`: Analizador avanzado de malware con reglas YARA
- `analisis/memory_analyzer.py`: Analiza volcados de memoria en busca de indicadores de compromiso
- `analisis/security_log_analyzer.py`: Analiza logs de seguridad en busca de patrones sospechosos
- `analisis/server_hardening.py`: Verifica y aplica configuraciones de seguridad en servidores

### Fuerza Bruta
- `brute_force/john_brute.py`: Realiza ataques de fuerza bruta con John the Ripper
- `brute_force/hydra_brute.py`: Realiza ataques de fuerza bruta con Hydra en diferentes servicios

### Escaneo de Redes
- `scanning/nmap_scan.py`: Script base para escaneos con Nmap
- `scanning/nmap_quick.py`: Escaneo rápido de puertos y servicios
- `scanning/nmap_completo.py`: Escaneo exhaustivo de puertos, servicios y vulnerabilidades
- `scanning/nmap_os.py`: Detección de sistema operativo

### Utilidades
- `utilidades/dir_enum.py`: Enumeración de directorios web
- `utilidades/port_scanner.py`: Escáner básico de puertos
- `utilidades/subdomain_enum.py`: Enumeración de subdominios

## Requisitos

Los scripts requieren las siguientes dependencias:
- Python 3.8+
- Dependencias listadas en `requirements.txt`
- Herramientas externas:
  - John the Ripper
  - Hydra
  - Nmap
  - YARA (para análisis de malware)

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

## Contribución

1. Seguir las guías de estilo
2. Documentar los cambios
3. Probar las modificaciones
4. Actualizar la documentación 