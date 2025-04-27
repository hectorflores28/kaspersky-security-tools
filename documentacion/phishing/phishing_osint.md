# Phishing e Inteligencia de Código Abierto

## Búsqueda y Eliminación de Correos de Phishing

### Comandos PowerShell para Exchange
```powershell
# Búsqueda base
Get-Mailbox | Search-mailbox -TargetMailbox admin@omegab2b.com –TargetFolder Resultados -SearchQuery ""

# Búsqueda por remitente
Get-Mailbox | Search-mailbox -TargetMailbox admin@omegab2b.com –TargetFolder Results -SearchQuery "from:'bob.dylan@verified-resume.com'"

# Búsqueda por asunto
Get-Mailbox | Search-mailbox -TargetMailbox admin@omegab2b.com -TargetFolder Results -SearchQuery "subject: HelloWorld"
```

### Parámetros de Búsqueda
- `Get-Mailbox`: Enumera todos los buzones
- `Search-Mailbox`: Realiza la búsqueda
- `-TargetMailbox`: Buzón destino para resultados
- `-TargetFolder`: Carpeta para almacenar resultados
- `-SearchQuery`: Consulta de búsqueda
- `-LogOnly -LogLevel Full`: Verificar sin mover/eliminar

### Ejemplos de Búsquedas
```powershell
# Por remitente específico
Get-Mailbox | Search-mailbox -TargetMailbox admin@omegab2b.com –TargetFolder Results -SearchQuery "from:'bob.dylan@verified-resume.com'"

# Por dominio de remitente
Get-Mailbox | Search-mailbox -TargetMailbox admin@omegab2b.com –TargetFolder Results -SearchQuery "from:'*@verified-resume.com'"

# Por asunto
Get-Mailbox | Search-mailbox -TargetMailbox admin@omegab2b.com -TargetFolder Results -SearchQuery "subject: Resume"

# Por cuerpo del mensaje
Get-Mailbox | Search-mailbox -TargetMailbox admin@omegab2b.com –TargetFolder Results -SearchQuery "body: support"
```

## Análisis de URLs Maliciosas

### Herramientas de Verificación
- [TrueURL](http://trueurl.net/) - Decodificación de URLs
- [PhishTank](https://phishtank.com/) - Verificación de dominios maliciosos
- [VirusTotal](https://www.virustotal.com/gui/home/upload) - Análisis de URLs

## Técnicas de Phishing

### Añadir Ruido a Correos
- Definir ruido del mismo color que el fondo
- Ocultar ruido mediante CSS
- URLs maliciosas ocultas

### Infraestructura de Suplantación
- Piratería de sitios web legítimos
- Creación de páginas maliciosas
- Enlaces similares en ataques masivos

## Análisis de Encabezados de Correo

### SPF (Sender Policy Framework)
- Verifica el servidor que envía el mensaje
- Resultados en encabezado Authentication-Result

### DKIM (DomainKeys Identified Mail)
- Protección basada en firmas digitales
- Verifica autenticación del dominio
- Proceso:
  1. Cliente crea mensaje
  2. Servidor firma mensaje
  3. Servidor destino verifica firma

## Análisis DNS
### Herramientas
- [WhatsMyDNS](https://whatsmydns.me/es)
- [DNS Checker](https://dnschecker.org/all-dns-records-of-domain.php)
- [Site24x7](https://www.site24x7.com/es/tools/analizar-dominio-dns.html)

## Inteligencia de Código Abierto (OSINT)

### Herramientas de Búsqueda
- Google, Yandex, Baidu
- [Shodan](https://www.shodan.io/)
- [BuiltWith](https://builtwith.com/)
- [HackerTarget](https://hackertarget.com/)

### Recon-ng
Herramienta para automatizar búsquedas OSINT

#### Tablas Principales
- domains: Dominios de empresa
- companies: Información de empresa
- ports: Puertos abiertos
- hosts: Hosts conectados
- contacts: Personas relacionadas
- credentials: Información de cuentas

#### Módulos Principales
1. shodan_hostname
   - Busca dispositivos conectados
   - Analiza puertos y servicios

2. builtwith
   - Información de sitios web
   - Contactos y tecnologías

3. hackertarget
   - Búsqueda de vulnerabilidades
   - Análisis de servidores

4. resolve
   - Resolución DNS
   - Mapeo IP-Dominio

5. freegeoip
   - Ubicación geográfica
   - Información de servidores

### Google Dorks
Búsquedas avanzadas para encontrar información expuesta:
```markdown
# Ejemplo: Buscar archivos de configuración
inurl:"sitemanager.xml" ext:xml-git
```

### Búsqueda de Filtraciones
- [Pastebin](https://pastebin.com/)
- [Have I Been Pwned](https://haveibeenpwned.com/)
- [Exploit Database](https://www.exploit-db.com/google-hacking-database)

### Módulos de Búsqueda de Filtraciones
1. hibp_paste
   - Busca correos en bases de datos filtradas
   - Verifica múltiples fuentes

2. github_miner
   - Busca repositorios relacionados
   - Analiza perfiles de usuarios

3. github_commits
   - Busca confirmaciones en repositorios
   - Identifica contribuidores

## Actividades Prácticas

### Búsqueda de Phishing
```powershell
# Búsqueda por múltiples remitentes
Get-Mailbox | Search-mailbox -TargetMailbox admin@omegab2b.com –TargetFolder Results -SearchQuery "from:'no-reply@mail-access.info' OR from:'accounts@mail-access.info' OR from:'accounts@securityupdate.pro'"
```

### OSINT con Recon-ng
```bash
# Configuración inicial
add domains omegab2b.com
add domains support.omegab2b.com

# Ejecución de módulos
use recon/domains-hosts/shodan_hostname
run
show hosts

# Análisis de ubicación
use recon/hosts-hosts/freegeoip
run
``` 