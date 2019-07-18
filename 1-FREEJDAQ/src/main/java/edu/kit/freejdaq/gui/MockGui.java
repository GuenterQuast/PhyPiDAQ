 package edu.kit.freejdaq.gui;

public class MockGui {

	public MockGui() {
		
		
	}
	
	
	
	
	
	public void updateConfig() {
		
		
	}
	
	
	//public void pushShellForVisualisation(Shell shell) {}
		
	
	// erstelle ein Gui Grundgeruest, das eine Prototypsammlung aus dem Model holt 
	
	public void initializeGui() {
		MainWindow mainWindow = MainWindow.getInstance();
		if (mainWindow.getPrototypeField().initialize()== true)
		{
			 System.out.println("PrototypeField successfull initialized");
		}
		else
		{
			System.out.println("Init of PrototypeField failed");
		}
		//mainWindow.configurationField.
		
	}	
	
	
	
	
	
	
}
