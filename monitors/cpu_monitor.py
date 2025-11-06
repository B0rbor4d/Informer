"""
CPU Monitor - Zeigt CPU-Auslastung an (Beispiel-Modul)
"""

from typing import Optional
from monitors.base_monitor import BaseMonitor


class CPUMonitor(BaseMonitor):
    """
    Beispiel-Monitor für CPU-Auslastung.
    Benötigt das psutil Package (optional).
    """

    def __init__(self, name: str = "CPU Auslastung", icon: str = "💻"):
        super().__init__(name, icon)
        self.psutil_available = self._check_psutil()

    def _check_psutil(self) -> bool:
        """Prüft ob psutil verfügbar ist."""
        try:
            import psutil
            return True
        except ImportError:
            print("ℹ️  psutil nicht installiert - CPU Monitor deaktiviert")
            print("   Installation: pip install psutil")
            return False

    async def get_value(self) -> Optional[str]:
        """
        Ermittelt die aktuelle CPU-Auslastung.

        Returns:
            CPU-Auslastung als String (z.B. "45.2%") oder None
        """
        if not self.psutil_available:
            return None

        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            return f"{cpu_percent:.1f}%"
        except Exception as e:
            print(f"⚠️  CPU Monitor Fehler: {e}")
            return None

    def format_value(self, value: Optional[str]) -> str:
        """
        Formatiert CPU-Wert mit Emoji-Indicator.

        Args:
            value: CPU-Wert (z.B. "45.2%")

        Returns:
            Formatierter String mit Status-Emoji
        """
        if value is None:
            return '❌ psutil nicht installiert'

        try:
            # Prozentsatz extrahieren
            percent = float(value.rstrip('%'))

            # Status-Emoji basierend auf Auslastung
            if percent < 30:
                emoji = '🟢'  # Niedrig
            elif percent < 70:
                emoji = '🟡'  # Mittel
            else:
                emoji = '🔴'  # Hoch

            return f'{emoji} **{value}**'

        except ValueError:
            return f'**{value}**'
