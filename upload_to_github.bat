@echo off
REM GitHub Upload Script für Windows
REM Pusht das lokale Repository zu GitHub

echo ============================================
echo   GitHub Upload - Informer
echo ============================================
echo.

REM Git prüfen
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git nicht gefunden!
    echo Bitte Git installieren: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo [OK] Git gefunden
echo.

REM Status anzeigen
echo [INFO] Git Status:
echo.
git status
echo.

REM Repository-Setup prüfen
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo [INFO] Kein Remote 'origin' gefunden.
    echo.
    set /p REPO_URL="GitHub Repository URL eingeben (z.B. https://github.com/Username/Informer.git): "

    if "!REPO_URL!"=="" (
        echo [ERROR] Keine URL eingegeben!
        pause
        exit /b 1
    )

    echo.
    echo [INFO] Füge Remote hinzu: !REPO_URL!
    git remote add origin !REPO_URL!

    if errorlevel 1 (
        echo [ERROR] Konnte Remote nicht hinzufügen!
        pause
        exit /b 1
    )
)

echo [OK] Remote 'origin' konfiguriert
echo.

REM Branch prüfen/setzen
git branch -M main

REM Push durchführen
echo [INFO] Pushe zu GitHub...
echo.

git push -u origin main

if errorlevel 1 (
    echo.
    echo [ERROR] Push fehlgeschlagen!
    echo.
    echo Mögliche Ursachen:
    echo   - Repository existiert nicht auf GitHub
    echo   - Keine Push-Rechte (Authentication fehlt)
    echo   - Netzwerkproblem
    echo.
    echo Hilfe:
    echo   1. Erstelle ein leeres Repository auf GitHub: https://github.com/new
    echo   2. Stelle sicher, dass du angemeldet bist (git config --global user.name)
    echo   3. Bei HTTPS: GitHub Personal Access Token verwenden
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   [SUCCESS] Upload erfolgreich!
echo ============================================
echo.
echo Dein Repository ist jetzt auf GitHub verfügbar.
echo.
echo Nächste Schritte:
echo   1. Gehe zu deinem GitHub Repository
echo   2. Lösche dein Personal Access Token (falls verwendet)
echo   3. Füge Topics hinzu: discord, bot, python, monitoring
echo   4. Setze eine Description
echo.

pause
