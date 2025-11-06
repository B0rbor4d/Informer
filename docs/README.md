# 📚 Informer - Dokumentation

Willkommen zur Dokumentation des Informer Discord System Monitor Bots.

## 📖 Verfügbare Dokumente

### Einstieg

- **[SCHNELLSTART.md](SCHNELLSTART.md)** - 5-Minuten-Anleitung zum ersten laufenden Bot
- **[../README.md](../README.md)** - Vollständige Projekt-Dokumentation

### Setup-Guides

Weitere Dokumentation wird bei Bedarf hinzugefügt:

- Multi-Device Setup-Beispiele
- Windows Service-Konfiguration
- Migration von alten Versionen
- GitHub Upload-Anleitung

## 🎯 Welches Dokument brauchst du?

### "Ich will schnell starten!"
→ [SCHNELLSTART.md](SCHNELLSTART.md)

### "Ich will alles verstehen!"
→ [../README.md](../README.md)

### "Ich will mehrere Geräte überwachen!"
→ Siehe README.md → "Multi-Device Setup"

### "Ich will ein eigenes Modul erstellen!"
→ Siehe README.md → "Eigenes Modul erstellen"

### "Ich habe Probleme!"
→ Siehe README.md → "Troubleshooting"

## 🔧 Architektur-Übersicht

```
┌─────────────────────────────────────────────┐
│         discord_bot.py (Haupt-Bot)          │
│  - Multi-Device Support                     │
│  - Embed-Verwaltung                         │
│  - Update-Loop                              │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│         monitors/ (Module-System)           │
│  ┌────────────────────────────────────────┐ │
│  │  base_monitor.py (Abstract Base)      │ │
│  └────────────┬───────────────────────────┘ │
│               │                              │
│       ┌───────┴────────┬──────────────┐     │
│       ▼                ▼              ▼     │
│  teamviewer_monitor  cpu_monitor   [neu]   │
└─────────────────────────────────────────────┘
```

## 🧩 Modulares System

Jedes Monitor-Modul:

1. **Erbt von `BaseMonitor`**
   - Implementiert `get_value()` - Ermittelt aktuellen Wert
   - Optional: Überschreibt `format_value()` - Custom Formatierung

2. **Wird registriert in `monitors/__init__.py`**
   - Eintrag in `AVAILABLE_MONITORS` Dictionary

3. **Wird aktiviert in `config.json`**
   - Konfiguration pro Modul: enabled, name, icon

## 📝 Changelog

### Version 1.1.0
- ✅ Multi-Device Support
- ✅ Automatische Embed-Wiederverwendung
- ✅ Socket-basierter Hostname-Fallback
- ✅ Modulare Monitor-Architektur

### Version 1.0.0
- ✅ Basis-Bot mit TeamViewer Monitor
- ✅ Discord Embed-Integration
- ✅ Konfigurierbare Updates

## 🤝 Beitragen

Möchtest du zur Dokumentation beitragen?

1. Fork das Repository
2. Erstelle/bearbeite Markdown-Dateien in `docs/`
3. Pull Request erstellen

### Dokumentations-Style-Guide

- **Überschriften:** Emoji + Titel
- **Code-Blöcke:** Mit Syntax-Highlighting
- **Listen:** Klare Bullet Points
- **Struktur:** Logischer Aufbau von einfach zu komplex

## 🔗 Externe Links

- **Discord.py Dokumentation:** https://discordpy.readthedocs.io/
- **Discord Developer Portal:** https://discord.com/developers/applications
- **Python Docs:** https://docs.python.org/3/

---

**Hinweis:** Diese Dokumentation wächst mit dem Projekt. Neue Guides werden bei Bedarf hinzugefügt.
