"""
Base Monitor - Abstrakte Basisklasse für alle Monitor-Module
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict


class BaseMonitor(ABC):
    """
    Abstrakte Basisklasse für alle Monitor-Module.

    Jedes Modul muss:
    - get_value() implementieren (gibt aktuellen Wert zurück)
    - Optional: format_value() überschreiben für custom Formatierung
    """

    def __init__(self, name: str = "Monitor", icon: str = "📊"):
        """
        Initialisiert den Monitor.

        Args:
            name: Anzeigename des Monitors
            icon: Emoji-Icon für Discord
        """
        self.name = name
        self.icon = icon
        self.last_value: Optional[str] = None
        self.current_value: Optional[str] = None

    @abstractmethod
    async def get_value(self) -> Optional[str]:
        """
        Hauptmethode: Ermittelt den aktuellen Wert.
        Muss von jeder Subklasse implementiert werden.

        Returns:
            Aktueller Wert als String, oder None bei Fehler
        """
        pass

    async def check_update(self) -> bool:
        """
        Prüft, ob sich der Wert geändert hat.
        Ruft get_value() auf und vergleicht mit vorherigem Wert.

        Returns:
            True wenn sich der Wert geändert hat, sonst False
        """
        self.last_value = self.current_value
        self.current_value = await self.get_value()

        # Beim ersten Aufruf immer True zurückgeben
        if self.last_value is None:
            return True

        # True wenn sich der Wert geändert hat
        return self.current_value != self.last_value

    def format_value(self, value: Optional[str]) -> str:
        """
        Formatiert den Wert für die Anzeige in Discord.
        Kann von Subklassen überschrieben werden für custom Formatierung.

        Args:
            value: Zu formatierender Wert

        Returns:
            Formatierter String für Discord
        """
        if value is None:
            return '❌ Nicht verfügbar'
        return f'**{value}**'

    def get_field_dict(self) -> Dict[str, any]:
        """
        Erstellt ein Dictionary für ein Discord Embed Field.

        Returns:
            Dict mit name, value, inline für discord.Embed.add_field()
        """
        formatted_value = self.format_value(self.current_value)

        return {
            'name': f'{self.icon} {self.name}',
            'value': formatted_value,
            'inline': False
        }

    def __repr__(self) -> str:
        """String-Repräsentation für Debugging."""
        return f"<{self.__class__.__name__} name='{self.name}' value='{self.current_value}'>"
