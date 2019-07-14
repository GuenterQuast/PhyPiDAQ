package edu.kit.freejdaq.mockup;

public class ControllerMockUp {
	
	ControllerModelImplement toModel = new ModelMockUp();
	
	public boolean blockAdded(String id) {
		toModel.addBuildingBlock(id);
		return true;
		
	}
	
	public boolean blockRemoved(String initId, long configId) {
		toModel.removeBuildingBlock(initId, configId);
		return true;
	}
	
	public boolean connectionAdded(String firstChannelId, String secondChannelId) {
		toModel.addConnection(firstChannelId, secondChannelId);
		return true;
		
	}
	
	public boolean connectionRemoved(String firstChannelId, String secondChannelId) {
		toModel.removeConnection(firstChannelId, secondChannelId);
		return true;
	}
	
	public void start(String[] sensorIds, IMStreamListener[] dataListeners) {
		toModel.start(sensorIds, dataListeners);
		
	}
	
	public void pause() {
		toModel.pause();
		
		
	}
	
	public void resume() {
		toModel.resume();
		
		
	}
	
	public void reset() {
		toModel.reset();
		
	}

}
