package edu.kit.freejdaq.mockup;

import java.util.HashMap;

import edu.kit.freejdaq.model.BuildingBlock;

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
	
	// ViewDirectoryInterface
	
	public BuildingBlock getInitBuildingBlock(String id) {
		System.out.println("getting init block with id " + id);
		return null;
	}
	
	public BuildingBlock getConfigBuildingBlock(int id) {
		System.out.println("getting config block with id " + id);
		return null;
	}
	
	public HashMap<String, BuildingBlock> getFullInitBlock() {
		System.out.println("getting all init blocks");
		return null;
	}
	
	public HashMap<Integer, BuildingBlock> getFullConfigBlock() {
		System.out.println("getting all config blocks");
		return null;
	}
	
	public boolean getConnection(int chId1, int chId2) {
		System.out.println("getting connection");
		return true;
	}
	
	public boolean checkForUpdate() {
		return true;
	}

}
