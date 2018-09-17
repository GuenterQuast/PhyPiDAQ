# Kennlinien von Dioden/Bestimmung von h

Der folgende Versuch dient der Aufzeichnung der Strom-Spannung- Kennlinien von Dioden und im Anschluss der Bestimmung des planckschen Wirkungsquantums h.
Die Kennlinien können entweder einzeln aufgenommen werden oder bis zu drei Dioden gleichzeitig.

**Benötigte Bauteile:**

* ADS1115 Analog-Digital-Wandler
* 1 Widerstand ($100\Omega$) pro Diode
* verschiedenfarbige Dioden mit bekannten Wellenlängen
* 1 Drehpotentiometer

**Versuchsaufbau:**

1 Diode:

![Kondensator2_Steckplatine](Images\Kennlinie_Steckplatine.jpg)



2 Dioden:

![Kennlinie_Steckplatine2](Images\Kennlinie2_Steckplatine.jpg)

3 Dioden

![Kondensator3_Steckplatine](Images\Kennlinie3_Steckplatine.png)

Beim Anschließen von Dioden ist zu beachten, dass die Einbaurichtung von Bedeutung ist. In diesem Versuch müssen die Dioden in der sogenannten "Durchlassrichtung" angeschlossen werden. Dabei wird die Anode der Diode an den Pluspol angeschlossen. Die Anode ist an den Dioden durch den längeren Verbindungsdraht zu erkennen. Wird die Diode verkehrtherum angeschlossen, in "Sperrichtung," so fließt bei den hier verwendeten Spannungen kein Strom. 
**Dioden nicht ohne Vorwiderstand anschließen**

**Erläuterung des Versuchs:**

Die Strom-Spannung-Kennlinie eines elektrischen Bauteils beschreibt schlicht den Zusammenhang zwischen der, an  das Bauteil angelegten Spannung und dem Stromfluss durch das Bauteil. Es soll also in einen x-y-Diagramm der Strom über die Spannung aufgetragen werden. Für einen Widerstand kennen wir den Zusammenhang bereits, nämlich $ I=U/R $. Die Kennlinie ist also einfach eine Gerade.

Da wir eine Kurve in Abhängigkeit der angelegten Spannung benötigen, brauchen wir eine regelbare Spannungsquelle. In unserem Aufbau übernimmt dies das Potentiometer.
Der Eingang A0 ist zwischen Potentiometer und Widerstand angeschlossen, er liefert uns daher direkt die angelegte Spannung.
Die Stromstärke ist nicht direkt messbar. Wir können aber die Spannung über einem bekannten Widerstand bestimmen und daraus von PhyPi die Stromstärke errechnen lassen. Betrachten wir dafür exemplarisch die Schaltung mit einer Diode. Die Spannung über den Widerstand können wir ermitteln, in dem wir das Potential auf beiden Seiten des Widerstands bestimmen und die Differenz bilden. Das Potential vor dem Widerstand wird mit A0 gemessen, A1 liefert das Potential danach. Der Widerstand hat den bekannten Wert 100\Omega. Damit ist der Strom I=(U_0 - U_1)/100\Omega$.  Mit dieser Formel können wir mit der Kanal-Formel-Funktion in der Config direkt in PhyPi die gemessenen Spannungen verarbeiten. Mit dem x-y-Modus von PhyPi werden die Messungen direkt in der gewünschten Diagrammform aufgetragen. Die Erläuterungen der Config-Datei finden sie im Anschluss.

**Versuchsdurchführung:**

Zu Beginn der Versuchsdurchführung sollte das Potentiometer so eingestellt sein, dass die angelegte Spannung 0 ist. Dann wird die Aufnahme gestartet und das Potentiometer langsam aufgedreht. Je feiner die Drehungen, desto besser wird das Ergebnis. Das Potentiometer wird so weit aufgedreht, bis für jede Diode ein deutlicher Stromfluss erkennbar war, dann wird die Aufnahme gestoppt und erst nach Stoppen der Aufnahme wird das Potentiometer wieder auf die Anfangsposition gedreht. Sollten sie nicht sicher sein, ob die aufgezeichneten Kurven der Erwartung entsprechen, finden sie im Anhang ein Beispiel. Für unsere Zwecke ist besonders der Moment interessant, in dem Strom zu fließen beginnt, dieser Bereich sollte also sauber aufgezeichnet sein, kleine Störungen im übrigen Diagramm sind nicht unbedingt schädlich für die bestimmung von h.

Falls die Dioden einzeln gemessen werden, wiederholen sie den Vorgang für alle gewünschten Dioden.

**Erläuterung der Config:**

Die vorgegeben Dateien nehmen an, dass an $100\Omega$-Widerstand verwendet wird für jede Diode. Sollte dies nicht der Fall sein, muss die ChanFormula angepasst werden und gegebenfalls die Chanlimits für bessere Sichtbarkeit.

```Python
# Configuration Options for PhyPiDAQ 

# device configuration files 
DeviceFile: config/ADS1115Config.yaml  
#DeviceFile: config/MCP3008Config.yaml  
#DeviceFile: config/PSConfig.yaml         
#DeviceFile: config/MAX31865Config.yaml 
#DeviceFile: config/GPIOCount.yaml

## an example for multiple devices
#DeviceFile: [config/ADS1115Config.yaml, config/GPIOCount.yaml]  


DisplayModule: DataLogger
# DisplayModule: DataGraphs  # text, bar-graph, history and xy-view
Interval: 0.05                     # logging interval         
XYmode:     true                 # enable/disable XY-display


# channel-specific information
ChanLabels: [(V), (mA), (mA), (mA) ]          # names and/or units for channels 
ChanColors: [darkblue, red, green, blue]    # channel colours in display

# eventually overwrite Channel Limits obtained from device config 
ChanLimits: 
 - [0., 5]   # chan0
 - [0., 20]   # chan1
 - [0., 20]   # chan2
 - [0., 20]   # chan3

#Chanlimits müssen korrigiert werden, auf Grund der verwendeten ChanFormula

ChanCalib:
##  - null    or  - <factor> or  - [ [ <true values> ], [ <raw values> ] ] 
  - 1.      # chan0
  - 1.      # chan1
  - 1.      # chan2
  - 1.      # chan3
                     

# apply formulae to calibrated channel values
ChanFormula:
  - c0  # chan0
  - (c0-c1)*10          # chan1
  - (c0-c2)*10      # chan2
  - (c0-c3)*10		# chan3

# Die allgemeine Formel für Kanal x lautet (c0-cX)/R*1000. Der Faktor 1000 resultiert aus der Umwandlung in mA. Für R /= 100 ändern sich die obigen Formeln damit.
  
# name of output file

DataFile:   Kennlinie             # file name for output file 

```



## 

### Aufgaben

1. Zeichnen sie die Kennlinie von mindestens drei verschiedenen Dioden auf.
2. Überlegen sie eine Erklärung, für die Form der Kennlinien.
3. Stellen sie die Kennlinien in einem U-I-Diagramm in Excel dar.
4. Bestimmen sie das Plancksche Wirkungsquantum h aus den Kennlinien. Gehen sie wie folgt vor:
   * Lesen sie für jede Diode die Spannung ab, an der Strom zu fließen beginnt - das ist die Schwellenspannung.
   * Fertigen sie eine Tabelle an, die für jede Diode folgende Informationen enthält: Farbe, Wellenlänge $\lambda$, Frequenz des Lichts $\nu$ und Schwellenspannung $U_s$.
   * Verwenden sie den Zusammenhang $eU_s = h\nu$ zum Berechnen von h. Berechnen sie h dabei zum einen direkt aus den einzelnen Messwerten, aus den Differenzen der Messwerte der verschiedenen Farben und mit Hilfe eines $\nu - U_s$-Diagramms und einer Ausgleichsgeraden. Vergleichen sie die Resultate der drei Methoden und überlegen sie, welche Vorteile die verschiedenen Methoden haben.

## Anhang

### Erläuterung der Ergebnisse

Noch zu erledigen

![Kennlinie](Images\Kennlinie.png)

### Schaltpläne

1 Diode:

![Kennlinie_Schaltplan](Images\Kennlinie_Schaltplan.jpg)



2 Dioden:

![Kennlinie_Schaltplan2](Images\Kennlinie2_Schaltplan.jpg)

3 Dioden:

![Kennlinie3_Schaltplan](Images\Kennlinie3_Schaltplan.png)
$$

$$
