#!/usr/bin/env python3
"""
Discord System Monitor Bot - Multi-Device Support
Überwacht System-Informationen und zeigt sie in einem Discord-Channel an.
"""

import discord
import json
import asyncio
import socket
from typing import Dict, Optional, List
from monitors import AVAILABLE_MONITORS


class MonitorBot(discord.Client):
    """
    Discord Bot zur Überwachung von System-Informationen.
    Unterstützt mehrere Geräte parallel im selben Channel.
    """

    def __init__(self, config_path: str = 'config.json'):
        """
        Initialisiert den Bot mit Konfiguration.

        Args:
            config_path: Pfad zur JSON-Konfigurationsdatei
        """
        # Discord Intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True

        super().__init__(intents=intents)

        # Konfiguration laden
        self.config = self._load_config(config_path)

        # Bot-Eigenschaften
        self.channel_id = int(self.config['channel_id'])
        self.update_interval = self.config.get('update_interval', 60)
        self.device_name = self._get_device_name()

        # Monitore initialisieren
        self.monitors: Dict = {}
        self._init_monitors()

        # Embed-Tracking
        self.embed_message: Optional[discord.Message] = None
        self.embed_message_id: Optional[int] = None

        # Status
        self.is_running = False

    def _load_config(self, config_path: str) -> dict:
        """Lädt die Konfiguration aus JSON-Datei."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Fehler: Konfigurationsdatei '{config_path}' nicht gefunden!")
            print("💡 Erstellen Sie eine config.json basierend auf config.example.json")
            raise
        except json.JSONDecodeError as e:
            print(f"❌ Fehler beim Parsen der Konfiguration: {e}")
            raise

    def _get_device_name(self) -> str:
        """
        Ermittelt den Gerätenamen.
        Verwendet device_alias aus Config oder Hostname als Fallback.

        Returns:
            Gerätename (alias oder hostname)
        """
        alias = self.config.get('device_alias', '').strip()
        if alias:
            return alias
        try:
            return socket.gethostname()
        except Exception as e:
            print(f"⚠️  Warnung: Hostname konnte nicht ermittelt werden: {e}")
            return "Unbekanntes Gerät"

    def _init_monitors(self):
        """Initialisiert alle aktivierten Monitor-Module."""
        modules_config = self.config.get('modules', {})

        for module_key, module_data in modules_config.items():
            if not module_data.get('enabled', False):
                continue

            monitor_class = AVAILABLE_MONITORS.get(module_key)
            if not monitor_class:
                print(f"⚠️  Warnung: Modul '{module_key}' nicht gefunden, überspringe...")
                continue

            try:
                monitor_instance = monitor_class(
                    name=module_data.get('name', module_key),
                    icon=module_data.get('icon', '📊')
                )
                self.monitors[module_key] = monitor_instance
                print(f"✅ Modul '{module_key}' geladen: {module_data.get('name')}")
            except Exception as e:
                print(f"❌ Fehler beim Laden von Modul '{module_key}': {e}")

    async def on_ready(self):
        """Event: Bot ist bereit und eingeloggt."""
        print(f"✅ Bot eingeloggt als {self.user}")
        print(f"🖥️  Gerätename: {self.device_name}")
        print(f"📺 Channel-ID: {self.channel_id}")
        print(f"🔄 Update-Intervall: {self.update_interval}s")
        print(f"📊 Aktive Module: {len(self.monitors)}")

        if not self.is_running:
            self.is_running = True
            await self.monitor_loop()

    async def monitor_loop(self):
        """Haupt-Loop: Aktualisiert die Monitore in regelmäßigen Abständen."""
        await self.wait_until_ready()

        channel = self.get_channel(self.channel_id)
        if not channel:
            print(f"❌ Fehler: Channel {self.channel_id} nicht gefunden!")
            return

        print(f"✅ Channel gefunden: #{channel.name}")

        # Beim ersten Durchlauf: Nach bestehendem Embed suchen
        await self._find_existing_embed(channel)

        while not self.is_closed():
            try:
                # Alle Monitore prüfen
                has_updates = False
                for monitor in self.monitors.values():
                    if await monitor.check_update():
                        has_updates = True

                # Embed aktualisieren
                if has_updates or self.embed_message is None:
                    await self._update_embed(channel)

            except Exception as e:
                print(f"❌ Fehler im Monitor-Loop: {e}")

            await asyncio.sleep(self.update_interval)

    async def _find_existing_embed(self, channel: discord.TextChannel):
        """
        Sucht nach einem bestehenden Embed für dieses Gerät.
        Durchsucht die letzten 50 Nachrichten im Channel.

        Args:
            channel: Discord TextChannel zum Durchsuchen
        """
        try:
            print(f"🔍 Suche nach bestehendem Embed für '{self.device_name}'...")

            async for message in channel.history(limit=50):
                # Nur eigene Nachrichten mit Embeds prüfen
                if message.author.id == self.user.id and message.embeds:
                    embed = message.embeds[0]

                    # Prüfe ob der Gerätename im Titel vorkommt
                    if embed.title and self.device_name in embed.title:
                        self.embed_message = message
                        self.embed_message_id = message.id
                        print(f"✅ Bestehendes Embed gefunden (Message ID: {message.id})")
                        return

            print(f"ℹ️  Kein bestehendes Embed gefunden, erstelle neues...")

        except Exception as e:
            print(f"⚠️  Fehler beim Suchen nach Embed: {e}")

    async def _update_embed(self, channel: discord.TextChannel):
        """
        Erstellt oder aktualisiert das Discord-Embed mit aktuellen Werten.

        Args:
            channel: Discord TextChannel für das Embed
        """
        try:
            # Embed erstellen
            embed = discord.Embed(
                title=f"🖥️ {self.device_name}",
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow()
            )

            # Alle Monitor-Felder hinzufügen
            for monitor in self.monitors.values():
                field_data = monitor.get_field_dict()
                embed.add_field(
                    name=field_data['name'],
                    value=field_data['value'],
                    inline=field_data['inline']
                )

            embed.set_footer(text="Letzte Aktualisierung")

            # Embed senden oder aktualisieren
            if self.embed_message:
                try:
                    await self.embed_message.edit(embed=embed)
                except discord.NotFound:
                    # Nachricht wurde gelöscht, neue erstellen
                    print(f"⚠️  Alte Nachricht nicht gefunden, erstelle neue...")
                    self.embed_message = await channel.send(embed=embed)
                    self.embed_message_id = self.embed_message.id
            else:
                # Erste Nachricht erstellen
                self.embed_message = await channel.send(embed=embed)
                self.embed_message_id = self.embed_message.id
                print(f"✅ Neues Embed erstellt (Message ID: {self.embed_message_id})")

        except Exception as e:
            print(f"❌ Fehler beim Aktualisieren des Embeds: {e}")


def main():
    """Hauptfunktion: Startet den Bot."""
    print("=" * 60)
    print("   Discord System Monitor Bot - Informer")
    print("   Version 1.1.0 - Multi-Device Support")
    print("=" * 60)
    print()

    try:
        # Bot initialisieren
        bot = MonitorBot('config.json')

        # Bot Token aus Config
        token = bot.config.get('discord_token')
        if not token:
            print("❌ Fehler: 'discord_token' nicht in config.json gefunden!")
            return

        print(f"🚀 Starte Bot für Gerät: {bot.device_name}")
        print()

        # Bot starten
        bot.run(token)

    except KeyboardInterrupt:
        print("\n⏹️  Bot wurde durch Benutzer gestoppt.")
    except Exception as e:
        print(f"\n❌ Kritischer Fehler: {e}")
        raise


if __name__ == "__main__":
    main()
