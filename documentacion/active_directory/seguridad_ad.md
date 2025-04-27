# Seguridad en Active Directory

## Verificación de Contraseñas

### API Have I Been Pwned?
Herramienta para verificar si una contraseña ha sido comprometida en filtraciones de datos.

Ejemplo de uso:
```powershell
# Guardar contraseña en archivo
# C:\Users\admin\Documents\pass.txt

# Obtener hash SHA1
Get-FileHash -Path .\Documents\pass.txt -Algorithm SHA1
# Ejemplo: CCF0730A2B5B791499AF996389BFD43F76704745
```

### Recomendaciones NIST 800-63B
- Comprobar contraseñas periódicamente
- No forzar cambios frecuentes innecesarios
- [Documentación NIST](https://pages.nist.gov/800-63-3/sp800-63b.html)

### Fuentes de Listas de Contraseñas
- [Have I Been Pwned](https://haveibeenpwned.com/)
- Almacenadas como hashes SHA-1 o NTLM
- Más de 6 millones de contraseñas documentadas

### Herramientas para Generar Hashes

#### CyberChef
- [Descarga CyberChef](https://gchq.github.io/CyberChef/)
- Usar copia local
- Seleccionar Hashing | SHA1

#### PowerShell
```powershell
Get-FileHash -Path <path-to-file> -Algorithm SHA1
```

> **Nota**: No usar redirección de archivo (>>) ya que genera hash incorrecto

### Método de Comprobación API
1. Enviar primeros 5 caracteres del hash
2. Recibir lista de hashes encontrados
3. Comparar localmente el hash completo

> **Ventaja**: Método seguro ya que no se envía el hash completo

## Microsoft LAPS (Local Administrator Password Solution)

### Descripción
Herramienta que utiliza GPO para:
- Cambiar periódicamente contraseñas de administrador local
- Generar contraseñas aleatorias
- Almacenar contraseñas en atributos de AD

### Configuración

#### Asignación de Permisos
```powershell
# Autoadministración de contraseñas
Set-AdmPwdComputerSelfPermission -OrgUnit PCs

# Lectura de contraseñas LAPS
Set-AdmPwdReadPasswordPermission -OrgUnit PCs -AllowedPrincipals 'OMEGAB2B\Domain admins', servicedesk

# Restablecimiento de contraseñas
Set-AdmPwdResetPasswordPermission -OrgUnit PCs -AllowedPrincipals 'OMEGAB2B\Domain admins', servicedesk
```

#### Ejemplo para Equipo Específico
```powershell
# Para CN=PETROV-PC
Set-AdmPwdComputerSelfPermission -Identity "CN=PETROV-PC,OU=Desktops,DC=omegab2b,DC=com"
Set-AdmPwdReadPasswordPermission -Identity "CN=PETROV-PC,OU=Desktops,DC=omegab2b,DC=com" -AllowedPrincipals "OMEGAB2B\Domain admins", "servicedesk"
Set-AdmPwdResetPasswordPermission -Identity "CN=PETROV-PC,OU=Desktops,DC=omegab2b,DC=com" -AllowedPrincipals "OMEGAB2B\Domain admins", "servicedesk"
```

### Consulta de Contraseñas
```powershell
Get-AdmPwdPassword -ComputerName admin-pc
```

### Verificación de Cobertura
- Usar PingCastle para análisis independiente
- Identificar equipos sin LAPS implementado

## Estructura de Active Directory

### Componentes Principales
- CN (Common Name)
- OU (Organizational Unit)
- DC (Domain Component)

### Ejemplo de DN
```
CN=PETROV-PC,OU=Desktops,DC=omegab2b,DC=com
```

## Auditoría de Active Directory

### PingCastle
Herramienta para:
- Detectar cuentas que requieren monitoreo
- Verificar cobertura de políticas de seguridad
- Analizar vulnerabilidades en la estructura de AD

### Cuentas de Administrador Local
- Riesgo de movimiento lateral mediante pass-the-hash
- Solución: Implementar LAPS para gestión centralizada
- Cambio periódico de contraseñas
- Almacenamiento seguro en AD 