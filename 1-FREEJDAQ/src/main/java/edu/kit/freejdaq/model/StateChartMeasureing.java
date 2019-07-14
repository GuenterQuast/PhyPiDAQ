package edu.kit.freejdaq.model;

/**

@author David


@startuml

[*] --> Idle : startProgram()
Idle -right-> [*] : quitProgram()



Idle : entry / initialize()
Idle : exit / destroy()
Idle : save(MeasurementConfiguration): boolean
Idle : load(Path) : MeasurementConfiguration
Idle : delete(MeasurementConfiguration)
Idle: saveData(data)
Idle: saveGraph(graph)
Idle: resetMeasurement()


Idle -> Running : run(MeasurementConfiguration)
Running: entry / checkSensor(MeasurementConfiguration),createYaml() and RunPhyPiDAQ()
Running: exit / stoppPhyPiDAQ()
Running --> Idle: stoppMeasurement() or ERROR
@enduml


*/
public class StateChartMeasureing {

}
