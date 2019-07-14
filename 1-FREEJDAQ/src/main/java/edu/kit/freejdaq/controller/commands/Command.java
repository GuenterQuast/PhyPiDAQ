package edu.kit.freejdaq.controller.commands;

/**
 * General command interface. Concrete commands must implement this.
 * 
 * @author Jan
 *
 */
public interface Command {

	/**
	 * Some commands are classified as undoable, others are not.
	 * 
	 * @return true if undoable, false if not undoable
	 */
	public boolean isUndoable();

	/**
	 * Execute the given command.
	 */
	public void execute();

	/**
	 * Un-execute the given command. Does nothing if the command is not undoable.
	 */
	public void unExecute();

}
