@echo off
REM Informer Service Stopper
REM Stoppt den Informer Windows-Dienst

echo ============================================
echo   Informer Discord Bot - Service Stopper
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

echo [INFO] Stoppe Informer Service...
echo.

nssm stop Informer

if %errorLevel% equ 0 (
    echo.
    echo [SUCCESS] Informer Service wurde erfolgreich gestoppt!
    echo.
) else (
    echo.
    echo [WARNUNG] Service war moeglicherweise bereits gestoppt
    echo.
)

echo Status pruefen:
echo   nssm status Informer
echo.

pause
