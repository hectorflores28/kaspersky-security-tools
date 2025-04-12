# Proyecto de Documentación de Ciberseguridad

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
- `malware_detector.py`: Herramienta para detección básica de malware
  - Análisis de archivos PE
  - Cálculo de hashes MD5
  - Escaneo de directorios
- `log_analyzer.py`: Herramienta para análisis de logs
  - Procesamiento de logs de eventos
  - Detección de patrones sospechosos
  - Generación de reportes

## Estructura del Proyecto
- `documentacion/`: Guías y manuales
- `scripts/`: Scripts de automatización
  - `utilidades/`: Scripts de utilidad
    - `malware_detector.py`
    - `log_analyzer.py`
    - `requirements.txt`
- `playbooks/`: Playbooks de respuesta a incidentes
- `herramientas/`: Herramientas personalizadas
- `casos/`: Casos de estudio y análisis
- `logs/`: Registros y análisis

## Estado Actual
- ✅ Seguridad en Active Directory (Completado)
- ✅ Aspectos Investigativos Básicos (Completado)
- 🔄 Software Malicioso (En progreso)
  - ✅ Script de detección básica de malware
  - ⏳ Análisis avanzado de malware
- ⏳ Phishing y OSINT (Pendiente)
- ⏳ PuP y Exploits (Pendiente)
- ⏳ Seguridad de Servidores (Pendiente)

## Próximos Pasos
1. Desarrollar playbooks de respuesta a incidentes
2. Crear scripts de automatización para análisis forense
3. Implementar sistema de monitoreo de red con ntopng
4. Desarrollar herramientas de análisis de logs
5. Crear base de datos de firmas de malware

## Contribución
Las contribuciones son bienvenidas. Por favor, asegúrate de:
1. Seguir las guías de estilo
2. Documentar los cambios
3. Probar las modificaciones
4. Actualizar la documentación correspondiente

## Licencia
Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.