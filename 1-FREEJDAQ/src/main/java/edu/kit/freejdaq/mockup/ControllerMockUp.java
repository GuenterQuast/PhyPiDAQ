package edu.kit.freejdaq.mockup;

public class ControllerMockUp {
	
	ControllerModelImplement toModel = new ModelMockUp();
	
	public boolean blockAdded(String id) {
		return toModel.addBuildingBlock(id);
		
		
	}
	
	public boolean blockRemoved(String initId, long configId) {
		return toModel.removeBuildingBlock(initId, configId);
		
	}
	
	public boolean connectionAdded(String firstChannelId, String secondChannelId) {
		return toModel.addConnection(firstChannelId, secondChannelId);
		
		
	}
	
	public boolean connectionRemoved(String firstChannelId, String secondChannelId) {
		return toModel.removeConnection(firstChannelId, secondChannelId);
	
	}
	
	public boolean start(String[] sensorIds, IMStreamListener[] dataListeners) {
		return toModel.start(sensorIds, dataListeners);
		
	}
	
	public boolean pause() {
		return toModel.pause();
		
		
	}
	
	public boolean resume() {
		return toModel.resume();
		
		
	}
	
	public boolean reset() {
		return toModel.reset();
		
	}

}
