package edu.kit.freejdaq.mockuptest;

public interface ControllerModelInterface {
	
	//Config
	
	public boolean addBuildingBlock(String id);
	
	public boolean removeBuildingBlock(String initId, long configId);
	
	public boolean addConnection(String firstChannelId, String secondChannelId);
	
	public boolean removeConnection(String firstChannelId, String secondChannelId);
	
	//MeasurementRun
	
	public boolean start(String[] sensorIds, IMStreamListener[] dataListeners);
	
	public boolean pause();
	
	public boolean resume();
	
	public boolean reset();

}
