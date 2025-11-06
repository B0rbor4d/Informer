"""
TeamViewer Monitor - Zeigt die TeamViewer ID an
"""

import sys
import platform
from typing import Optional
from monitors.base_monitor import BaseMonitor


class TeamViewerMonitor(BaseMonitor):
    """
    Monitor für TeamViewer ID.
    Unterstützt Windows (Registry) und Linux (Config-Datei).
    """

    def __init__(self, name: str = "TeamViewer ID", icon: str = "🖥️"):
        super().__init__(name, icon)
        self.system = platform.system()

    async def get_value(self) -> Optional[str]:
        """
        Ermittelt die TeamViewer ID des Systems.

        Returns:
            TeamViewer ID als String, oder None wenn nicht verfügbar
        """
        try:
            if self.system == "Windows":
                return self._get_teamviewer_id_windows()
            elif self.system == "Linux":
                return self._get_teamviewer_id_linux()
            else:
                return None
        except Exception as e:
            print(f"⚠️  TeamViewer Monitor Fehler: {e}")
            return None

    def _get_teamviewer_id_windows(self) -> Optional[str]:
        """
        Liest TeamViewer ID aus Windows Registry.

        Returns:
            TeamViewer ID oder None
        """
        try:
            import winreg

            # Mögliche Registry-Pfade
            registry_paths = [
                r"SOFTWARE\TeamViewer",
                r"SOFTWARE\WOW6432Node\TeamViewer",
            ]

            for path in registry_paths:
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
                    client_id, _ = winreg.QueryValueEx(key, "ClientID")
                    winreg.CloseKey(key)

                    if client_id:
                        return str(client_id)
                except FileNotFoundError:
                    continue
                except Exception:
                    continue

            return None

        except ImportError:
            print("⚠️  winreg Modul nicht verfügbar (nicht Windows?)")
            return None
        except Exception as e:
            print(f"⚠️  Windows Registry Fehler: {e}")
            return None

    def _get_teamviewer_id_linux(self) -> Optional[str]:
        """
        Liest TeamViewer ID aus Linux Config-Datei.

        Returns:
            TeamViewer ID oder None
        """
        try:
            config_path = "/opt/teamviewer/config/global.conf"

            with open(config_path, 'r') as f:
                for line in f:
                    if line.startswith("ClientID"):
                        # Format: ClientID = 123456789
                        parts = line.split("=")
                        if len(parts) == 2:
                            client_id = parts[1].strip()
                            return client_id

            return None

        except FileNotFoundError:
            print("⚠️  TeamViewer Config nicht gefunden")
            return None
        except Exception as e:
            print(f"⚠️  Linux Config Fehler: {e}")
            return None

    def format_value(self, value: Optional[str]) -> str:
        """
        Formatiert die TeamViewer ID für Discord.

        Args:
            value: TeamViewer ID

        Returns:
            Formatierter String
        """
        if value is None:
            return '❌ TeamViewer nicht gefunden'

        # TeamViewer ID mit Trennzeichen formatieren
        # z.B. 1234567890 -> 1 234 567 890
        if value.isdigit() and len(value) >= 9:
            formatted = ' '.join([value[i:i+3] for i in range(0, len(value), 3)])
            return f'`{formatted}`'

        return f'`{value}`'
