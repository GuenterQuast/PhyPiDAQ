package edu.kit.freejdaq.mockupTest;


public class GuiMockup {
	
	FacadeViewController facade = new ControllerMockUp();

	public GuiMockup() {
		
		
		// TODO Auto-generated constructor stub
	}

	
	public void showGeneralException(String title, String description) {
		System.out.println("General Exception: title " + title + "; Decription: " + description);
		
	}
	
	public void showBuildingBlockException(String id, String title, String description) {
		System.out.println("Block Exception: id" + id + " title " + title + "; Decription: " + description);
		
	}
	
	public void showConnectionException(long id,  String title,  String description) {
		System.out.println("Connection Exception: id" + id + " title " + title + "; Decription: " + description);
		
	}
	
	// keine Shell zur Zeit verfuegbar
	//public void pushShellForVisualisation(Shell shell) {
		
		
	//}
	
	public void updateConfig() {
		System.out.println(" Config updated");
		
	}
	
	public void blockPlaced(String id) {
		facade.blockAdded(id);
	}
	
	public void blockRemoved(String initId, long configId) {
		facade.blockRemoved(initId, configId);
	}
	
	public void connectionAdded(String firstChannelId, String secondChannelId) {
		facade.addConnection(firstChannelId, secondChannelId);
		
	}
	
	public void connectionRemoved(String firstChannelId, String secondChannelId) {
		facade.removeConnection(firstChannelId, secondChannelId);
	}
	//MeasurementRun
	
	public void startPressed(String[] sensorIds, IMStreamListener[] dataListeners) {
		facade.start(sensorIds, dataListeners);
	}
	
	public void pausePressed() {
		facade.pause();
	}
	
	public void resumePressed() {
		facade.resume();
	}
	
	public void resetPressed() {
		facade.reset();
	}
	
	
	
	
}
