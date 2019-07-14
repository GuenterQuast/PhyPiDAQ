package edu.kit.freejdaq.controller.commands;

public class CreateChannelConnectionCommand implements Command {
	
	private String startId;
	private String endId;

	public CreateChannelConnectionCommand(String firstChId, String secondChId) {
		startId = firstChId;
		endId = secondChId;
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
