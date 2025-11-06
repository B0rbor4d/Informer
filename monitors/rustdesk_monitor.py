"""
RustDesk Monitor - Zeigt die RustDesk ID an
"""

import os
import platform
from typing import Optional
from monitors.base_monitor import BaseMonitor


class RustDeskMonitor(BaseMonitor):
    """
    Monitor für RustDesk ID.
    Unterstützt Windows und Linux Config-Dateien.
    """

    def __init__(self, name: str = "RustDesk ID", icon: str = "🖥️"):
        super().__init__(name, icon)
        self.system = platform.system()

    async def get_value(self) -> Optional[str]:
        """
        Ermittelt die RustDesk ID des Systems.

        Returns:
            RustDesk ID als String, oder None wenn nicht verfügbar
        """
        try:
            if self.system == "Windows":
                return self._get_rustdesk_id_windows()
            elif self.system == "Linux":
                return self._get_rustdesk_id_linux()
            else:
                return None
        except Exception as e:
            print(f"⚠️  RustDesk Monitor Fehler: {e}")
            return None

    def _get_rustdesk_id_windows(self) -> Optional[str]:
        """
        Liest RustDesk ID aus Windows Config-Datei.

        Returns:
            RustDesk ID oder None
        """
        try:
            # Mögliche Config-Pfade
            appdata = os.environ.get('APPDATA', '')
            config_paths = [
                os.path.join(appdata, 'RustDesk', 'config', 'RustDesk2.toml'),
                os.path.join(appdata, 'RustDesk', 'config', 'RustDesk.toml'),
            ]

            for config_path in config_paths:
                if os.path.exists(config_path):
                    with open(config_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            # Suche nach id = "123456789"
                            if line.strip().startswith('id'):
                                parts = line.split('=')
                                if len(parts) == 2:
                                    rustdesk_id = parts[1].strip().strip('"').strip("'")
                                    if rustdesk_id:
                                        return rustdesk_id

            return None

        except Exception as e:
            print(f"⚠️  Windows Config Fehler: {e}")
            return None

    def _get_rustdesk_id_linux(self) -> Optional[str]:
        """
        Liest RustDesk ID aus Linux Config-Datei.

        Returns:
            RustDesk ID oder None
        """
        try:
            home = os.path.expanduser('~')
            config_paths = [
                os.path.join(home, '.config', 'rustdesk', 'RustDesk2.toml'),
                os.path.join(home, '.config', 'rustdesk', 'RustDesk.toml'),
            ]

            for config_path in config_paths:
                if os.path.exists(config_path):
                    with open(config_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            # Suche nach id = "123456789"
                            if line.strip().startswith('id'):
                                parts = line.split('=')
                                if len(parts) == 2:
                                    rustdesk_id = parts[1].strip().strip('"').strip("'")
                                    if rustdesk_id:
                                        return rustdesk_id

            return None

        except FileNotFoundError:
            print("⚠️  RustDesk Config nicht gefunden")
            return None
        except Exception as e:
            print(f"⚠️  Linux Config Fehler: {e}")
            return None

    def format_value(self, value: Optional[str]) -> str:
        """
        Formatiert die RustDesk ID für Discord.

        Args:
            value: RustDesk ID

        Returns:
            Formatierter String
        """
        if value is None:
            return '❌ RustDesk nicht gefunden'

        # RustDesk ID formatieren (meist 9-12 Ziffern)
        # z.B. 123456789 -> 123 456 789
        if value.isdigit() and len(value) >= 9:
            formatted = ' '.join([value[i:i+3] for i in range(0, len(value), 3)])
            return f'`{formatted}`'

        return f'`{value}`'
