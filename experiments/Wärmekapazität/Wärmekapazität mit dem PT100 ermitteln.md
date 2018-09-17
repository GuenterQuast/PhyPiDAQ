

# Wärmekapazität mit dem PT100 ermitteln

In diesem Dokument erfahren sie, wie sie mit dem PT100 die Wärmekapazität von Wasser oder einer anderen Flüssigkeit bestimmen.

**Benötigte Bauteile:**

* PT100-Temperatursensor
* MAX31865 Temperatursensor-Verstärker
* Tauchsieder
* Behälter mit Flüssigkeit

Der PT100 ist ein temperaturabhängiger Widerstand aus Platin mit einem nominellen Widerstand von $100\Omega$ bei 0°C. Auf Grund des niedrigen Widerstandswertes ist es notwendig das Spannungssignal des PT100 über den dafür konzipierten Verstärker MAX31865 auszulesen. Der MAX31865 ist gleichzeitig auch noch ein Analog-Digital-Wandler, so dass keine weiteren Teile notwendig sind.
Der PT100 kommt in Varianten mit zwei, drei oder vier Kabeln. Das dritte und vierte Kabel dienen jeweils dazu die Widerstände der Kabel im Sensor auszugleichen - besonders interessant, wenn sehr lange Kabel verwendet werden. In unserem Koffer ist die einfache Variante mit zwei Kabeln beigelegt, da diese für das Aufzeichnen von Temperaturkurven im Schulbereich vollkommen ausreichend ist. Zu beachten ist, dass, je nach verwendeter Anzahl Kabel, unterschiedliche Verlötungen auf dem MAX31865 nötig sind, ein fliegender Wechsel zwischen verschiedenen PT100 ist also nicht möglich.

Um Verluste durch Abkühlung zu vermeiden, ist es von Vorteil, wenn der Flüssigkeitsbehälter möglichst gut isoliert ist.

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

Der Behälter mit der Flüssigkeit wird in Position gebracht und der PT100 darin platziert. Der Tauchsieder sollte vor dem Versuch vorgeheizt werden, da sonst die Temperatur zu stark ansteigt, bevor der Sieder seine gewünschte konstante Leistung liefert, was zu Verlusten durch Abkühlung führt.
Die Temperaturaufnahme wird gestartet und der vorgeheizte Tauchsieder vollständig eingetaucht. Der Temperaturverlauf wird dann für einige Sekunden gemessen.
Falls eine endlos verfügbare Flüssigkeit, wie Wasser, verwendet wird, kann die erhitzte Flüssigkeit dann einfach gegen neue, kalte, Flüssigkeit ausgetauscht werden und noch ein Messdurchgang gestartet werden.



**Erläuterung der Config:**

Der Versuch verwendet die universell für den PT100 einsetzbare Config PT100.daq. Es sind weder Änderungen an den ChanLimits nötig, noch irgendwelche Kalibrierungen oder Formeln. 

Die ModuleConfig MAX31865Config.yaml enhält nur drei Zeilen:

```Python
NWires: 2         # numbers of wires PT100
Rref: 430         # value reference resistor MAX31865
R0: 100.          # value resistor PT100 at 0°C
    
# Rref und R0 sind im Standardmäßig immer 430 und 100. Falls man präzisere Werte für R0 möchte, könnte man den exakten Widerstandswert bei 0°C ausmessen, dies ist aber nicht nötig. Rref ist auf dem MAX31965 verlötet und kann theoretisch ausgetauscht werden.
# NWires kann 2, 3 oder 4 sein, je nach verwendetem PT100.

```



## Aufgaben

1. Führen sie den Versuch für eine oder mehrer Flüßigkeiten durch.
2. Exportieren sie die Daten in Excel und stellen sie sie als t-$\vartheta$-Diagramm dar.

3. Verwenden sie den Zusammenhang zwischen zugeführter Energie und Temperatur

$$
\Delta E =c\cdot m \cdot \Delta \vartheta
$$
​	um mit Hilfe einer Ausgleichsgerade die Wärmekapazität der Flüssigkeit zu ermitteln.

*Hinweis:* Nehmen sie an, dass für die zugeführte Energie $E= P_{el}\cdot t $ gilt, der Tauchsieder also verlustfrei seine gesamte elektrische Leistung an die Flüssigkeit abgibt.



## Anhang

### Erläuterung der Ergebnisse

Noch zu erledigen

### Schaltplan



![PT100_Schaltplan](Images\PT100_Schaltplan.png)