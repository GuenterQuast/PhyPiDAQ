# PhyPiDAQ

## Datenerfassung und Analyse für die Physikausbildung mit Raspberry Pi

Dieser Code in der Programmmiersprache *pyhton3* bietet einige grundlegende Funktionen zur Datenerfassung und -visualisierung wie Datenlogger, Balkendiagramm, XY- oder Oszilloskopanzeige und Datenaufzeichnung auf Festplatte.

Neben den GPIO Ein- und Ausgängen des Raspberry Pi werden die Analog-Digital-Wandler ADS1115 und MCP3008 sowie USB-Oszilloskope (PicoScope der Firma Picotech) als Eingabegeräte für analoge Daten sowie eine Reihe von digitalen Sensoren mit Protokollen wie I²C oder SPI unterstützt.

Diese grafische Benutzeroberfläche hilft bei der Verwaltung der Konfigurationsoptionen und kann zum Starten der Datenerfassung verwendet werden.
Die Konfigurationen und erzeugte Datendateien werden in einem dedizierten Unterverzeichnis in `$HOME/PhyPi` abgelegt. Die jeweiligen Dateinamen werden von einem benutzerdefinierten Tag und dem aktuellen Datum und der Uhrzeit abgeleitet.

## Bedienungshinweise

Im Hauptreiter **Control** wird zunächst die Haupt-Konfigurationsdatei vom Typ *.daq* festgelegt - voreingestellt ist
*$HOME/PhyPi/phypi.daq*. In dieser Datei wird mindestens eine weitere Konfigurationsdatei angegeben, die die Konfiguration für den verwendeten Sensor oder AD-Wandler enthält (im Folgenden als
'Gerät' bezeichnet). 
Weiter können in diesem Reiter das Arbeitsverzeichnis (voreingestellt
*$HOME/PhyPi/*) sowie ein Tag für das Messprojekt angegeben werden.
Über den Knopf `Start` wir das Skript `run_phypi.py` gestartet, das
die Datenaufnahme steuert. 

Im Reiter **Configuration** wird der Inhalt der Konfigurationsdateien angezeigt und kann - nach Freischalten über 
den Knopf `EditMode` - editiert und abgespeichert werden. Als Dateiename für die Hauptkonfiguration wird der im Reiter *Control* als `Tag` eingestellte Name verwendet; die Namen
für die Dateien mit der Geräte-Konfiguration sind  die Hauptkonfiguration angegebenen Dateinamen inklusive eventuell angegebener Dateipfade. 

Der Reiter **Help/Hilfe** gib Hinweise zur Benutzung in englischer 
oder deutscher Sprache.

