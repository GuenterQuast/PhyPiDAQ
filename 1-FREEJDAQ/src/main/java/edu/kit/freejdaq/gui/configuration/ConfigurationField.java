package edu.kit.freejdaq.gui.configuration;

import edu.kit.freejdaq.gui.*;
import edu.kit.freejdaq.gui.button.*;
import edu.kit.freejdaq.gui.configuration.*;
import edu.kit.freejdaq.gui.configuration.blockproperties.*;
import edu.kit.freejdaq.gui.exception.*;
import edu.kit.freejdaq.gui.helpandoption.*;
import edu.kit.freejdaq.gui.imodel.*;
import edu.kit.freejdaq.gui.menues.*;

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
