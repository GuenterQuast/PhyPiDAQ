package edu.kit.freejdaq.model.core;


import edu.kit.freejdaq.model.*;
import java.util.HashMap;
import edu.kit.freejdaq.model.buildingBlockBuilder.*;
import edu.kit.freejdaq.model.channelLogic.*;
import edu.kit.freejdaq.model.core.*;
import edu.kit.freejdaq.model.facadeViewModel.*;
import edu.kit.freejdaq.model.representationLogic.*;
import edu.kit.freejdaq.model.sensorLogic.*;
import edu.kit.freejdaq.model.transformationLogic.*;


import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class BuildingBlockDirectory {
	
	
	private HashMap initHashMap;
	private HashMap configHashMap;
	private static final Logger logger = LogManager.getLogger(BuildingBlockDirectory.class);
	
	
	public BuildingBlockDirectory() {
		
		HashMap<String, BuildingBlock> initHashMap = new HashMap<String, BuildingBlock>();
		HashMap<Long, BuildingBlock> configHashMap = new HashMap<Long, BuildingBlock>();
		
	}
	
	
	
	public boolean isUpdated( ) {
		return false;
		}
	public boolean addInitBuildingBlock(String id, BuildingBlock block ) {
		return false;
		}
	public boolean addConfigBuildingBlock(int id, BuildingBlock block ) {
		return false;
	}
	public boolean removeConfigBuildingBlock(String id ) {
		return false;
		}
	
	//public BuildingBlock getInitBuildingBlock(String id ) {}
	//public BuildingBlock getConfigBuildingBlock(int id ) {}
	public HashMap<String, BuildingBlock> getFullInitBlock() {
		return initHashMap;
	}
	
	
	
	
	public HashMap<String, BuildingBlock> getFullConfigBlock() {
		return configHashMap;
	}
	public boolean addConfigConnection(String bbId1,  int chId1, int chId2, String bbId2) {
		return false;
		}
	public boolean removeConfigConnection(String bbId1,  int chId1, int chId2, String bbId2) {
		return false;
		}
	public boolean getConnection( int chId1, int chId2) {
		return false;
		}
	public boolean setUpdate( boolean bool) {
		return false;
		}
	public boolean checkUpdate() {
		return false;
		}
	
	
	
	
	
	
	
}
