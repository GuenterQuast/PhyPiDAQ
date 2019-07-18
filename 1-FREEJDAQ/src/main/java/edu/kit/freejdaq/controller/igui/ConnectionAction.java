package edu.kit.freejdaq.controller.igui;

import edu.kit.freejdaq.controller.commands.CommandManager;
import edu.kit.freejdaq.controller.commands.CreateChannelConnectionCommand;

public class ConnectionAction {
	
	private CommandManager cmdManager = CommandManager.getInstance();
	
	public boolean connectionAdded(String firstChId, String secondChId) {
		cmdManager.runCommand(new CreateChannelConnectionCommand(firstChId, secondChId));
		return true;
	}
	
	public boolean connectionRemoved() {
		return true;
	}

}
