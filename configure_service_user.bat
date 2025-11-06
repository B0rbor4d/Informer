@echo off
REM Informer Service - Benutzer-Konfiguration
REM Konfiguriert den Service, um unter deinem Benutzerkonto zu laufen

echo ============================================
echo   Informer Service - Benutzer-Konfiguration
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

echo [INFO] Stoppe Service falls er laeuft...
nssm stop Informer >nul 2>&1

echo [INFO] Konfiguriere Service fuer Benutzerkonto...
echo.

REM Hole aktuellen Benutzernamen
set USERNAME_INPUT=%USERNAME%
set /p USERNAME_INPUT="Benutzername [%USERNAME%]: "
if "%USERNAME_INPUT%"=="" set USERNAME_INPUT=%USERNAME%

REM Frage nach Passwort (wird nicht angezeigt)
echo.
echo WICHTIG: Dein Windows-Passwort wird sicher in Windows gespeichert
echo und ist nicht in dieser Batch-Datei sichtbar.
echo.
set /p PASSWORD="Windows-Passwort fuer %COMPUTERNAME%\%USERNAME_INPUT%: "

if "%PASSWORD%"=="" (
    echo.
    echo [ERROR] Passwort darf nicht leer sein!
    echo.
    pause
    exit /b 1
)

REM Setze ObjectName mit Benutzerkonto
echo.
echo [INFO] Setze Service-Konto auf: %COMPUTERNAME%\%USERNAME_INPUT%
nssm set Informer ObjectName ".\%USERNAME_INPUT%" "%PASSWORD%"

if %errorLevel% equ 0 (
    echo [SUCCESS] Service-Konto erfolgreich konfiguriert!
    echo.
    echo [INFO] Starte Service...
    nssm start Informer

    timeout /t 3 >nul

    echo.
    echo [INFO] Service-Status:
    nssm status Informer
    echo.
    echo [INFO] Log pruefen:
    echo   type Z:\Coding\claude\projects\Informer\informer.log
    echo.
) else (
    echo.
    echo [ERROR] Fehler beim Konfigurieren des Service-Kontos!
    echo.
    echo Moegliche Ursachen:
    echo   - Falsches Passwort
    echo   - Benutzer hat keine "Als Dienst anmelden"-Berechtigung
    echo.
    echo Loesung:
    echo   1. Richtiges Passwort eingeben
    echo   2. In secpol.msc: "Lokale Richtlinien" -^> "Zuweisen von Benutzerrechten"
    echo      -^> "Als Dienst anmelden" -^> Benutzer hinzufuegen
    echo.
)

pause
