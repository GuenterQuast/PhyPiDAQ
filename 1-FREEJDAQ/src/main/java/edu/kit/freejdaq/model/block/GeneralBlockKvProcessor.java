package edu.kit.freejdaq.model.block;

import java.util.LinkedHashMap;
import edu.kit.freejdaq.gui.configuration.BuildingBlockView;
import edu.kit.freejdaq.model.*;
import edu.kit.freejdaq.model.block.*;
import edu.kit.freejdaq.model.channel.*;
import edu.kit.freejdaq.model.core.*;
import edu.kit.freejdaq.model.igui.*;
import edu.kit.freejdaq.model.representation.*;
import edu.kit.freejdaq.model.sensor.*;
import edu.kit.freejdaq.model.transformation.*;

public class GeneralBlockKvProcessor extends KvProcessor{

	public GeneralBlockKvProcessor() {
		// TODO Auto-generated constructor stub
	}
	
	
	public void processKvPair(LinkedHashMap<String, String> lhm) {
		String blockType = lhm.get("type");
		
		switch(blockType) {
		  case "Sensor":
		    this.successor = new SensorKvProcessor();
		    break;
		  case "Transformation":
		    // code to create Transformation
		    break;
		  case "Representation":
			    // code to create Representation
			    break;
		  default:
		    // Code to create general Block
		}
		successor.processKvPair(lhm);
		
		
	}

}
