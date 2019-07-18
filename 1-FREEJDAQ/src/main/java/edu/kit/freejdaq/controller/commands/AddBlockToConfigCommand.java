package edu.kit.freejdaq.controller.commands;

import edu.kit.freejdaq.controller.imodel.IModelInformation;
import edu.kit.freejdaq.controller.imodel.PickupPointModelFacade;

public class AddBlockToConfigCommand implements Command {
	
	private String blockId;
	private IModelInformation model;
	
	public AddBlockToConfigCommand(String initId) {
		blockId = initId;
		model = PickupPointModelFacade.getModelInformation();
	}

	public boolean isUndoable() {
		return true;
	}

	public void execute() {
		// TODO Auto-generated method stub
		model.addBuildingBlock(blockId);
	}

	public void unExecute() {
		// TODO Auto-generated method stub

	}

}
