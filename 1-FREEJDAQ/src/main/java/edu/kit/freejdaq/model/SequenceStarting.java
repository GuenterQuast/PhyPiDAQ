package edu.kit.freejdaq.model;

/**
 * 
 * 
 * @author David
 * 
 * oder alternativ als loop ab getDataStream... , bei der dann die loop für ein 
 * Abtastintervall durchgeführt wird ?
 * 
 * 
 * 
 * 
@startuml



actor "User" as U

activate UI

participant ":UserInterface" as UI
participant ":MeasurementInterface" as MR


participant ":PhyPiDAQInterface" as PPDI

participant ":Display" as D
participant "MC1:MeasurementConfiguration" as MC
participant "DS1:DataStream" as DS

U -> UI : start()
UI -> MR : start()
MR -> MR: initializeMeasurement()
activate MR
MR -> MR : load(MC1)
activate MR
MR -> PPDI : getDataStream(MC1, DS1)
activate PPDI
PPDI --> MR 
MR -> MR: runMeasurement(DS1)
activate MR
 
MR -> D : displayData(DS1)
activate D
D -> D : displayDataStream(DS1, MC1)
activate D
D --> MR: 
MR --> UI : 




@enduml
*/


public class SequenceStarting {

}
