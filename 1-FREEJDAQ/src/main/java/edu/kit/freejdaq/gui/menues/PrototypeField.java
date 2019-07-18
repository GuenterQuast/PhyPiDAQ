package edu.kit.freejdaq.gui.menues;

import edu.kit.freejdaq.gui.*;
import edu.kit.freejdaq.gui.button.*;
import edu.kit.freejdaq.gui.configuration.*;
import edu.kit.freejdaq.gui.configuration.blockproperties.*;
import edu.kit.freejdaq.gui.exception.*;
import edu.kit.freejdaq.gui.helpandoption.*;
import edu.kit.freejdaq.gui.imodel.*;
import edu.kit.freejdaq.gui.menues.*;

import java.util.ArrayList;
import java.util.HashMap;

public class PrototypeField {
	
	private ArrayList<BuildingBlockView> buildingBlockViews;
	private MainWindow mainWindow;
	
	
	public PrototypeField(MainWindow mainWindow) {
		this.buildingBlockViews =  new ArrayList<BuildingBlockView>();
		this.mainWindow = mainWindow;
	}
	
	
	//public void open() {}
	//public void update() {}
		
		
		
		
		
	
public boolean initialize() {
		
		//HashMap hashmap = ViewDirectoryInterface.getFullInitBlock();
		//for (String i : hashmap.keySet()) {
    	//		 BuildingBlockView buildingBlockView = new BuildingBlockView(i, hashmap.get(i));
		// 		 buildingBlockViews.add(buildingBlockView);		
 		//		}
		//if(buildingBlockViews.size() > 0)	{
		//	 return true;
		//   }	
		//
		//
		return false;
		
		
	}
	

}
