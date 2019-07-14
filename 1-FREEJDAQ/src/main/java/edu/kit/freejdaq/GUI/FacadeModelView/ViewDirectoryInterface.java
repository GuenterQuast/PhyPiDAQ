package edu.kit.freejdaq.GUI.FacadeModelView;


import edu.kit.freejdaq.GUI.*;
import edu.kit.freejdaq.GUI.Configuration.*;
import edu.kit.freejdaq.GUI.Menues.*;
import edu.kit.freejdaq.GUI.Exception.*;
import edu.kit.freejdaq.GUI.Configuration.BuildingBlockProperties.*;
import edu.kit.freejdaq.GUI.HelpAndOption.*;
import edu.kit.freejdaq.GUI.FacadeModelView.*;
import edu.kit.freejdaq.GUI.Button.*;


import java.util.HashMap;


public interface ViewDirectoryInterface {
	
	public BuildingBlock getInitBuildingBlock(String id);
	public BuildingBlock getConfigBuildingBlock(int id);
	public HashMap getFullInitBlock();
	public HashMap getFullConfigBlock();
	public boolean getConnection(int chId1, int chId2);
	
	
	
	// falls True, wie erkenne ich, was verändert wurde?
	public boolean checkForUpdate();
	
	
}
