# Logitech G15 v1: Helligkeit und Tastenprofile

Diese Erweiterung ist für das erste G15-Modell mit blauer Beleuchtung,
G1–G18, M1–M3 und MR vorgesehen.

## Tastaturhelligkeit

Die globale Daemon-Konfiguration akzeptiert die Stufen 0 bis 2:

```ini
[Global]
Keyboard Backlight Level: 2
```

- `0`: aus
- `1`: mittel
- `2`: maximale Helligkeit (Standard)

Ungültige Werte werden protokolliert und durch Stufe 2 ersetzt. Die Taste für
die Beleuchtung kann weiterhin zwischen den drei Stufen wechseln.

## Profile M1, M2 und M3

`g15daemon` meldet die Zusatztasten über sein UINPUT-Plugin als Linux-Tasten.
Die Vorlage [contrib/keyd/g15.conf](../contrib/keyd/g15.conf) übersetzt diese
Ereignisse mit `keyd` in drei exklusive Profile mit je 18 frei belegbaren
G-Tasten. Beim Start ist M1 aktiv; ein Druck auf M1, M2 oder M3 aktualisiert
weiterhin die entsprechende LED der Tastatur.

Die Zuordnungen sind zunächst `noop` und lösen damit absichtlich nichts aus.
Erlaubt sind normale Tasten, Tastenkombinationen, `macro(...)` und mit der
nötigen Vorsicht `command(...)`.

## Installation der Profilvorlage

Vor dem Kopieren muss die Geräte-ID mit `sudo keyd monitor` geprüft werden.
Auf dem Entwicklungssystem lautet sie `0000:0000:95e990cb`.

```bash
sudo install -Dm644 contrib/keyd/g15.conf /etc/keyd/g15.conf
sudo keyd check /etc/keyd/g15.conf
sudo keyd reload
```

Eine Geräte-ID darf nur in einer keyd-Konfigurationsdatei vorkommen. Eine alte
G15-Zuordnung muss daher vorher gesichert oder entfernt werden.

## Grafischer Profileditor

`g15-profile-editor` bietet eine GTK-4-Oberfläche für die Starthelligkeit und
alle 54 Belegungen der drei M-Profile. Ohne Installation kann die erzeugte
Datei aus dem Build-Verzeichnis mit `gui/g15-profile-editor` gestartet werden.

Die Schaltfläche **Speichern** schreibt zunächst ausschließlich nach
`~/.config/g15daemon/g15.conf` und prüft die Datei mit `keyd check`.
**Systemweit übernehmen …** startet über Polkit den getrennten Helfer
`g15-profile-install`. Dieser prüft Eigentümer, Größe, Geräte-ID und Syntax,
legt vorhandene Konfigurationen unter `/var/backups/g15daemon-config` ab und
lädt keyd neu. Bei einer doppelten Geräte-ID bricht er ab, statt eine andere
keyd-Konfiguration zu überschreiben.

Der Helfer startet `g15daemon` absichtlich nicht neu. Die gewählte Helligkeit
wird daher beim nächsten kontrollierten Daemon-Start aktiv.

### Abhängigkeiten und Portabilität

Der Editor benötigt Python 3, PyGObject und GTK 4. Die systemweite
Profilaktivierung benötigt Linux, keyd und Polkit (`pkexec`). Diese
Abhängigkeiten werden zur Laufzeit erkannt und sind nicht an CachyOS oder den
Paketmanager pacman gebunden. Für abweichende Paketlayouts können
`G15_PROFILE_PATH`, `G15_KEYD`, `G15_PKEXEC` und `G15_INSTALL_HELPER` gesetzt
werden.

Das Datenmodell (`g15_profile.py`), das keyd-Backend (`g15_keyd.py`), die
Plattformerkennung (`g15_platform.py`) und die GTK-Oberfläche sind getrennt.
Dadurch kann später ein anderes Eingabe-Backend ergänzt werden, ohne den
Profileditor oder das Datenmodell neu zu schreiben.

## Tastencodes des UINPUT-Plugins

| Physisch | keyd-Name | Physisch | keyd-Name |
|---|---|---|---|
| G1–G16 | Aliase `g1`–`g16` | G17/G18 | `f13`/`f14` |
| M1/M2/M3 | `f15`/`f16`/`f17` | MR | `f18` |

Die Aliasdefinitionen der Vorlage bilden auch G1–G16 auf ihre tatsächlichen
Linux-Namen ab. Die LCD-Tasten werden nicht durch keyd übernommen.

## MR

MR ist in der ersten Ausbaustufe deaktiviert. Eine Windows-ähnliche
Laufzeitaufzeichnung benötigt einen eigenen, persistenten Makrorecorder und
wird getrennt entwickelt.
