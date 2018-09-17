# Abkühlungskurve mit dem PT100 messen.

In diesem Dokument erfahren sie, wie sie mit dem PT100 eine Abkühlungskurve aufnehmen

**Benötigte Bauteile:**

* PT100-Temperatursensor
* MAX31865 Temperatursensor-Verstärker
* Ein Behälter mit heißem Wasser

Der PT100 ist ein temperaturabhängiger Widerstand aus Platin mit einem nominellen Widerstand von $100\Omega$ bei 0°C. Auf Grund des niedrigen Widerstandswertes ist es notwendig das Spannungssignal des PT100 über den dafür konzipierten Verstärker MAX31865 auszulesen. Der MAX31865 ist gleichzeitig auch noch ein Analog-Digital-Wandler, so dass keine weiteren Teile notwendig sind.
Der PT100 kommt in Varianten mit zwei, drei oder vier Kabeln. Das dritte und vierte Kabel dienen jeweils dazu die Widerstände der Kabel im Sensor auszugleichen - besonders interessant, wenn sehr lange Kabel verwendet werden. In unserem Koffer ist die einfache Variante mit zwei Kabeln beigelegt, da diese für das Aufzeichnen von Temperaturkurven im Schulbereich vollkommen ausreichend ist. Zu beachten ist, dass, je nach verwendeter Anzahl Kabel, unterschiedliche Verlötungen auf dem MAX31865 nötig sind, ein fliegender Wechsel zwischen verschiedenen PT100 ist also nicht möglich.

**Versuchsaufbau:**

Der 2-Kabel-PT100 wird an die beiden mittleren Anschlüsse am MAX31865 angeschlossen.

Der Anschluss des MAX31865 erfolgt an folgende Pins:

* $V_{in}$ an 3.3V
* GND an GND
* CS an CE0 (GPOI8)
* SDO an MISO (GPIO9)
* SDI an MOSI (GPIO10)
* CLK an SCLK (GPIO11)

![PT100_Steckplatine](Images\PT100_Steckplatine.png)



**Versuchsdurchführung:**

Die Durchführung ist simpel. Man erhitzt das Wasser und steckt anschließend den PT100 in den Behälter. Für bessere Ergebnisse sollte darauf geachtet werden, dass der PT100 keine Wand berührt.

Sobald der Versuch gestartet ist, heißt es nur noch warten, bis das Wasser zufriedenstellend abgekühlt ist. Um die Zeit zum Abkühlen zu verkürzen, kann, falls die Möglichkeit besteht, der Aufbau an einem möglichst kalten Ort aufgestellt werden (Fensterbank im Winter als Beispiel). Es sollte aber darauf geachtet werden, dass der Versuchsbereich über den Versuchszeitraum eine möglichst konstante Temperatur besitzt, da andernfalls das Ergebnis verfälscht wird.



**Erläuterung der Config:**

Der Versuch verwendet die universell für den PT100 einsetzbare Config PT100.daq. Lediglich das Logging-Intervall wurde auf eine Sekunde erhöht, um die Datenmenge auf Grund der Dauer des Versuches in Grenzen zu halten. Es sind weder Änderungen an den ChanLimits nötig, noch irgendwelche Kalibrierungen oder Formeln. 

Die ModuleConfig MAX31865Config.yaml enhält nur drei Zeilen:

```Python
NWires: 2         # numbers of wires PT100
Rref: 430         # value reference resistor MAX31865
R0: 100.          # value resistor PT100 at 0°C
    
# Rref und R0 sind im Standardmäßig immer 430 und 100. Falls man präzisere Werte für R0 möchte, könnte man den exakten Widerstandswert bei 0°C ausmessen, dies ist aber nicht nötig. Rref ist auf dem MAX31965 verlötet und kann theoretisch ausgetauscht werden.
# NWires kann 2, 3 oder 4 sein, je nach verwendetem PT100.

```



## Aufgaben

1. Nehmen sie die aktuelle Umgebungstemperatur im Versuchsbereich auf.

2. Führen sie den Versuch wie beschrieben durch. Abhängig vom verwendeten Behälter und den äußeren Umständen wird die Abkühlung viel Zeit in Anspruch nehmen, es ist sinnvoll den Versuch einfach "nebenher" laufen zu lassen, während man sich mit etwas anderem beschäftigt.

3. Exportieren sie die gewonnenen Daten in Excel und stellen sie die Daten als in t-$\alttheta$-Diagramm dar.

4. Schätzen sie mit Hilfe von Excel eine Gleichung für die Abkühlungskurve ab. Überlegen sie dafür, welche Faktoren alles eine Rolle spielen könnten.

## Anhang



### Erläuterung der Ergebnisse

Noch zu erledigen.

### Schaltplan

![PT100_Schaltplan](Images\PT100_Schaltplan.png)