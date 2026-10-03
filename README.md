# G15 Daemon für Linux

Dieses Projekt erweitert den G15Daemon um eine moderne, deutschsprachige
Konfiguration für die erste Logitech G15 mit blauer Beleuchtung. Es steuert
LCD und Tastaturbeleuchtung und stellt die 18 G-Tasten über drei M-Ebenen als
54 frei konfigurierbare Belegungen bereit.

> Unterstütztes Referenzgerät: Logitech G15 v1 mit G1–G18, M1–M3, MR und
> blauer Beleuchtung. Die LCD-Tasten einschließlich des runden
> Applet-Umschalters sind vom G-Tasten-Profil getrennt.

## Funktionen

- LCD-Daemon mit Uhr-, Netzwerk- und UINPUT-Plugin
- Uhr mit deutscher Datumsanzeige und festem 24-Stunden-Format
- konfigurierbare Starthelligkeit von 0 bis 2, standardmäßig Stufe 2
- GTK-4-Profileditor nach dem Bedienprinzip der Logitech-Windows-Software
- 54 Belegungen für G1–G18 in den Ebenen M1, M2 und M3
- Einzeltasten, Tastenkombinationen, Makros und wiederholte Makros
- Import und Export lesbarer Profile
- Kopieren, Deaktivieren und Zurücksetzen kompletter M-Ebenen
- sichere systemweite Übernahme über Polkit und keyd
- modular getrenntes Datenmodell, keyd-Backend und Plattformerkennung
- automatische Builds mit GCC und Clang

## Voraussetzungen

Zum Bauen des Daemons werden ein C-Compiler, Autoconf, Automake, libtool,
pkg-config sowie die Entwicklungsdateien von `libg15` und `libg15render`
benötigt.

Der grafische Editor benötigt zusätzlich:

- Python 3
- PyGObject und GTK 4
- keyd für die G-Tasten-Profile unter Linux
- Polkit mit `pkexec` für die systemweite Übernahme

Die konkreten Paketnamen unterscheiden sich je nach Distribution. Das Projekt
ist nicht an CachyOS oder einen bestimmten Paketmanager gebunden.

## Bauen und testen

```bash
git clone https://github.com/IT-NWD/G15-Daemon_Linux.git
cd G15-Daemon_Linux
autoreconf --force --install
./configure --prefix=/usr --sbindir=/usr/bin
make
make check
```

Mit `make distcheck` wird zusätzlich geprüft, ob sich ein vollständiges
Quellarchiv bauen, testen, installieren und wieder entfernen lässt.

## Installation

```bash
sudo make install
```

Die Einrichtung eines Systemdienstes ist distributionsabhängig. Eine
Beispielkonfiguration liegt unter `contrib/init/`; Paketbetreuer sollten
Programm- und Pluginpfade an das jeweilige Zielsystem anpassen.

Zum manuellen Test kann der Daemon im Vordergrund gestartet werden:

```bash
sudo g15daemon --debug
```

Ein bereits laufender Daemon lässt sich mit `sudo g15daemon --kill` beenden.

## Grafischer Profileditor

Nach der Installation startet die Oberfläche mit:

```bash
g15-profile-editor
```

Der Editor schreibt mit **Speichern** zunächst nur die Benutzerdatei
`~/.config/g15daemon/g15.conf`. **Systemweit übernehmen …** prüft das Profil,
sichert eine vorhandene Konfiguration und installiert es über einen getrennten
Polkit-Helfer für keyd. Der Daemon wird dabei absichtlich nicht automatisch
neu gestartet; eine geänderte Starthelligkeit gilt beim nächsten kontrollierten
Start.

Eine ausführliche Beschreibung der Profile, Makros und Sicherheitsgrenzen
steht in [G15-PROFILES.md](Documentation/G15-PROFILES.md).

## Manuelle keyd-Einrichtung

Vor der Installation muss die Geräte-ID mit `sudo keyd monitor` ermittelt und
in `contrib/keyd/g15.conf` eingetragen werden. Danach:

```bash
sudo install -Dm644 contrib/keyd/g15.conf /etc/keyd/g15.conf
sudo keyd check /etc/keyd/g15.conf
sudo keyd reload
```

Eine Geräte-ID darf nur in einer keyd-Konfigurationsdatei vorkommen. Der
Editor bricht bei einem Konflikt ab, statt fremde Konfigurationen zu
überschreiben.

## Grenzen des aktuellen Stands

- Die MR-Schnellaufnahme ist noch nicht implementiert.
- Automatische, anwendungsabhängige Profilwechsel fehlen noch.
- Programmstarts werden nicht über keyds privilegierte `command()`-Aktion
  ausgeführt. Dafür ist später ein unprivilegierter Benutzerdienst vorgesehen.
- Die LCD-Tasten und der runde Applet-Umschalter gehören nicht zu den
  M1–M3-Profilen.
- Das keyd-/Polkit-Backend ist Linux-spezifisch; Datenmodell und Oberfläche
  sind bewusst davon getrennt.

## Projektstruktur

| Pfad | Inhalt |
|---|---|
| `g15daemon/` | Daemon, Hardwarezugriff und Konfiguration |
| `plugins/` | LCD-, Netzwerk-, Uhr- und UINPUT-Plugins |
| `libg15daemon_client/` | Clientbibliothek für LCD-Anwendungen |
| `gui/` | GTK-Editor, Profilmodell und Installationshelfer |
| `contrib/keyd/` | Vorlage für die G-Tasten-Belegung |
| `Documentation/` | Profil- und Entwicklungsdokumentation |
| `tests/` | automatisierte C-, Shell- und Python-Tests |

Weitere technische Hinweise stehen in
[DEVELOPMENT.md](Documentation/DEVELOPMENT.md). Häufige Fragen beantwortet die
[FAQ](FAQ), die geplante Weiterentwicklung steht in [TODO](TODO).

## Herkunft und Lizenz

Dieses Repository baut auf dem von Daniel Menelkir gepflegten
[G15Daemon-Upstream](https://gitlab.com/menelkir/g15daemon) und der Arbeit der
ursprünglichen G15Tools-Autoren auf. Die vollständige Historie und die Namen
der Mitwirkenden befinden sich in `ChangeLog` und `AUTHORS`.

Der Quellcode steht unter der GNU General Public License, Version 2 oder
später. Einzelheiten enthält [LICENSE](LICENSE).

## Mitwirken

Fehlerberichte und Beiträge sind willkommen. Bitte zuerst
[CONTRIBUTING.md](CONTRIBUTING.md) und bei sicherheitsrelevanten Problemen
[SECURITY.md](SECURITY.md) lesen.
