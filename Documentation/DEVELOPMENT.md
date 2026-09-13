# Entwicklung und Paketierung

## Komponenten

| Verzeichnis | Aufgabe | Plattformabhängigkeit |
|---|---|---|
| `g15daemon/` | Daemon, Hardwaresteuerung und Konfigurationsparser | libg15 |
| `plugins/` | LCD-, Netzwerk- und UINPUT-Plugins | UINPUT nur unter Linux |
| `gui/g15_profile.py` | Profil-Datenmodell | keine |
| `gui/g15_keyd.py` | keyd-Import, Export und Prüfung | keyd |
| `gui/g15_platform.py` | Werkzeug- und Pfaderkennung | Backend-spezifisch |
| `gui/g15-profile-editor.in` | GTK-4-Oberfläche | PyGObject/GTK 4 |
| `gui/g15-profile-install` | privilegierte Linux-Übernahme | keyd/Polkit |
| `tests/` | C-, Konfigurations- und Python-Tests | teilweise keyd |

Ein weiteres Eingabe-Backend soll das Datenmodell verwenden und seine eigene
Serialisierung, Validierung und Systemübernahme bereitstellen. GTK-Code darf
keine distributionsspezifischen Paketmanager oder absolute Programmpfade
enthalten.

## Bauen

Benötigt werden ein C-Compiler, Autoconf, Automake, libtool, pkg-config sowie
die Entwicklungsdateien von libg15 und libg15render. Für die GUI kommen
Python 3, PyGObject und GTK 4 hinzu; keyd und Polkit sind nur für die
Linux-Profilaktivierung nötig.

```bash
autoreconf --force --install
./configure --prefix=/usr --sbindir=/usr/bin
make
make check
```

Eine Paket-Probeinstallation ohne Änderung des laufenden Systems ist möglich
mit:

```bash
make DESTDIR=/tmp/g15daemon-package install
```

## Tests

`make check` umfasst den Parser der Starthelligkeit, die statische
Daemon-/keyd-Konfiguration, den Profil-Roundtrip und die Textänderungen des
privilegierten Helfers. Ist keyd vorhanden, wird zusätzlich dessen eigener
Syntaxprüfer ausgeführt.

Hardwaretests sind bewusst nicht Teil der automatischen Tests: Sie benötigen
exklusiven USB-Zugriff und würden einen laufenden g15daemon samt LCD-Clients
unterbrechen.

## Konfigurierbare Pfade

Die GUI unterstützt folgende Laufzeit-Overrides für Paketierung und Tests:

| Variable | Bedeutung |
|---|---|
| `G15_PROFILE_PATH` | Benutzerdatei statt `$XDG_CONFIG_HOME/g15daemon/g15.conf` |
| `G15_KEYD` | Pfad zum keyd-Programm |
| `G15_PKEXEC` | Pfad zum Polkit-Frontend |
| `G15_INSTALL_HELPER` | alternativer privilegierter Helfer |

Ohne Overrides werden XDG-Verzeichnisse und die Programmsuche des Systems
verwendet. Dadurch bleibt die Anwendung unabhängig von Arch, CachyOS, Debian,
Fedora oder deren konkreten Installationspfaden.
