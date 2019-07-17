package edu.kit.freejdaq.mockup;

public interface IAccessToSensorInfo {
	public String[] getIdsOfAvailableSensorsSensors();
	public boolean copyYamlFileFromPi(String sensorId);
	public boolean copyYamlFileToPi(String sensorId);
}