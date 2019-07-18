package edu.kit.freejdaq.model.core;


import edu.kit.freejdaq.model.*;
import edu.kit.freejdaq.model.block.*;
import edu.kit.freejdaq.model.channel.*;

import java.util.HashMap;

import edu.kit.freejdaq.model.core.*;
import edu.kit.freejdaq.model.igui.*;
import edu.kit.freejdaq.model.representation.*;
import edu.kit.freejdaq.model.sensor.*;
import edu.kit.freejdaq.model.transformation.*;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class BuildingBlockDirectory {
	
	
	private HashMap<String, BuildingBlock> initHashMap;
	private HashMap<Long, BuildingBlock> configHashMap;
	private static final Logger logger = LogManager.getLogger(BuildingBlockDirectory.class);
	
	
	public BuildingBlockDirectory() {
		
		this.initHashMap = new HashMap<String, BuildingBlock>();
		this.configHashMap = new HashMap<Long, BuildingBlock>();
		
	}
	
	
	
	public boolean isUpdated( ) {
		return false;
		}
	public boolean addInitBuildingBlock(String id, BuildingBlock block ) {
		
		initHashMap.put(id, block);
		logger.trace("BuildingBlock added to BuildingBlockDirectory initHashMap with initId: " +  id );
		return true;
		}
	public boolean addConfigBuildingBlock(long id, BuildingBlock block ) {
		configHashMap.put(id, block);
		logger.trace("BuildingBlock added to BuildingBlockDirectory configHashMap with configId: " +  id );
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
