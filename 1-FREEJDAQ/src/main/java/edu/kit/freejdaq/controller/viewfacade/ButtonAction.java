package edu.kit.freejdaq.controller.viewfacade;

import edu.kit.freejdaq.controller.commands.CommandManager;

public class ButtonAction {
	
	private CommandManager cmdManager = CommandManager.getInstance();

	public boolean undoPressed() {
		cmdManager.undo();
		return true;
	}

	public boolean redoPressed() {
		cmdManager.redo();
		return true;
	}
	
}
