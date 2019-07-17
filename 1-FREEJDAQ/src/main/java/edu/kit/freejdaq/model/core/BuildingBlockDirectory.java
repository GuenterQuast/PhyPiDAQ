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
	
	
	private HashMap<String, BuildingBlock> initHashMap;
	private HashMap<Long, BuildingBlock> configHashMap;
	private static final Logger logger = LogManager.getLogger(BuildingBlockDirectory.class);
	
	
	public BuildingBlockDirectory() {
		
		HashMap<String, BuildingBlock> initHashMap = new HashMap<String, BuildingBlock>();
		HashMap<Long, BuildingBlock> configHashMap = new HashMap<Long, BuildingBlock>();
		
	}
	
	
	
	public boolean isUpdated( ) {
		return false;
		}
	public boolean addInitBuildingBlock(String id, BuildingBlock block ) {
		initHashMap.put(id, block);
		return true;
		}
	public boolean addConfigBuildingBlock(long id, BuildingBlock block ) {
		configHashMap.put(id, block);
		return true;
	}
	public boolean removeConfigBuildingBlock(Long id ) {
		configHashMap.remove(id);
		return true;
		}
	
	public BuildingBlock getInitBuildingBlock(String id ) {
		return (BuildingBlock) initHashMap.get(id);
	}
	public BuildingBlock getConfigBuildingBlock(long id ) {
		return (BuildingBlock) configHashMap.get(id);
	}
	public HashMap<String, BuildingBlock> getFullInitBlock() {
		return initHashMap;
	}
	
	public HashMap<Long, BuildingBlock> getFullConfigBlock() {
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
