# Investigación Forense Digital

## Definición
La investigación forense digital es la ciencia detrás de la resolución de delitos relacionados con la información y los datos informáticos. Los especialistas utilizan sus conocimientos para buscar evidencia que determine los hechos de los delitos informáticos.

## Fundamentos de Investigación
Preguntas clave a plantearse:
- ¿Quién llevó a cabo el ataque?
- ¿Cuándo ocurrió el ataque?
- ¿Qué servidores o estaciones de trabajo resultaron perjudicados?
- ¿Cuáles fueron los motivos y objetivos de los atacantes?

## Primeros Pasos ante un Incidente
1. Aislar los ordenadores comprometidos
2. Recopilar información para análisis posterior
3. No desconectar físicamente los ordenadores infectados
4. Reconfigurar reglas de enrutamiento para aislar la máquina infectada

## Recopilación de Información

### Imágenes de Memoria y Disco
#### FTK Imager
- Permite guardar imágenes de unidades en uso
- [Descarga FTK Imager](http://accessdata.com/product-download/ftk-imager-lite-version-3.1.1)
- Recomendación: Adjuntar archivo de paginación (pagefile.sys) a la captura

#### Belkasoft
- Alternativa cuando otras apps evitan la captura de memoria
- Belkasoft Live RAM Capturer para evadir restricciones

#### Imágenes del Disco Duro
- Capturar después de la RAM
- No apagar normalmente (pérdida de información en %TEMP%)
- Desenchufar directamente
- Usar "Create Disk Image" en Windows
- Capturar disco físico completo, incluyendo sectores no utilizados

### Fuentes de Evidencia
- Registros de firewall
- Registros del controlador de dominio
- Registros de DNS
- Registros de Windows

## Análisis de Registros de Windows

### Comprobación Diaria
- Muchos ataques pueden descubrirse en etapas tempranas
- Información disponible en sistema y registros de aplicación

### Eventos Anómalos
- Cambios de contraseñas de usuarios
- Eliminación de registros de eventos
- Cambios en horario del sistema
- Intentos de autentificación fallidos
- Cambios en configuración de firewall
- Uso de cuentas con privilegios elevados

### Archivos de Registro
- Ubicación: %windir%\system32\winevt\
- Herramienta: Event Viewer
- Tipos de registros:
  1. Application (eventos de apps)
  2. Setup (instalaciones)
  3. System (componentes del sistema)
  4. Security (directiva de auditoría)
  5. Forwarded Events (eventos remotos)

### Audit Policy
- Configuración en secpol.msc
- [Recomendaciones de Auditoría](https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/audit-policy-recommendations)

## Identificación de Usuarios
- Reglas de nomenclatura:
  - nombre.apellido
  - inicial.apellido
- Cuentas con privilegios: nombre.apellidoPE
- Atención a discrepancias entre sistemas (AD vs BD)

## Análisis de Actividad del Usuario

### Logon ID
- Evento 4624 (inicio de sesión)
- Evento 4663 (eliminación de archivos)
- Evento 4624 contiene dirección IP del usuario

### Logon Type
- 2: Interactive (teclado y pantalla)
- 3: Network (red)
- 4: Batch (tareas programadas)
- 5: Service (servicios)
- 10: Remote Interactive (RDP)

## Análisis del Sistema de Archivos

### Montaje de Unidades
- FTK Imager para montar imágenes
- Autopsy (GUI de Sleuth Kit)
- [Descarga Autopsy](https://www.sleuthkit.org/autopsy/download.php)

### Marcas de Tiempo
- Modified Time
- Accessed Time
- Creation Time
- Útiles para crear línea de tiempo de eventos

## Protocolo Netflow

### Definición
Protocolo estándar de la industria para generar reportes de red, desarrollado por Cisco Systems.

### Estructura
- Divide paquetes en "flujos"
- Metadatos importantes:
  - Marcas de tiempo
  - Dirección de origen
  - Dirección de destino
  - Código de protocolo

### Arquitectura
1. Sensor (enrutador Cisco)
2. Colector
3. Analizador

### Amenazas Detectables
- Movimiento lateral
- Conexiones desde puertos no estándar
- Comunicación entre máquinas comprometidas

## Análisis de Tráfico

### Puertos del Sistema (0-1023)
- Actividad sospechosa en puertos conocidos
- Verificación de servicios legítimos

### Puertos Personalizados (1024-49151)
- Lista de servicios permitidos
- Monitoreo de actividad no autorizada

### Puertos Dinámicos (49151-65535)
- Asignación aleatoria para conexiones internas
- Actividad sospechosa en conexiones externas

## Herramientas de Análisis

### Ntop
- Análisis y supervisión en tiempo real
- [Descarga Ntop](http://www.ntop.org/get-started/download/)
- Funcionalidades:
  - Análisis de red/detección (NIDS)
  - Seguimiento de nuevas conexiones
  - Detección de llamadas de malware 