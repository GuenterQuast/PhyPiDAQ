package edu.kit.freejdaq.backend.command;

import java.io.BufferedReader;

public abstract class ComToPi {
	
	private String idOfSensorInChannelOrSensorInfoTask;
	private String pathToRemoteDir;
	private String pathToLocalDir;
	
	public ComToPi(String id, String pathToRemoteDir, String pathToLocalDir) {
		idOfSensorInChannelOrSensorInfoTask = id;
		this.pathToRemoteDir = pathToRemoteDir;
		this.pathToLocalDir = pathToLocalDir;
	}
	
	public abstract String[] fetchSensorIds(int timeout);
	
	public abstract boolean copyFileFromPi(String nameOfFile, int timeout);
	
	public abstract boolean copyFileToPi(String nameOfFile, int timeout);
	
	public abstract void startMRunAtPi(String inChannelId);
	
	public abstract String readLine();

}
