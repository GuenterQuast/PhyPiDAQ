package edu.kit.freejdaq.controller.imodel;

public interface IMeasurementRun {

	public boolean start();
	
	public boolean pause();
	
	public boolean resume();
	
	public boolean reset();
	
}
