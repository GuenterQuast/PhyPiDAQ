# PhyPiDAQ

## Datenerfassung und Analyse für die Physikausbildung mit Raspberry Pi

Dieser Code in der Programmmiersprache *pyhton3* bietet einige grundlegende Funktionen zur Datenerfassung und -visualisierung wie Datenlogger, Balkendiagramm, XY- oder Oszilloskopanzeige und Datenaufzeichnung auf Festplatte.

Neben den GPIO Ein- und Ausgängen des Raspberry Pi werden die Analog-Digital-Wandler ADS1115 und MCP3008 sowie USB-Oszilloskope (PicoScope der Firma picotech) als Eingabegeräte für analoge Daten sowie eine Reihe von digitalen Sensoren mit Protokollen wie I²C oder SPI unterstützt.

Das Paket bietet eine Abstraktionsschicht für Messgeräte und Sensoren, die an einen Raspberry Pi angeschlossen sind. Eigene Klassen für jedes Gerät bieten eine einfache, einheitliche Schnittstelle, die nur die Methoden `init(<config_dictionary>)`, `acquireData(buffer)`und `close()` enthalten. Einfache Beispiele mit minimalem Code veranschaulichen die Verwendung. Die grafische Benutzeroberfläche `phypi.py` und das Skript `run_phypi.py` bieten eine konfigurierbare Umgebung für komplexere Messprojekte.


 *Abbildung1*:  Darstellung der Zeitabhängigkeit von zwei an einen ADC angeschlossene Signalquellen
 
![Figure 1](doc/Kondensator.png)



## Schnellstart

Nach der Installation - siehe unten - steht eine Reihe von einheitlichen Klassen für die Datenerfassung, Visualisierung und Aufzeichnung aus dem Unterverzeichnis
`./phypidaq` zur Verfügung. Jedes unterstützte Gerät benötigt eine spezifische Konfiguration, die aus Konfigurationsdateien im Unterverzeichnis `./config` gelesen wird. Die Gesamtkonfiguration wird in Konfigurtionsdateien vom typ `.daq`
angegeben, die spezifizieren , welche Geräte und Anzeigemodule verwendet werden sollen, welche Ausleserate, Kalibrierungen oder analytische Formeln für aufgezeichnete Daten gelten sollen, oder auch Bereiche und Achsenbeschriftungen der grafischen Ausgabe.

Die grafische Benutzeroberfläche `phypi.py` hilft bei der Verwaltung der Konfigurationsoptionen und kann zum Starten der Datenerfassung verwendet werden.
In diesem Fall werden Konfigurationen und erzeugte Datendateien in einem dedizierten Unterverzeichnis in `$HOME/PhyPi` abgelegt. Der Name wird von einem benutzerdefinierten Tag und dem aktuellen Datum und der Uhrzeit abgeleitet.

Die Datenerfassung kann auch über die Kommandozeile gestartet werden:

   run_phypi.py <config_file_name\>.daq

Wenn keine Konfigurationsdatei angegeben ist, wird der Standardwert `PhyPiConf.daq` verwendet.

Das Unterverzeichnis `./examples` enthält eine Reihe einfacher Python-Skripte, die die Verwendung der bertreitgestellten Datenerfassungs- und Anzeigemodule mit minimalem Code veranschaulichen.

## Konfiguration


Mit dem Skript `run_phypi.py` können sehr allgemeine Messaufgaben ausgeführt werden, ohne eigenen Code schreiben zu müssen. Die Konfigurationsoptionen für Eingabegeräte und deren Kanäle sowie für die Anzeige- und Datenspeichermodule werden in einer globalen Konfigurationsdatei vom Typ `.daq` (in *yaml*-Markup-Sprache) angegeben, die Verweise auf Gerätekonfigurationsdateien vom Typ `.yaml` enthält.

Ein typisches, kommentiertes Beispiel sieht wie folgt aus:

**file PhyPiConf.daq**

    # Configuration Options for PhyPiDAQ
    
    # device configuration files
    DeviceFile: config/ADS1115Config.yaml
    #DeviceFile: config/MCP3008Config.yaml
    #DeviceFile: config/PSConfig.yaml
    #DeviceFile: config/MAX31865Config.yaml
    #DeviceFile: config/GPIOCount.yaml
    
    ## an example for multiple devices
    #DeviceFile: [config/ADS1115Config.yaml, config/ GPIOCount.yaml]
    
    DisplayModule: DataLogger
    # DisplayModule: DataGraphs  # text, bar-graph, history and xy-view
    Interval: 0.1                     # logging interval
    XYmode:     false                 # enable/disable XY-display
    
    # channel-specific information
    ChanLabels: [(V), (V) ]          # names and/or units for channels 
    ChanColors: [darkblue, sienna]    # channel colours in display
    
    # eventually overwrite Channel Limits obtained from device config 
    ##ChanLimits: 
    ## - [0., 1.]   # chan 0
    ## - [0., 1.]   # chan 1
    ## - [0., 1.]   # chan 2
    
    #ChanCalib:
    #  - null    or  - <factor> or  - [ [ <true values> ], [ <raw values> ] ] 
    #  - 1.                       # chan0: simple calibration factor
    #  - [ [0.,1.], [0., 1.] ]    # chan1: interpolation: [true]([<raw>] )
    #  - null                     # chan2: no calbration
    
    # apply formulae to calibrated channel values
    #ChanFormula:
    #  - c0 + c1  # chan0
    #  - c1          # chan1
    #  - null        # chan2 : no formula

    # name of output file
    #DataFile:   testfile.csv     # file name for output file 
    DataFile:   null              #      use null if no output wanted
    #CSVseparator: ';'            # field separator for output file, defaults to ','
    

The device configuration file for the analog-to-digital converter **ADS1115**
specifies the active channels and their ranges:

**file ADS1115Config.yaml**

    # example of a configuration file for ADC ADS1115
    
    DAQModule: ADS1115Config    # phypidaq module to be loaded
    
    ADCChannels: [0, 3]         # active ADC-Channels
                            # possible values: 0, 1, 2, 3
                            # when using differential mode:
                                #    -  0 = ADCChannel 0 
                                #            minus ADCChannel 1
                                #    -  1 = ADCChannel 0 
                                #            minus ADCChannel 3
                                #    -  2 = ADCChannel 1 
                                #            minus ADCChannel 3
                                #    -  3 = ADCChannel 2 
                                #            minus ADCChannel 3
    
    DifModeChan: [true, true] # enable differential mode for Channels
    
    Gain: [2/3, 2/3]          # programmable gain of ADC-Channel
                              #   possible values for Gain:
                              #     - 2/3 = +/-6.144V
                              #     -   1 = +/-4.096V
                              #     -   2 = +/-2.048V
                              #     -   4 = +/-1.024V
                              #     -   8 = +/-0.512V
                              #     -  16 = +/-0.256V
    sampleRate: 860           # programmable Sample Rate of ADS1115
                              #    possible values for SampleRate: 
                              #    8, 16, 32, 64, 128, 250, 475, 860

Beispiele für andere Geräte wie das Picotech USB-Oszilloskop  PicoScope, den Analog-Digital-Wandler MCP3008 oder für Geschwindigkeitsmessungen über die GPIO - Pins,
sind im Konfigurationsverzeichnis `./config` enthalten:  `PSConfig.yaml`, `MCP3008Config.yaml` bzw. `GPIOcount.yaml`.


## Installation

Dieses Paket basiert auf Code aus anderen Paketen, die die Treiber für die unterstützten Geräte bereitstellen:

```
- die Adafruit Pyhon MCP3008 Bibliothek, 
    <https://github.com/adafruit/Adafruit_Python_MCP3008>
- die Adafruit Python ADX1x15 Bibliothek
    <https://github.com/adafruit/Adafruit_Python_ADS1x15>
- Komponenten des picoDAQ-Projekts
    <https://github.com/GuenterQuast/picoDAQ>
- das  *python* Interface für die PicoScope Treiber des *pico-python*-Projeks   
    von Colin O'Flynn, <https://github.com/colinoflynn/pico-python> und
- die C-Treiber aus dem Pico Technology Software Development Kit
    <https://www.picotech.com/downloads>
```

Zur Vereinfachung der Installation werden Installationsdateien für benötigte externe Pakete im PIP-Wheel-Format im Unterverzeichnis *./whl* bereitgestellt .

Die Visualisierungsmodule hängen von *matplotlib.pyplot* , *Tkinter* und *pyQt5* ab, die ebenfalls installiert sein müssen.

Nach dem Einrichten Ihres Raspberry Pi mit dem aktuellen Debian-Release *stretch*
sollten die folgenden Schritte durchgeführt werden, um alle erforderlichen Pakete  
zu aktualisieren und zu installieren:


```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-scipy
sudo apt-get install python3-matplotlib
sudo apt-get install python3-pyqt5

sudo pip3 install pyyaml

# PicoTech base drivers for picoScope USB devices
#   see https://www.picotech.com/support/topic14649.html
# after inclusion of the picotech raspbian repository:  
sudo apt-get install libps2000a
# allow access of user pi to usb port
sudo usermod -a -G tty pi

# get PhyPiDAQ code and dependencies
mkdir git
cd git
git clone https://GuenterQuast/PhyPiDAQ
cd PhyPicDAQ/whl
sudo pip3 install *.whl
```
## Empfohlene Sensoren und Devices

## Beschreibung der Beispiele
