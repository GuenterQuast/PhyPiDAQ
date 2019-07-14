package edu.kit.freejdaq.controller.viewfacade;

import edu.kit.freejdaq.controller.commands.AddBlockToConfigCommand;
import edu.kit.freejdaq.controller.commands.CommandManager;
import edu.kit.freejdaq.controller.commands.RemoveBlockFromConfigCommand;

public class BlockAction {

	private CommandManager cmdManager = CommandManager.getInstance();

	public boolean blockPlaced(String initId) {
		cmdManager.runCommand(new AddBlockToConfigCommand(initId));
		return true;
	}
	
	public boolean blockMoved() {
		return true;
	}
	
	public boolean blockRemoved(String configId) {
		cmdManager.runCommand(new RemoveBlockFromConfigCommand(configId));
		return true;
	}
	
}
