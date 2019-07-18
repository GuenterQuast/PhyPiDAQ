package edu.kit.freejdaq.backend;

public class PickPointForAgentsBasedOnSsh {
	
	private final static PickPointForAgentsBasedOnSsh INSTANCE = new PickPointForAgentsBasedOnSsh();
	
	private PickPointForAgentsBasedOnSsh() {
		// empty
	}

	public static PickPointForAgentsBasedOnSsh getPickPointForAgentsBasedOnSsh() {
		return INSTANCE;
	}

	public IAccessToMRun getAccessToMRun() {
		// TODO Auto-generated method stub
		return null;
	}

	public IAccessToSensorInfo getAccessToSensorInfo() {
		// TODO Auto-generated method stub
		return null;
	}

}
