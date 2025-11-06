@echo off
REM Windows Schnellstart-Skript für Informer Discord Bot
REM Prüft Dependencies und startet den Bot

echo ============================================
echo   Informer Discord Bot - Schnellstart
echo ============================================
echo.

REM Python-Version prüfen
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python nicht gefunden!
    echo Bitte Python 3.8+ installieren: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python gefunden
echo.

REM Config prüfen
if not exist "config.json" (
    echo [WARNUNG] config.json nicht gefunden!
    echo.
    echo Bitte erstellen Sie eine config.json aus config.example.json:
    echo   1. Kopieren: copy config.example.json config.json
    echo   2. Bearbeiten: notepad config.json
    echo   3. Bot-Token und Channel-ID eintragen
    echo.
    pause
    exit /b 1
)

echo [OK] config.json gefunden
echo.

REM Dependencies prüfen
echo Prüfe Dependencies...
pip show discord.py >nul 2>&1
if errorlevel 1 (
    echo [INFO] discord.py nicht installiert, installiere Dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Installation fehlgeschlagen!
        pause
        exit /b 1
    )
) else (
    echo [OK] Dependencies bereits installiert
)

echo.
echo ============================================
echo   Starte Bot...
echo ============================================
echo.

REM Bot starten
python discord_bot.py

REM Bei Fehler warten
if errorlevel 1 (
    echo.
    echo [ERROR] Bot wurde mit Fehler beendet
    pause
)
