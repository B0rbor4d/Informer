@echo off
REM Informer Service Installer
REM Installiert den Informer Discord Bot als Windows-Dienst

echo ============================================
echo   Informer Discord Bot - Service Installer
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

echo [INFO] Entferne existierenden Service falls vorhanden...
nssm stop Informer >nul 2>&1
nssm remove Informer confirm >nul 2>&1

echo [INFO] Erstelle Service...
echo.

REM Service installieren mit Batch-Wrapper
nssm install Informer "Z:\Coding\claude\projects\Informer\run_bot.bat"

REM Service konfigurieren
nssm set Informer AppDirectory "Z:\Coding\claude\projects\Informer"
nssm set Informer AppExit Default Restart
nssm set Informer AppStdout "Z:\Coding\claude\projects\Informer\informer.log"
nssm set Informer AppStderr "Z:\Coding\claude\projects\Informer\informer-error.log"
nssm set Informer AppRotateFiles 1
nssm set Informer AppRotateBytes 1048576
nssm set Informer Description "Discord System Monitor Bot - Multi-Device Support"
nssm set Informer DisplayName "Informer"
nssm set Informer Start SERVICE_AUTO_START

echo.
echo [WICHTIG] Service-Konto konfigurieren
echo.
echo Python ist nur fuer deinen Benutzer installiert, nicht systemweit.
echo Der Service muss unter deinem Benutzerkonto laufen.
echo.
echo Bitte waehle eine Option:
echo.
echo 1. Automatisch konfigurieren (Passwort wird abgefragt)
echo 2. Manuell in Services-GUI konfigurieren
echo 3. Service vorerst nicht starten
echo.
set /p CHOICE="Deine Wahl [1/2/3]: "

if "%CHOICE%"=="1" (
    echo.
    echo [INFO] Automatische Konfiguration...
    echo.

    set USERNAME_INPUT=%USERNAME%
    set /p USERNAME_INPUT="Benutzername [%USERNAME%]: "
    if "%USERNAME_INPUT%"=="" set USERNAME_INPUT=%USERNAME%

    echo.
    set /p PASSWORD="Windows-Passwort fuer %COMPUTERNAME%\%USERNAME_INPUT%: "

    if "%PASSWORD%"=="" (
        echo.
        echo [ERROR] Passwort darf nicht leer sein!
        echo Bitte Service manuell konfigurieren.
        pause
        exit /b 1
    )

    echo.
    echo [INFO] Setze Service-Konto...
    nssm set Informer ObjectName ".\%USERNAME_INPUT%" "%PASSWORD%"

    if %errorLevel% equ 0 (
        echo [SUCCESS] Service-Konto konfiguriert!
        echo.
        echo [INFO] Starte Service...
        nssm start Informer

        timeout /t 3 >nul

        echo.
        nssm status Informer
        echo.
        echo [INFO] Log pruefen:
        echo   type Z:\Coding\claude\projects\Informer\informer.log
        echo.
    ) else (
        echo.
        echo [ERROR] Fehler beim Konfigurieren!
        echo Bitte manuell konfigurieren oder Passwort pruefen.
        echo.
    )
) else if "%CHOICE%"=="2" (
    echo.
    echo [INFO] Manuelle Konfiguration:
    echo.
    echo 1. services.msc oeffnen
    echo 2. "Informer" Service suchen
    echo 3. Rechtsklick -^> Eigenschaften
    echo 4. Tab "Anmelden"
    echo 5. "Dieses Konto" auswaehlen
    echo 6. Benutzerkonto eingeben: %COMPUTERNAME%\%USERNAME%
    echo 7. Passwort eingeben
    echo 8. OK klicken
    echo 9. Service starten
    echo.
    echo Danach starten mit: nssm start Informer
    echo.
) else (
    echo.
    echo [INFO] Service installiert aber nicht gestartet.
    echo.
    echo Zum Konfigurieren und Starten:
    echo   1. Benutzerkonto setzen (siehe Option 1 oder 2)
    echo   2. Service starten: nssm start Informer
    echo.
)

echo ============================================
echo   Installation abgeschlossen
echo ============================================
echo.
pause
