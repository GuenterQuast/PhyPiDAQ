package edu.kit.freejdaq.mockup;

public interface ControllerModelInterface {
	
	public boolean addBuildingBlock(String id);
	
	public boolean removeBuildingBlock(String initId, long configId);
	
	public boolean addConnection(String firstChannelId, String secondChannelId);
	
	public boolean removeConnection(String firstChannelId, String secondChannelId);
	
	public boolean start(String[] sensorIds, IMStreamListener[] dataListeners);
	
	public boolean pause();
	
	public boolean resume();
	
	public boolean reset();

}
