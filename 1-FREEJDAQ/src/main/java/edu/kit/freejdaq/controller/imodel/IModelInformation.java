package edu.kit.freejdaq.controller.imodel;

public interface IModelInformation {

	public boolean addBuildingBlock(String id);
	
	public boolean removeBuildingBlock(String initId, long configId);
	
	public boolean addConnection(String firstChId, String secondChId);
	
	public boolean removeConnection(String firstChId, String secondChId);
	
	public boolean saveConfig(String path);
	
	public boolean loadConfig(String path);
	
}
