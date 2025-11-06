"""
Monitors Package - Registry für alle verfügbaren Monitor-Module
"""

from monitors.base_monitor import BaseMonitor
from monitors.teamviewer_monitor import TeamViewerMonitor
from monitors.cpu_monitor import CPUMonitor

# Registry aller verfügbaren Monitore
# Key = Modul-Name in config.json
# Value = Monitor-Klasse
AVAILABLE_MONITORS = {
    'teamviewer': TeamViewerMonitor,
    'cpu': CPUMonitor,
}

__all__ = [
    'BaseMonitor',
    'TeamViewerMonitor',
    'CPUMonitor',
    'AVAILABLE_MONITORS',
]
