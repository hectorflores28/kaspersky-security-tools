# Scripts de Automatización

Esta carpeta contiene scripts útiles para tareas básicas de ciberseguridad.

## Scripts Disponibles

### Utilidades
1. `port_scanner.py`
   - Escaneo básico de puertos
   - Uso: `python port_scanner.py <host> <puerto_inicio> <puerto_fin>`
   - Ejemplo: `python port_scanner.py 192.168.1.1 1 1000`

2. `dir_enum.py`
   - Enumeración de directorios web
   - Uso: `python dir_enum.py <url> <wordlist>`
   - Ejemplo: `python dir_enum.py http://example.com wordlist.txt`

3. `subdomain_enum.py`
   - Enumeración de subdominios
   - Uso: `python subdomain_enum.py <dominio> <wordlist>`
   - Ejemplo: `python subdomain_enum.py example.com subdomains.txt`

## Requisitos
Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Notas de Uso
- Estos scripts son herramientas básicas para aprendizaje
- Úselos solo en sistemas que tenga permiso para probar
- No se recomienda su uso en entornos de producción sin modificaciones adicionales

## Mejoras Planificadas
- Agregar soporte para proxies
- Implementar manejo de errores más robusto
- Agregar opciones de personalización
- Mejorar la velocidad de ejecución 