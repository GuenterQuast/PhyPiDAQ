package edu.kit.freejdaq.GUI.Menues;

import edu.kit.freejdaq.GUI.*;
import edu.kit.freejdaq.GUI.Configuration.*;
import edu.kit.freejdaq.GUI.Menues.*;
import edu.kit.freejdaq.GUI.Exception.*;
import edu.kit.freejdaq.GUI.Configuration.BuildingBlockProperties.*;
import edu.kit.freejdaq.GUI.HelpAndOption.*;
import edu.kit.freejdaq.GUI.FacadeModelView.*;
import edu.kit.freejdaq.GUI.Button.*;
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
