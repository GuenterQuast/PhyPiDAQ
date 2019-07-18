package edu.kit.freejdaq.gui.imodel;


import edu.kit.freejdaq.gui.*;
import edu.kit.freejdaq.gui.button.*;
import edu.kit.freejdaq.gui.configuration.*;
import edu.kit.freejdaq.gui.configuration.blockproperties.*;
import edu.kit.freejdaq.gui.exception.*;
import edu.kit.freejdaq.gui.helpandoption.*;
import edu.kit.freejdaq.gui.imodel.*;
import edu.kit.freejdaq.gui.menues.*;

import java.util.HashMap;


public interface ViewDirectoryInterface {
	
	public BuildingBlock getInitBuildingBlock(String id);
	public BuildingBlock getConfigBuildingBlock(int id);
	public HashMap getFullInitBlock();
	public HashMap getFullConfigBlock();
	public boolean getConnection(int chId1, int chId2);
	
	
	
	// falls True, wie erkenne ich, was veraendert wurde?
	public boolean checkForUpdate();
	
	
}
