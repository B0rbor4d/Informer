#!/bin/bash
# GitHub Upload Script für Linux/Mac
# Pusht das lokale Repository zu GitHub

echo "============================================"
echo "  GitHub Upload - Informer"
echo "============================================"
echo

# Git prüfen
if ! command -v git &> /dev/null; then
    echo "[ERROR] Git nicht gefunden!"
    echo "Installation:"
    echo "  Ubuntu/Debian: sudo apt install git"
    echo "  Fedora: sudo dnf install git"
    echo "  macOS: brew install git"
    exit 1
fi

echo "[OK] Git gefunden"
echo

# Status anzeigen
echo "[INFO] Git Status:"
echo
git status
echo

# Repository-Setup prüfen
if ! git remote get-url origin &> /dev/null; then
    echo "[INFO] Kein Remote 'origin' gefunden."
    echo
    read -p "GitHub Repository URL eingeben (z.B. https://github.com/Username/Informer.git): " REPO_URL

    if [ -z "$REPO_URL" ]; then
        echo "[ERROR] Keine URL eingegeben!"
        exit 1
    fi

    echo
    echo "[INFO] Füge Remote hinzu: $REPO_URL"
    git remote add origin "$REPO_URL"

    if [ $? -ne 0 ]; then
        echo "[ERROR] Konnte Remote nicht hinzufügen!"
        exit 1
    fi
fi

echo "[OK] Remote 'origin' konfiguriert"
echo

# Branch prüfen/setzen
git branch -M main

# Push durchführen
echo "[INFO] Pushe zu GitHub..."
echo

git push -u origin main

if [ $? -ne 0 ]; then
    echo
    echo "[ERROR] Push fehlgeschlagen!"
    echo
    echo "Mögliche Ursachen:"
    echo "  - Repository existiert nicht auf GitHub"
    echo "  - Keine Push-Rechte (Authentication fehlt)"
    echo "  - Netzwerkproblem"
    echo
    echo "Hilfe:"
    echo "  1. Erstelle ein leeres Repository auf GitHub: https://github.com/new"
    echo "  2. Stelle sicher, dass du angemeldet bist (git config --global user.name)"
    echo "  3. Bei HTTPS: GitHub Personal Access Token verwenden"
    echo
    exit 1
fi

echo
echo "============================================"
echo "  [SUCCESS] Upload erfolgreich!"
echo "============================================"
echo
echo "Dein Repository ist jetzt auf GitHub verfügbar."
echo
echo "Nächste Schritte:"
echo "  1. Gehe zu deinem GitHub Repository"
echo "  2. Lösche dein Personal Access Token (falls verwendet)"
echo "  3. Füge Topics hinzu: discord, bot, python, monitoring"
echo "  4. Setze eine Description"
echo
