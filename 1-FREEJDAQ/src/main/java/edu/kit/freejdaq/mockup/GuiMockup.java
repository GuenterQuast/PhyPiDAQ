
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
		facade.addBuildingBlock(id);
	}
	
	public void blockRemoved(String initId, long configId) {
		facade.removeBuildingBlock(initId, configId);
	}
	
	public boolean connectionAdded(String firstChannelId, String secondChannelId) {
		facade.addConnection(firstChannelId, secondChannelId);
		
	}
	
	public boolean connectionRemoved(String firstChannelId, String secondChannelId) {
		facade.removeConnection(firstChannelId, secondChannelId);
	}
	//MeasurementRun
	
	public boolean startPressed(String[] sensorIds, IMStreamListener[] dataListeners) {
		facade.start(sensorIds, dataListeners);
	}
	
	public boolean pausePressed() {
		facade.pause();
	}
	
	public boolean resumePressed() {
		facade.resume();
	}
	
	public boolean resetPressed() {
		facade.reset();
	}
	
	
	
	
}
