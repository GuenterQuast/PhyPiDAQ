
public class GuiMockup {

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
	
	// keine Shell zur Zeit verfügbar
	//public void pushShellForVisualisation(Shell shell) {
		
		
	//}
	
	public void updateConfig() {
		System.out.println(" Config updated");
		
	}
	
	
	
	
}
