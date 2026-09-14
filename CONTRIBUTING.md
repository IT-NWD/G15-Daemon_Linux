# Mitwirken

Beiträge zu Fehlerbehebungen, Portabilität, Dokumentation und neuen Funktionen
sind willkommen.

## Fehler melden

Bitte vor einem neuen Issue nach ähnlichen Meldungen suchen. Eine gute Meldung
enthält:

- genaue Logitech-Modellbezeichnung;
- Distribution, Version, Desktop und Sitzungstyp;
- Schritte zum Reproduzieren und erwartetes Verhalten;
- Ausgabe von `g15daemon --version`;
- relevante Protokolle ohne vertrauliche Daten.

Hardwaretests dürfen einen laufenden Daemon oder LCD-Client unterbrechen. Das
im Bericht ausdrücklich erwähnen.

## Änderungen einreichen

1. Einen thematisch begrenzten Branch erstellen.
2. Änderungen modular und distributionsunabhängig halten.
3. Neue Funktionen und geändertes Verhalten auf Deutsch dokumentieren.
4. `make check` und möglichst `make distcheck` ausführen.
5. Aussagekräftige Commits im üblichen Format erstellen, zum Beispiel
   `fix(gui): installierte Modulpfade korrekt auflösen`.
6. Im Pull Request Motivation, Umsetzung und durchgeführte Tests nennen.

GUI-Code darf keinen Paketmanager voraussetzen. Plattformabhängige Funktionen
gehören hinter klar definierte Backends. Programmstarts dürfen nicht über eine
als root laufende keyd-`command()`-Aktion umgesetzt werden.

## Stil

C-Änderungen sollen zum vorhandenen Stil passen. Python-Code bleibt mit
Python 3 kompatibel und trennt Datenmodell, Backend, Plattformerkennung und
Oberfläche. Benutzertexte und aktuelle Projektdokumentation werden auf Deutsch
gepflegt; technische Bezeichner dürfen Englisch bleiben.
