package edu.kit.freejdaq.GUI.Configuration;

import edu.kit.freejdaq.GUI.*;
import edu.kit.freejdaq.GUI.Configuration.*;
import edu.kit.freejdaq.GUI.Menues.*;
import edu.kit.freejdaq.GUI.Exception.*;
import edu.kit.freejdaq.GUI.Configuration.BuildingBlockProperties.*;
import edu.kit.freejdaq.GUI.HelpAndOption.*;
import edu.kit.freejdaq.GUI.FacadeModelView.*;
import edu.kit.freejdaq.GUI.Button.*;
 import java.util.ArrayList;
 
 
public class ConfigurationField {

	private ArrayList<BuildingBlockView> buildingBlockViews;
	private MainWindow mainWindow;
	
	public ConfigurationField(MainWindow mainWindow) {
		this.buildingBlockViews =  new ArrayList<BuildingBlockView>();
		this.mainWindow = mainWindow;
		
		
	}
	
	//public void update() {}
	
	
	// beachte: BuildingBlockView ist normalerweise abstract und kann nicht Instanziiert werden
	public void add(BuildingBlock block) {
			BuildingBlockView blockView = new BuildingBlockView(block.getInitId(), block);
			buildingBlockViews.add(blockView);
		
		}
	//public void remove(BuildingBlock block) {}
	//public void open() {}
	
	
}
