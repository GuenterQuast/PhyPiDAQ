package edu.kit.freejdaq.mockup;

import edu.kit.freejdaq.mockup.ControllerModelInterface;
import edu.kit.freejdaq.mockup.ModelMockup;

public class ControllerMockUp implements FacadeViewController {
	
	ControllerModelInterface toModel = new ModelMockup();
	
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

	@Override
	public boolean addBuildingBlock(String id) {
		// TODO Auto-generated method stub
		return false;
	}

	@Override
	public boolean removeBuildingBlock(String initId, long configId) {
		// TODO Auto-generated method stub
		return false;
	}

	@Override
	public boolean addConnection(String firstChannelId, String secondChannelId) {
		// TODO Auto-generated method stub
		return false;
	}

	@Override
	public boolean removeConnection(String firstChannelId, String secondChannelId) {
		// TODO Auto-generated method stub
		return false;
	}

}
