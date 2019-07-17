package edu.kit.freejdaq.model.core;




import java.util.ArrayList;

import edu.kit.freejdaq.GUI.Configuration.BuildingBlockView;
import edu.kit.freejdaq.model.*;
import edu.kit.freejdaq.model.buildingBlockBuilder.*;
import edu.kit.freejdaq.model.channelLogic.*;
import edu.kit.freejdaq.model.core.*;
import edu.kit.freejdaq.model.facadeViewModel.*;
import edu.kit.freejdaq.model.representationLogic.*;
import edu.kit.freejdaq.model.sensorLogic.*;
import edu.kit.freejdaq.model.transformationLogic.*;


public class MeasurementConfiguration {
	
	private BuildingBlockDirectory bbDirectory;
	private String pathToFile;
	private double updateRate;
	private long counter = 0;
	private ArrayList<BuildingBlock> blockList;
	
	public MeasurementConfiguration() {
		this.blockList = new ArrayList<BuildingBlock>();
		this.updateRate = 1.0;
	}
	private long createConfigId(String id) {
		counter++; 
		return counter;
	}
	private BuildingBlock cloneInitBlock(String id) {
		return bbDirectory.getInitBuildingBlock(id);
	}
	public String getPathToFile() {
		return pathToFile;
	}
	
	private boolean checkForCycle() {return false;}
	
	public MeasurementConfiguration getMeasurementConfig() {return this;} 
	public void addBuildingBlock(String id) {
		BuildingBlock block = cloneInitBlock(id);
		long blockConfigId = createConfigId(id);
		blockList.add(block);
		bbDirectory.addConfigBuildingBlock(blockConfigId, block );
	} 
	public void removeBuildingBlock(String initId, long configId) {
		// TODO
		
	} 
	public void addConnection(String firstChannelId, String secondChannelId) {}
	public void removeConnection(String firstChannelId, String secondChannelId) {}
	//public String createModelFromYamlDom(modelDom: YamlDom)

	

}
