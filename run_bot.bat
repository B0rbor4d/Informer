@echo off
REM Informer Bot Wrapper für Windows Service
REM Startet den Bot mit vollständigem Pfad

cd /d "Z:\Coding\claude\projects\Informer"

REM UTF-8 Encoding für Python (Emoji-Support)
set PYTHONIOENCODING=utf-8

REM Python mit vollständigem Pfad (echte Python.exe, kein UWP-Alias)
"C:\Users\flori\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\python.exe" "Z:\Coding\claude\projects\Informer\discord_bot.py"

REM Fehlercode weitergeben
exit /b %errorlevel%
