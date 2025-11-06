# Informer - Fehlerbehebung

Dieses Dokument beschreibt häufige Probleme und deren Lösungen beim Einrichten des Informer Discord Bots als Windows-Dienst.

## Inhaltsverzeichnis

1. [Service startet nicht (SERVICE_PAUSED)](#service-startet-nicht-service_paused)
2. [Discord Connection Fehler (Privileged Intents)](#discord-connection-fehler-privileged-intents)
3. [Unicode/Emoji Fehler](#unicodeemoji-fehler)
4. [Python nicht gefunden](#python-nicht-gefunden)

---

## Service startet nicht (SERVICE_PAUSED)

### Problem

Nach `nssm start Informer` zeigt der Status `SERVICE_PAUSED` oder der Service stoppt sofort.

**Error Log:**
```
Das angegebene Programm kann nicht ausgeführt werden.
```

### Ursache

Python ist nur für deinen Benutzer installiert (Microsoft Store Version), nicht systemweit.
Der Windows-Dienst läuft standardmäßig als `LocalSystem` und kann nicht auf benutzerspezifische Programme zugreifen.

### Lösung: Service unter Benutzerkonto ausführen

#### Option 1: Automatischer Installer (Empfohlen)

Führe `install_service.bat` als Administrator aus:

```batch
# Rechtsklick auf install_service.bat → "Als Administrator ausführen"
# Wähle Option 1 für automatische Konfiguration
# Gib dein Windows-Passwort ein
```

#### Option 2: Manuelle Konfiguration über Services-GUI

1. **Services öffnen:**
   - `Win + R` → `services.msc` → Enter

2. **Informer Service finden:**
   - Suche "Informer" in der Liste

3. **Anmeldeinformationen konfigurieren:**
   - Rechtsklick auf "Informer" → **Eigenschaften**
   - Tab **"Anmelden"**
   - Wähle **"Dieses Konto"**
   - Gib ein: `.\flori` (oder `COMPUTERNAME\flori`)
   - Gib dein Windows-Passwort ein
   - **OK** klicken

4. **Service starten:**
   ```batch
   nssm start Informer
   nssm status Informer
   ```

#### Option 3: Kommandozeile

```batch
# Als Administrator ausführen:
nssm set Informer ObjectName ".\flori" "DEIN_PASSWORT"
nssm start Informer
```

### Verifizierung

```batch
nssm status Informer
# Sollte zeigen: SERVICE_RUNNING

type Z:\Coding\claude\projects\Informer\informer.log
# Sollte Bot-Startup-Meldungen zeigen
```

---

## Discord Connection Fehler (Privileged Intents)

### Problem

**Error:**
```
discord.errors.PrivilegedIntentsRequired: Shard ID None is requesting privileged intents
that have not been explicitly enabled in the developer portal.
```

### Ursache

Der Bot benötigt **Message Content Intent**, das im Discord Developer Portal nicht aktiviert ist.

### Lösung

1. **Discord Developer Portal öffnen:**
   - https://discord.com/developers/applications/

2. **Deine Application auswählen:**
   - Klicke auf deinen Bot (z.B. "Informer")

3. **Bot-Einstellungen öffnen:**
   - Linkes Menü → **"Bot"**

4. **Privileged Gateway Intents aktivieren:**
   - Scrolle zu **"Privileged Gateway Intents"**
   - Aktiviere: ✅ **Message Content Intent**
   - Klicke **"Save Changes"**

5. **Bot neu starten:**
   ```batch
   nssm restart Informer
   ```

### Wichtig

Ohne **Message Content Intent** kann der Bot keine Nachrichten lesen und funktioniert nicht!

---

## Unicode/Emoji Fehler

### Problem

**Error:**
```
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 0
```

### Ursache

Windows Console verwendet standardmäßig CP1252-Encoding, kann aber UTF-8 Emojis nicht darstellen.

### Lösung

Diese Fehler wurden bereits behoben durch:

1. **Umgebungsvariable in `run_bot.bat`:**
   ```batch
   set PYTHONIOENCODING=utf-8
   ```

2. **Try-Catch in `discord_bot.py`:**
   ```python
   if sys.platform == 'win32':
       try:
           sys.stdout.reconfigure(encoding='utf-8')
           sys.stderr.reconfigure(encoding='utf-8')
       except (AttributeError, OSError):
           pass  # PYTHONIOENCODING wird verwendet
   ```

Wenn der Fehler trotzdem auftritt:

```batch
# Windows Terminal mit UTF-8 Support verwenden statt cmd.exe
# ODER in cmd.exe:
chcp 65001
python discord_bot.py
```

---

## Python nicht gefunden

### Problem

**Error:**
```
'python' wird nicht als interner oder externer Befehl erkannt
```

### Ursache

Python ist nicht im System-PATH oder nicht systemweit installiert.

### Lösung 1: Python-Pfad in `run_bot.bat` prüfen

Öffne `run_bot.bat` und stelle sicher, dass der Python-Pfad korrekt ist:

```batch
"C:\Users\flori\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\python.exe"
```

### Lösung 2: Python-Installation prüfen

```batch
# Finde Python:
where python

# Zeige tatsächlichen Python-Pfad:
python -c "import sys; print(sys.executable)"
```

Aktualisiere `run_bot.bat` mit dem korrekten Pfad falls nötig.

---

## Nützliche Befehle

### Service-Management

```batch
# Status prüfen
nssm status Informer

# Service starten
nssm start Informer

# Service stoppen
nssm stop Informer

# Service neu starten
nssm restart Informer

# Service-Konfiguration anzeigen
nssm dump Informer

# Service entfernen
nssm remove Informer confirm
```

### Logs prüfen

```batch
# Stdout-Log
type Z:\Coding\claude\projects\Informer\informer.log

# Stderr-Log (Fehler)
type Z:\Coding\claude\projects\Informer\informer-error.log

# Log live verfolgen (mit PowerShell)
Get-Content Z:\Coding\claude\projects\Informer\informer.log -Wait
```

### Bot manuell testen

```batch
cd Z:\Coding\claude\projects\Informer
python discord_bot.py

# Mit timeout (5 Sekunden)
timeout 5 python discord_bot.py
```

---

## Häufige Fehlerdiagnose

### 1. Service startet nicht

```batch
# Prüfe Service-Status
nssm status Informer

# Prüfe Error-Log
type Z:\Coding\claude\projects\Informer\informer-error.log

# Teste Bot manuell
python Z:\Coding\claude\projects\Informer\discord_bot.py
```

### 2. Bot verbindet nicht zu Discord

```batch
# Prüfe stdout-Log nach Fehlern
type Z:\Coding\claude\projects\Informer\informer.log

# Häufigste Ursachen:
# - Falscher Discord Token in config.json
# - Message Content Intent nicht aktiviert
# - Keine Internetverbindung
```

### 3. Monitor zeigt keine Daten

```batch
# Prüfe config.json:
# - Ist das Modul "enabled": true?
# - Ist RustDesk/TeamViewer installiert?

# Für RustDesk:
rustdesk.exe --get-id

# Für TeamViewer:
# Prüfe Registry: HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\TeamViewer
```

---

## Weitere Hilfe

Bei anhaltenden Problemen:

1. **Logs sammeln:**
   ```batch
   type Z:\Coding\claude\projects\Informer\informer.log > debug.txt
   type Z:\Coding\claude\projects\Informer\informer-error.log >> debug.txt
   nssm dump Informer >> debug.txt
   ```

2. **GitHub Issues:**
   - Öffne ein Issue im GitHub-Repository mit den Logs

3. **Manuelle Ausführung:**
   ```batch
   # Als Fallback: Bot ohne Service starten
   cd Z:\Coding\claude\projects\Informer
   python discord_bot.py
   ```
