@echo off
REM Informer Service Starter
REM Startet den Informer Windows-Dienst

echo ============================================
echo   Informer Discord Bot - Service Starter
echo ============================================
echo.

REM Prüfe ob als Administrator ausgeführt
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Dieses Skript muss als Administrator ausgefuehrt werden!
    echo.
    echo Rechtsklick auf diese Datei -^> "Als Administrator ausfuehren"
    echo.
    pause
    exit /b 1
)

echo [INFO] Starte Informer Service...
echo.

nssm start Informer

if %errorLevel% equ 0 (
    echo.
    echo [SUCCESS] Informer Service wurde erfolgreich gestartet!
    echo.
    echo Status pruefen:
    echo   nssm status Informer
    echo.
    echo Logs ansehen:
    echo   tail -f Z:\Coding\claude\projects\Informer\informer.log
    echo.
) else (
    echo.
    echo [ERROR] Fehler beim Starten des Services!
    echo.
    echo Troubleshooting:
    echo   1. Status pruefen: nssm status Informer
    echo   2. Logs pruefen: tail -f Z:\Coding\claude\projects\Informer\informer-error.log
    echo   3. Bot manuell testen: python Z:\Coding\claude\projects\Informer\discord_bot.py
    echo.
)

pause
