package edu.kit.freejdaq.model.core;


import edu.kit.freejdaq.GUI.Configuration.BuildingBlockView;
import edu.kit.freejdaq.model.*;
import java.util.ArrayList;
import edu.kit.freejdaq.model.buildingBlockBuilder.*;
import edu.kit.freejdaq.model.channelLogic.*;
import edu.kit.freejdaq.model.core.*;
import edu.kit.freejdaq.model.facadeViewModel.*;
import edu.kit.freejdaq.model.representationLogic.*;
import edu.kit.freejdaq.model.sensorLogic.*;
import edu.kit.freejdaq.model.transformationLogic.*;

public abstract class BuildingBlock {
	private ArrayList<InChannel> inChannels;
	private ArrayList<OutChannel> outChannels;
	private long configId;
	private String initId;
	private String name;
	private String userInfo;
	
	public BuildingBlock(String initId) {
		this.inChannels =  new ArrayList<InChannel>();
		this.outChannels =  new ArrayList<OutChannel>();
		this.setInitId(initId);
		
		
	}

	
	public void addInChannel(String id, String name) {
		
	}
	public void addOutChannel(String id, String name) {
		
	}
	public void removeInChannel(String id, String name) {
		
	}
	public void removeOutChannel(String id, String name) {
		
	}
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	public String getUserInfo() {
		return userInfo;
	}

	public void setUserInfo(String userInfo) {
		this.userInfo = userInfo;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getInitId() {
		return initId;
	}

	public void setInitId(String initId) {
		this.initId = initId;
	}

	public long getConfigId() {
		return configId;
	}

	public void setConfigId(long configId) {
		this.configId = configId;
	}
	

}
