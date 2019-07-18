package edu.kit.freejdaq.model.block;

import edu.kit.freejdaq.gui.configuration.BuildingBlockView;
import edu.kit.freejdaq.model.*;
import java.util.ArrayList;
import java.util.LinkedHashMap;

import edu.kit.freejdaq.model.block.*;
import edu.kit.freejdaq.model.channel.*;
import edu.kit.freejdaq.model.core.*;
import edu.kit.freejdaq.model.igui.*;
import edu.kit.freejdaq.model.representation.*;
import edu.kit.freejdaq.model.sensor.*;
import edu.kit.freejdaq.model.transformation.*;
import java.util.*; 

public class Director {
	
	public Director() {
		
	}
	
	
	// todo read from yaml, ben�tige inhalt
	public BuildingBlock constructBuildingBlock(String id) {
		BuildingBlock block = new BuildingBlock(id);
	return block;	
	}
	
	//To DO finish processor chain
	public BuildingBlock constructBuildingBlock(LinkedHashMap<String, String> lhm) {
		BuildingBlock block = new BuildingBlock("stub");
	return block;
	}
	
	

}
