# Sicherheitsrichtlinie

## Sicherheitsproblem melden

Bitte Sicherheitslücken nicht zuerst als öffentliches Issue veröffentlichen.
Nutze auf GitHub unter **Security → Advisories** die Funktion zum privaten
Melden einer Schwachstelle. Falls sie im Repository nicht verfügbar ist,
eröffne ein knappes Issue ohne technische Angriffsdaten und bitte um einen
privaten Kontaktweg.

Eine Meldung sollte betroffene Version, Auswirkungen, Voraussetzungen und
reproduzierbare Schritte enthalten. Zugangsdaten und personenbezogene Daten
dürfen nicht mitgesendet werden.

## Sicherheitsmodell

Der Daemon benötigt Hardwarezugriff und keyd läuft üblicherweise mit
Systemrechten. Deshalb validiert der Installationshelfer Quelle, Eigentümer,
Größe, Geräte-ID und Syntax, bevor er ein Profil übernimmt. Direkte
`command()`-Aktionen werden nicht erzeugt, weil dadurch Programme mit
Systemrechten gestartet würden.

Nur der aktuelle Stand des Hauptbranches wird aktiv gepflegt. Historische
Versionen erhalten in der Regel keine rückwirkenden Sicherheitskorrekturen.
