"""
RustDesk Monitor - Zeigt die RustDesk ID an
"""

import os
import platform
import subprocess
from typing import Optional
from monitors.base_monitor import BaseMonitor


class RustDeskMonitor(BaseMonitor):
    """
    Monitor für RustDesk ID.
    Verwendet rustdesk.exe --get-id Befehl.
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
        Holt RustDesk ID über rustdesk.exe --get-id Befehl (Windows).

        Returns:
            RustDesk ID oder None
        """
        try:
            # Mögliche RustDesk.exe Pfade
            rustdesk_paths = [
                r"C:\Program Files\RustDesk\rustdesk.exe",
                r"C:\Program Files (x86)\RustDesk\rustdesk.exe",
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'RustDesk', 'rustdesk.exe'),
                os.path.join(os.environ.get('PROGRAMFILES', ''), 'RustDesk', 'rustdesk.exe'),
            ]

            # Versuche auch PATH
            try:
                result = subprocess.run(
                    ['rustdesk.exe', '--get-id'],
                    capture_output=True,
                    text=True,
                    timeout=3,
                    creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                )
                if result.returncode == 0 and result.stdout.strip():
                    return result.stdout.strip()
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

            # Versuche spezifische Pfade
            for rustdesk_path in rustdesk_paths:
                if os.path.exists(rustdesk_path):
                    try:
                        result = subprocess.run(
                            [rustdesk_path, '--get-id'],
                            capture_output=True,
                            text=True,
                            timeout=3,
                            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                        )
                        if result.returncode == 0 and result.stdout.strip():
                            return result.stdout.strip()
                    except subprocess.TimeoutExpired:
                        continue

            return None

        except Exception as e:
            print(f"⚠️  Windows Command Fehler: {e}")
            return None

    def _get_rustdesk_id_linux(self) -> Optional[str]:
        """
        Holt RustDesk ID über rustdesk --get-id Befehl (Linux).

        Returns:
            RustDesk ID oder None
        """
        try:
            # Versuche rustdesk Befehl
            result = subprocess.run(
                ['rustdesk', '--get-id'],
                capture_output=True,
                text=True,
                timeout=3
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()

            return None

        except FileNotFoundError:
            print("⚠️  RustDesk nicht im PATH gefunden")
            return None
        except subprocess.TimeoutExpired:
            print("⚠️  RustDesk Befehl Timeout")
            return None
        except Exception as e:
            print(f"⚠️  Linux Command Fehler: {e}")
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
