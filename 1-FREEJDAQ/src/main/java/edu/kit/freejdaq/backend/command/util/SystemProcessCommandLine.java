package edu.kit.freejdaq.backend.command.util;

import java.io.BufferedReader;
import java.io.Writer;

public class SystemProcessCommandLine {
	
	private Runtime anotherLocalSystemProcess;
	private BufferedReader standardOutput;
	private Writer standardInput;
	
	public SystemProcessCommandLine() {
		
	}
	
	public int execute(String commandToExecute) {
		// TODO stub
		return 0;
	}
	
	public BufferedReader getStdOutput() {
		return standardOutput;
	}
	
	public Writer getStdInput() {
		return standardInput;
	}

}
