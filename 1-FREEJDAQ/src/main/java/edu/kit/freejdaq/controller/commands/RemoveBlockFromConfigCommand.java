package edu.kit.freejdaq.controller.commands;

import edu.kit.freejdaq.controller.imodel.IModelInformation;
import edu.kit.freejdaq.controller.imodel.PickupPointModelFacade;

public class RemoveBlockFromConfigCommand implements Command {
	
	private String blockId;
	private IModelInformation model;
	
	public RemoveBlockFromConfigCommand(String configId) {
		blockId = configId;
		model = PickupPointModelFacade.getModelInformation();
	}

	public boolean isUndoable() {
		return true;
	}

	public void execute() {
		// TODO Auto-generated method stub
	}

	public void unExecute() {
		// TODO Auto-generated method stub

	}

}
