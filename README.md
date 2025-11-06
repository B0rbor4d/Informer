# 🖥️ Informer - Discord System Monitor Bot

**Version 1.1.0** - Multi-Device Support

Ein modularer Discord-Bot zur Überwachung von System-Informationen. Zeigt Daten wie TeamViewer ID, CPU-Auslastung und mehr in einem Discord-Channel an.

## ✨ Features

- ✅ **Multi-Device Support** - Mehrere Geräte gleichzeitig im selben Channel
- ✅ **TeamViewer Integration** - Zeigt aktuelle TeamViewer ID an
- ✅ **Modulares System** - Einfach erweiterbar mit neuen Monitor-Modulen
- ✅ **Discord Embeds** - Jedes Gerät hat sein eigenes ansprechendes Embed
- ✅ **Automatische Updates** - Konfigurierbare Update-Intervalle
- ✅ **Embed-Wiederverwendung** - Bei Neustart wird bestehendes Embed gefunden

## 📋 Voraussetzungen

- **Python 3.8+**
- **Discord Bot Token** (siehe [Discord Developer Portal](https://discord.com/developers/applications))
- **Git** (optional, für Versionskontrolle)

### Windows-spezifisch:
- pywin32 (für TeamViewer Registry-Zugriff)

### Optional:
- psutil (für CPU Monitor)

## 🚀 Schnellstart

### 1. Repository klonen (oder herunterladen)

```bash
git clone https://github.com/B0rbor4d/Informer.git
cd Informer
```

### 2. Dependencies installieren

```bash
pip install -r requirements.txt
```

### 3. Konfiguration erstellen

```bash
# Windows
copy config.example.json config.json

# Linux/Mac
cp config.example.json config.json
```

### 4. Konfiguration anpassen

Öffne `config.json` und trage ein:

```json
{
    "discord_token": "DEIN_BOT_TOKEN",
    "channel_id": "DEINE_CHANNEL_ID",
    "device_alias": "Mein PC",
    "update_interval": 60,
    "modules": {
        "teamviewer": {
            "enabled": true,
            "name": "TeamViewer ID",
            "icon": "🖥️"
        }
    }
}
```

#### Discord Bot Token erhalten:
1. Gehe zu [Discord Developer Portal](https://discord.com/developers/applications)
2. Erstelle eine neue Application
3. Gehe zu "Bot" → "Add Bot"
4. Kopiere den Token unter "TOKEN"
5. Aktiviere "Message Content Intent" unter "Privileged Gateway Intents"

#### Channel ID herausfinden:
1. Discord Developer Mode aktivieren: Einstellungen → Erweitert → Entwicklermodus
2. Rechtsklick auf den gewünschten Channel → "ID kopieren"

### 5. Bot starten

```bash
# Direkt mit Python
python discord_bot.py

# Oder mit Windows Batch-Datei
start_bot.bat
```

## 📦 Projektstruktur

```
Informer/
├── discord_bot.py              # Haupt-Bot mit Multi-Device Logic
├── config.example.json         # Config-Template
├── requirements.txt            # Python Dependencies
├── start_bot.bat              # Windows Schnellstart
├── upload_to_github.bat       # GitHub Upload (Windows)
├── upload_to_github.sh        # GitHub Upload (Linux/Mac)
├── LICENSE                    # MIT License
├── .gitignore                # Git Ignore Rules
│
├── monitors/                  # Monitor-Module
│   ├── __init__.py           # Modul-Registry
│   ├── base_monitor.py       # Abstract Base Class
│   ├── teamviewer_monitor.py # TeamViewer ID Monitor
│   └── cpu_monitor.py        # CPU Monitor (Beispiel)
│
└── docs/                      # Dokumentation
    └── README.md
```

## 🔧 Konfiguration

### config.json Parameter

| Parameter | Typ | Beschreibung | Beispiel |
|-----------|-----|--------------|----------|
| `discord_token` | String | Bot-Token von Discord Developer Portal | `"MTA1N..."` |
| `channel_id` | String | ID des Discord-Channels | `"123456789"` |
| `device_alias` | String | Optionaler Name für das Gerät (leer = Hostname) | `"Haupt-PC"` |
| `update_interval` | Number | Sekunden zwischen Updates (min. 30 empfohlen) | `60` |
| `modules` | Object | Dictionary mit aktivierten Modulen | siehe unten |

### Module konfigurieren

```json
{
    "modules": {
        "module_key": {
            "enabled": true,
            "name": "Anzeige-Name",
            "icon": "📊"
        }
    }
}
```

#### Verfügbare Module:

**teamviewer** - TeamViewer ID anzeigen
```json
"teamviewer": {
    "enabled": true,
    "name": "TeamViewer ID",
    "icon": "🖥️"
}
```

**cpu** - CPU-Auslastung (benötigt psutil)
```json
"cpu": {
    "enabled": true,
    "name": "CPU Auslastung",
    "icon": "💻"
}
```

## 🖥️ Multi-Device Setup

Um mehrere Geräte gleichzeitig zu überwachen:

1. **Gleiche Konfiguration** auf allen Geräten:
   - Gleicher `discord_token`
   - Gleiche `channel_id`

2. **Unterschiedliche Namen** pro Gerät:
   - Setze `device_alias` auf einen eindeutigen Namen
   - Oder lasse leer für automatischen Hostname

3. **Bot auf jedem Gerät starten**

**Beispiel:**

```json
// Gerät 1 - PC
{
    "device_alias": "Haupt-PC",
    ...
}

// Gerät 2 - Laptop
{
    "device_alias": "🖥️ Laptop",
    ...
}

// Gerät 3 - Server
{
    "device_alias": "",  // Verwendet Hostname
    ...
}
```

## 🧩 Eigenes Modul erstellen

### 1. Neue Datei in `monitors/` erstellen

```python
# monitors/mein_modul.py
from typing import Optional
from monitors.base_monitor import BaseMonitor

class MeinModul(BaseMonitor):
    """Beschreibung deines Moduls"""

    async def get_value(self) -> Optional[str]:
        """Hauptlogik - gibt aktuellen Wert zurück"""
        try:
            # Deine Logik hier
            wert = "Beispiel-Wert"
            return wert
        except Exception as e:
            print(f"Fehler: {e}")
            return None

    def format_value(self, value: Optional[str]) -> str:
        """Optional: Custom Formatierung"""
        if value is None:
            return '❌ Nicht verfügbar'
        return f'**{value}**'
```

### 2. Modul registrieren in `monitors/__init__.py`

```python
from monitors.mein_modul import MeinModul

AVAILABLE_MONITORS = {
    'teamviewer': TeamViewerMonitor,
    'cpu': CPUMonitor,
    'mein_modul': MeinModul,  # NEU
}
```

### 3. Modul in config.json aktivieren

```json
{
    "modules": {
        "mein_modul": {
            "enabled": true,
            "name": "Mein Custom Modul",
            "icon": "🔥"
        }
    }
}
```

## 🐛 Troubleshooting

### Bot startet nicht

```bash
# Python-Version prüfen (muss 3.8+ sein)
python --version

# Dependencies prüfen
pip list | grep discord

# Config prüfen
cat config.json  # Linux/Mac
type config.json  # Windows
```

### TeamViewer ID nicht gefunden

**Windows:**
- Als Administrator starten
- TeamViewer muss installiert und gestartet sein

**Linux:**
- Config-Datei muss existieren: `/opt/teamviewer/config/global.conf`

### Embed wird nicht aktualisiert

- Prüfe Bot-Berechtigungen im Channel:
  - ✅ Nachrichten senden
  - ✅ Embed Links
  - ✅ Nachrichtenverlauf lesen
- Prüfe Update-Intervall (nicht unter 30 Sekunden)
- Prüfe Discord Rate Limits (max. 5 Updates/Sekunde)

### Git-Probleme

```bash
# Remote prüfen
git remote -v

# Remote neu setzen
git remote remove origin
git remote add origin https://github.com/Username/Informer.git
```

## 📚 Weitere Dokumentation

- **CHANGELOG.md** - Alle Änderungen und Versionen
- **docs/** - Erweiterte Dokumentation und Guides

## 🤝 Contributing

Beiträge sind willkommen!

1. Fork das Repository
2. Erstelle einen Feature Branch (`git checkout -b feature/MeinFeature`)
3. Commit deine Änderungen (`git commit -m 'Füge MeinFeature hinzu'`)
4. Push zum Branch (`git push origin feature/MeinFeature`)
5. Erstelle einen Pull Request

## 📄 Lizenz

MIT License - siehe [LICENSE](LICENSE) Datei

## 🔗 Links

- **GitHub Repository:** https://github.com/B0rbor4d/Informer
- **Discord Developer Portal:** https://discord.com/developers/applications
- **Python Download:** https://www.python.org/downloads/
- **Git Download:** https://git-scm.com/downloads

## 💡 Support

Bei Fragen oder Problemen:
- Erstelle ein [GitHub Issue](https://github.com/B0rbor4d/Informer/issues)
- Prüfe die Dokumentation in `docs/`

---

**Erstellt mit ❤️ für Multi-Device System Monitoring**
