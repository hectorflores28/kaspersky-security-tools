#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Control de Aplicaciones
Este script gestiona el control de aplicaciones en Windows y Linux.
"""

import os
import sys
import logging
import json
import platform
import subprocess
import psutil
from datetime import datetime

class AppControl:
    def __init__(self):
        self.logger = self._setup_logging()
        self.os_type = platform.system().lower()

    def _setup_logging(self):
        """Configura el sistema de logging."""
        log_dir = os.path.join(os.path.dirname(__file__), '../../logs')
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, f'app_control_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def get_running_apps(self):
        """Obtiene la lista de aplicaciones en ejecución."""
        try:
            apps = []
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
                try:
                    app_info = proc.info
                    app_info['path'] = proc.exe()
                    apps.append(app_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            return apps
        except Exception as e:
            self.logger.error(f"Error al obtener aplicaciones: {str(e)}")
            return []

    def get_installed_apps(self):
        """Obtiene la lista de aplicaciones instaladas."""
        try:
            if self.os_type == 'windows':
                return self._get_windows_installed_apps()
            else:
                return self._get_linux_installed_apps()
        except Exception as e:
            self.logger.error(f"Error al obtener aplicaciones instaladas: {str(e)}")
            return []

    def _get_windows_installed_apps(self):
        """Obtiene aplicaciones instaladas en Windows."""
        try:
            apps = []
            # Consulta de 32 bits
            output = subprocess.check_output(
                'powershell "Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName, DisplayVersion, Publisher, InstallDate | ConvertTo-Json"',
                shell=True
            ).decode('utf-8')
            apps.extend(json.loads(output))

            # Consulta de 64 bits
            output = subprocess.check_output(
                'powershell "Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName, DisplayVersion, Publisher, InstallDate | ConvertTo-Json"',
                shell=True
            ).decode('utf-8')
            apps.extend(json.loads(output))

            return apps
        except Exception as e:
            self.logger.error(f"Error al obtener aplicaciones de Windows: {str(e)}")
            return []

    def _get_linux_installed_apps(self):
        """Obtiene aplicaciones instaladas en Linux."""
        try:
            apps = []
            # Debian/Ubuntu
            if os.path.exists('/usr/bin/dpkg'):
                output = subprocess.check_output(['dpkg', '-l'], universal_newlines=True)
                for line in output.split('\n')[5:]:
                    if line:
                        parts = line.split()
                        if len(parts) >= 3:
                            apps.append({
                                'name': parts[1],
                                'version': parts[2],
                                'description': ' '.join(parts[3:])
                            })
            # Red Hat/CentOS
            elif os.path.exists('/usr/bin/rpm'):
                output = subprocess.check_output(['rpm', '-qa', '--queryformat', '%{NAME}\t%{VERSION}\t%{SUMMARY}\n'],
                                              universal_newlines=True)
                for line in output.split('\n'):
                    if line:
                        parts = line.split('\t')
                        if len(parts) >= 3:
                            apps.append({
                                'name': parts[0],
                                'version': parts[1],
                                'description': parts[2]
                            })
            return apps
        except Exception as e:
            self.logger.error(f"Error al obtener aplicaciones de Linux: {str(e)}")
            return []

    def block_app(self, app_name):
        """Bloquea una aplicación específica."""
        try:
            if self.os_type == 'windows':
                return self._block_windows_app(app_name)
            else:
                return self._block_linux_app(app_name)
        except Exception as e:
            self.logger.error(f"Error al bloquear aplicación: {str(e)}")
            return False

    def _block_windows_app(self, app_name):
        """Bloquea una aplicación en Windows usando AppLocker."""
        try:
            # Crear regla de AppLocker
            cmd = f'powershell "New-AppLockerPolicy -XmlPolicy -RuleCollectionType Appx,Exe,Script -User Everyone -RuleName "Block {app_name}" -Path "{app_name}" -Action Deny"'
            subprocess.run(cmd, shell=True, check=True)
            return True
        except Exception as e:
            self.logger.error(f"Error al bloquear aplicación en Windows: {str(e)}")
            return False

    def _block_linux_app(self, app_name):
        """Bloquea una aplicación en Linux usando AppArmor."""
        try:
            # Crear perfil de AppArmor
            profile = f"""
#include <tunables/global>

profile {app_name} flags=(attach_disconnected) {{
    #include <abstractions/base>
    #include <abstractions/python>

    deny /usr/bin/{app_name} rwx,
}}
"""
            profile_path = f"/etc/apparmor.d/usr.bin.{app_name}"
            with open(profile_path, 'w') as f:
                f.write(profile)
            
            # Cargar perfil
            subprocess.run(['apparmor_parser', '-r', profile_path], check=True)
            return True
        except Exception as e:
            self.logger.error(f"Error al bloquear aplicación en Linux: {str(e)}")
            return False

    def unblock_app(self, app_name):
        """Desbloquea una aplicación específica."""
        try:
            if self.os_type == 'windows':
                return self._unblock_windows_app(app_name)
            else:
                return self._unblock_linux_app(app_name)
        except Exception as e:
            self.logger.error(f"Error al desbloquear aplicación: {str(e)}")
            return False

    def _unblock_windows_app(self, app_name):
        """Desbloquea una aplicación en Windows."""
        try:
            cmd = f'powershell "Remove-AppLockerPolicy -XmlPolicy -RuleName "Block {app_name}"'
            subprocess.run(cmd, shell=True, check=True)
            return True
        except Exception as e:
            self.logger.error(f"Error al desbloquear aplicación en Windows: {str(e)}")
            return False

    def _unblock_linux_app(self, app_name):
        """Desbloquea una aplicación en Linux."""
        try:
            profile_path = f"/etc/apparmor.d/usr.bin.{app_name}"
            if os.path.exists(profile_path):
                subprocess.run(['apparmor_parser', '-R', profile_path], check=True)
                os.remove(profile_path)
            return True
        except Exception as e:
            self.logger.error(f"Error al desbloquear aplicación en Linux: {str(e)}")
            return False

    def export_app_list(self, filename=None):
        """Exporta la lista de aplicaciones a un archivo JSON."""
        if not filename:
            filename = f'app_list_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

        try:
            apps = {
                'running': self.get_running_apps(),
                'installed': self.get_installed_apps()
            }
            with open(filename, 'w') as f:
                json.dump(apps, f, indent=4)
            self.logger.info(f"Lista de aplicaciones exportada a {filename}")
        except Exception as e:
            self.logger.error(f"Error al exportar lista de aplicaciones: {str(e)}")

def main():
    # Ejemplo de uso
    app_control = AppControl()
    
    # Obtener aplicaciones en ejecución
    running_apps = app_control.get_running_apps()
    
    # Obtener aplicaciones instaladas
    installed_apps = app_control.get_installed_apps()
    
    # Bloquear una aplicación
    app_control.block_app('notepad.exe')
    
    # Exportar lista de aplicaciones
    app_control.export_app_list()

if __name__ == "__main__":
    main() 