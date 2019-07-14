package edu.kit.freejdaq.controller.commands;

import java.util.Stack;

/**
 * Singleton CommandManager
 * 
 * @author Jan
 *
 */
public class CommandManager {

	private Stack<Command> doneCommands;
	private Stack<Command> undoneCommands;

	private final static CommandManager INSTANCE = new CommandManager();

	private CommandManager() {
		doneCommands = new Stack<Command>();
		undoneCommands = new Stack<Command>();
	}

	/**
	 * get the singleton instance
	 * 
	 * @return single CommandManager instance
	 */
	public static CommandManager getInstance() {
		return INSTANCE;
	}

	/**
	 * Execute a specific command (cmd). If cmd is undoable, adds it to the undo
	 * stack. Otherwise, the undo stack is not touched. The redo stack is cleared.
	 * 
	 * @param cmd specific Command instance
	 */
	public void runCommand(Command cmd) {
		cmd.execute();
		if (cmd.isUndoable()) {
			doneCommands.push(cmd);
		}
		undoneCommands.clear();
	}

	/**
	 * Undo the latest undoable command.
	 */
	public void undo() {
		Command cmd = doneCommands.pop();
		cmd.unExecute();
		undoneCommands.push(cmd);
	}

	/**
	 * Redo the latest undone command.
	 */
	public void redo() {
		Command cmd = undoneCommands.pop();
		cmd.unExecute();
		doneCommands.push(cmd);
	}

}
