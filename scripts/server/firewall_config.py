#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configurador de Firewall
Este script gestiona las reglas del firewall en Windows y Linux.
"""

import os
import sys
import logging
import json
import platform
import subprocess
from datetime import datetime

class FirewallConfig:
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
                logging.FileHandler(os.path.join(log_dir, f'firewall_config_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def get_firewall_rules(self):
        """Obtiene las reglas del firewall según el sistema operativo."""
        if self.os_type == 'windows':
            return self._get_windows_rules()
        else:
            return self._get_linux_rules()

    def _get_windows_rules(self):
        """Obtiene reglas del firewall de Windows."""
        try:
            output = subprocess.check_output(['netsh', 'advfirewall', 'firewall', 'show', 'rule', 'name=all'],
                                          universal_newlines=True)
            rules = []
            current_rule = {}
            
            for line in output.split('\n'):
                line = line.strip()
                if line.startswith('Rule Name:'):
                    if current_rule:
                        rules.append(current_rule)
                    current_rule = {'name': line.split(':', 1)[1].strip()}
                elif line.startswith('Enabled:'):
                    current_rule['enabled'] = line.split(':', 1)[1].strip()
                elif line.startswith('Direction:'):
                    current_rule['direction'] = line.split(':', 1)[1].strip()
                elif line.startswith('Action:'):
                    current_rule['action'] = line.split(':', 1)[1].strip()
                elif line.startswith('Protocol:'):
                    current_rule['protocol'] = line.split(':', 1)[1].strip()
                elif line.startswith('LocalPort:'):
                    current_rule['local_port'] = line.split(':', 1)[1].strip()
                elif line.startswith('RemotePort:'):
                    current_rule['remote_port'] = line.split(':', 1)[1].strip()

            if current_rule:
                rules.append(current_rule)

            return rules
        except Exception as e:
            self.logger.error(f"Error al obtener reglas de Windows: {str(e)}")
            return []

    def _get_linux_rules(self):
        """Obtiene reglas del firewall de Linux (iptables)."""
        try:
            output = subprocess.check_output(['iptables', '-L', '-n', '-v'],
                                          universal_newlines=True)
            rules = []
            current_chain = None
            
            for line in output.split('\n'):
                line = line.strip()
                if line.startswith('Chain'):
                    current_chain = line.split()[1]
                elif line and not line.startswith('target') and not line.startswith('Chain'):
                    parts = line.split()
                    if len(parts) >= 8:
                        rules.append({
                            'chain': current_chain,
                            'target': parts[0],
                            'protocol': parts[1],
                            'source': parts[3],
                            'destination': parts[4],
                            'ports': parts[6] if len(parts) > 6 else 'any'
                        })

            return rules
        except Exception as e:
            self.logger.error(f"Error al obtener reglas de Linux: {str(e)}")
            return []

    def add_rule(self, rule_config):
        """Agrega una nueva regla al firewall."""
        try:
            if self.os_type == 'windows':
                return self._add_windows_rule(rule_config)
            else:
                return self._add_linux_rule(rule_config)
        except Exception as e:
            self.logger.error(f"Error al agregar regla: {str(e)}")
            return False

    def _add_windows_rule(self, rule_config):
        """Agrega una regla al firewall de Windows."""
        try:
            cmd = ['netsh', 'advfirewall', 'firewall', 'add', 'rule']
            cmd.extend([
                f'name={rule_config["name"]}',
                f'dir={rule_config["direction"]}',
                f'action={rule_config["action"]}',
                f'protocol={rule_config["protocol"]}'
            ])
            
            if 'local_port' in rule_config:
                cmd.append(f'localport={rule_config["local_port"]}')
            if 'remote_port' in rule_config:
                cmd.append(f'remoteport={rule_config["remote_port"]}')
            if 'program' in rule_config:
                cmd.append(f'program={rule_config["program"]}')
            
            subprocess.run(cmd, check=True)
            return True
        except Exception as e:
            self.logger.error(f"Error al agregar regla de Windows: {str(e)}")
            return False

    def _add_linux_rule(self, rule_config):
        """Agrega una regla al firewall de Linux."""
        try:
            cmd = ['iptables', '-A', rule_config['chain']]
            
            if 'protocol' in rule_config:
                cmd.extend(['-p', rule_config['protocol']])
            if 'source' in rule_config:
                cmd.extend(['-s', rule_config['source']])
            if 'destination' in rule_config:
                cmd.extend(['-d', rule_config['destination']])
            if 'port' in rule_config:
                cmd.extend(['--dport', rule_config['port']])
            
            cmd.extend(['-j', rule_config['target']])
            
            subprocess.run(cmd, check=True)
            return True
        except Exception as e:
            self.logger.error(f"Error al agregar regla de Linux: {str(e)}")
            return False

    def remove_rule(self, rule_name):
        """Elimina una regla del firewall."""
        try:
            if self.os_type == 'windows':
                subprocess.run(['netsh', 'advfirewall', 'firewall', 'delete', 'rule', f'name={rule_name}'],
                             check=True)
            else:
                subprocess.run(['iptables', '-D', rule_name], check=True)
            return True
        except Exception as e:
            self.logger.error(f"Error al eliminar regla: {str(e)}")
            return False

    def export_rules(self, filename=None):
        """Exporta las reglas a un archivo JSON."""
        if not filename:
            filename = f'firewall_rules_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

        try:
            rules = self.get_firewall_rules()
            with open(filename, 'w') as f:
                json.dump(rules, f, indent=4)
            self.logger.info(f"Reglas exportadas a {filename}")
        except Exception as e:
            self.logger.error(f"Error al exportar reglas: {str(e)}")

def main():
    # Ejemplo de uso
    firewall = FirewallConfig()
    
    # Obtener reglas actuales
    rules = firewall.get_firewall_rules()
    
    # Agregar nueva regla
    new_rule = {
        'name': 'Allow Web Server',
        'direction': 'in',
        'action': 'allow',
        'protocol': 'TCP',
        'local_port': '80,443'
    }
    firewall.add_rule(new_rule)
    
    # Exportar reglas
    firewall.export_rules()

if __name__ == "__main__":
    main() 