package edu.kit.freejdaq.mockuptest;

public class ModelMockup implements ControllerModelInterface {
	
	// IModelInformation
	public boolean addBuildingBlock(String id) {
		System.out.println("added block; id: " + id);
		return true;
	}
	
	public boolean removeBuildingBlock(String initId, long configId) {
		System.out.println("removed block; init id: " + initId + "; config id: " + configId);
		return true;
	}
	
	public boolean addConnection(String firstChannelId, String secondChannelId) {
		System.out.println("added connection; first id: " + firstChannelId + "; second id: " + secondChannelId);
		return true;
	}
	
	public boolean removeConnection(String firstChannelId, String secondChannelId) {
		System.out.println("removed connection; first id: " + firstChannelId + "; second id: " + secondChannelId);
		return true;
	}
	
	// IMeasurementRun
	public boolean start(String[] sensorIds, IMStreamListener[] dataListeners) {
		System.out.println("started");
		return true;
	}
	public boolean pause(){
		System.out.println("paused");
		return true;
	}
	public boolean resume(){
		System.out.println("resumed");
		return true;
	}
	public boolean reset(){
		System.out.println("resetted");
		return true;
	}

}
