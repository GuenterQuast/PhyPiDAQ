package edu.kit.freejdaq.mockupTest;

public class Main {
	
	public static void main(String[] args) {
		
		GuiMockup gui = new GuiMockup();
				
		gui.blockPlaced("1");
		gui.blockRemoved("1", 2);
		gui.connectionAdded("2", "3");
		gui.connectionRemoved("4", "5");
		gui.pausePressed();
		gui.resumePressed();
		gui.resetPressed();
		
		
	}

}
