# 🚀 Schnellstart - Informer Discord Bot

Diese Anleitung führt dich in **5 Minuten** zum laufenden Bot.

## ✅ Schritt 1: Voraussetzungen prüfen

```bash
# Python-Version prüfen (muss 3.8+ sein)
python --version

# Git prüfen (optional)
git --version
```

## 📥 Schritt 2: Projekt herunterladen

### Option A: Mit Git

```bash
git clone https://github.com/B0rbor4d/Informer.git
cd Informer
```

### Option B: ZIP-Download

1. Gehe zu: https://github.com/B0rbor4d/Informer
2. Klicke "Code" → "Download ZIP"
3. Entpacke das ZIP
4. Öffne Terminal im entpackten Ordner

## 📦 Schritt 3: Dependencies installieren

```bash
pip install -r requirements.txt
```

**Windows:** Falls Fehler auftreten, versuche:
```bash
python -m pip install -r requirements.txt
```

## 🔑 Schritt 4: Discord Bot erstellen

### 4.1 Bot Token erhalten

1. Gehe zu: https://discord.com/developers/applications
2. Klicke "New Application"
3. Gib einen Namen ein (z.B. "Informer")
4. Gehe zu "Bot" (linkes Menü)
5. Klicke "Add Bot" → "Yes, do it!"
6. Klicke "Reset Token" → Kopiere den Token
7. ⚠️ **WICHTIG:** Aktiviere "Message Content Intent"

### 4.2 Bot einladen

1. Gehe zu "OAuth2" → "URL Generator"
2. Wähle Scopes: `bot`
3. Wähle Bot Permissions:
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Read Message History
4. Kopiere die generierte URL
5. Öffne URL im Browser → Wähle deinen Server

### 4.3 Channel ID herausfinden

1. Discord: Einstellungen → Erweitert → Entwicklermodus (aktivieren)
2. Rechtsklick auf deinen Channel → "ID kopieren"

## ⚙️ Schritt 5: Konfiguration

```bash
# Windows
copy config.example.json config.json

# Linux/Mac
cp config.example.json config.json
```

**Bearbeite config.json:**

```json
{
    "discord_token": "DEIN_BOT_TOKEN_HIER_EINFÜGEN",
    "channel_id": "DEINE_CHANNEL_ID_HIER_EINFÜGEN",
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

## ▶️ Schritt 6: Bot starten

```bash
# Methode 1: Direkt
python discord_bot.py

# Methode 2: Windows Batch
start_bot.bat
```

## ✅ Erfolgreich?

Du solltest jetzt sehen:
- ✅ Bot eingeloggt als [BotName]
- ✅ Channel gefunden: #[channel-name]
- 📊 Embed im Discord-Channel mit deinen Informationen

## 🎉 Fertig!

Dein Bot läuft jetzt und aktualisiert sich automatisch alle 60 Sekunden.

---

## 🔧 Nächste Schritte

### Mehrere Geräte überwachen

1. Kopiere das Projekt auf ein anderes Gerät
2. Ändere `device_alias` in config.json
3. Verwende denselben Bot-Token und Channel-ID
4. Starte den Bot

### Weitere Module aktivieren

**CPU Monitor** (benötigt psutil):

```bash
# psutil installieren
pip install psutil

# In config.json aktivieren
"cpu": {
    "enabled": true,
    "name": "CPU Auslastung",
    "icon": "💻"
}
```

### Als Windows-Dienst einrichten

Siehe Hauptdokumentation für NSSM, Task Scheduler oder Python Service Setup.

---

## ❌ Probleme?

### Bot startet nicht

```bash
# Python erneut prüfen
python --version

# Dependencies neu installieren
pip install --upgrade -r requirements.txt
```

### "Token is invalid"

- Token neu generieren im Developer Portal
- Korrekt in config.json kopiert? (keine Leerzeichen, keine Anführungszeichen am Ende)

### Bot ist online, aber sendet keine Nachricht

- Channel-ID korrekt? (Rechtsklick → ID kopieren)
- Bot-Berechtigungen im Channel prüfen
- "Message Content Intent" aktiviert im Developer Portal?

### TeamViewer ID nicht gefunden

- TeamViewer installiert und gestartet?
- Windows: Als Administrator starten

---

## 📚 Mehr Infos

- Hauptdokumentation: [README.md](../README.md)
- Eigene Module erstellen: Siehe README.md "Eigenes Modul erstellen"
- GitHub Issues: https://github.com/B0rbor4d/Informer/issues

---

**Happy Monitoring! 🎉**
