package edu.kit.freejdaq.backend.command;

import edu.kit.freejdaq.backend.IMStreamListener;

public class CommandMRunAtPi implements Runnable {

	private String inChannelId;
	private boolean resetFlag;
	private boolean pauseFlag;
	
	
	public CommandMRunAtPi(ComToPi comInstance, String inChannelId, IMStreamListener listener) {
		this.inChannelId = inChannelId;
		this.resetFlag = false;
		this.pauseFlag = false;
	}
	
	public void run() {
		// TODO Auto-generated method stub
		
	}
	
	public void raiseResetFlag() {
		// TODO stub
		resetFlag = true;
	}
	
	public void raisePauseFlag() {
		// TODO stub
		pauseFlag = true;
	}
	
	public void executeLocal() {
		// TODO stub
	}

}
