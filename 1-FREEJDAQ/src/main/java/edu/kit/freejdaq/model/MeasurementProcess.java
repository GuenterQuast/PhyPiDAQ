package edu.kit.freejdaq.model;


/**
 * @author David
 *
 *  
 *
 *@startuml
 *
 * class MeasurementInterface {
 * 
 * -initializeMeasurement(MeasurementConfiguration)
 * +run(MeasurementConfiguration, DataStream)
 * +check(MeasurementConfiguration):boolean
 * -resetMeasurement() : boolean
 * -stopMeasurement() : boolean
 * 
 * 
 * 
 * }
 *
 *
 * class Display {
 * +saveGraph() : boolean
 * +saveData() : boolean
 * +displayDataStream(MeasurementConfiguration, DataStream)
 * 
 * }
 *
 * class UserInterface {
 * 
 * }
 *
 * class PhyPiDAQInterface {
 * + getDataStream(MeasurementConfiguration.DAQ): Datastream
 * + stopDataStream()
 * }
 *
 *
 * class DataStream {
 * IdOfSensor : String
 * timeStamp : Integer
 * samplingRate : float
 * numberOfChannels : Integer
 * rawData<float>
 * 
 * 
 * }
 *
 * 
 * class MeasurementConfiguration {
 * name : String
 * samplingRate : float
 * listOfBlocks<Block>
 * 
 * 
 * +save(MeasurementConfiguration) : boolean
 * +load(MeasurementConfiguration) : boolean
 * }
 * 
 * MeasurementInterface -down- UserInterface
 * MeasurementInterface -up- PhyPiDAQInterface
 * MeasurementConfiguration - MeasurementInterface
 * MeasurementInterface -down- Display
 * MeasurementInterface "1" -right- "0..N" DataStream : > maintains 
 * 
 *
 *
 *@enduml
 *
 * Die Klasse MeasurementInterface nimmt einen Befehl über das UserInterface
 * entgegen (z.B. starte Messung) und führt ihn dann aus. Dabei muss sie
 * auf andere Klassen zugreifen, wie z.B. auf das PhyPiDAQInterface.
 *
 *
 */



public class MeasurementProcess {

}
