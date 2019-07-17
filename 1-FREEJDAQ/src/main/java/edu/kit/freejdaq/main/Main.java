package edu.kit.freejdaq.main;

import edu.kit.freejdaq.GUI.MainWindow;
import edu.kit.freejdaq.model.ModelManager;
import edu.kit.freejdaq.phyPiDAQBackend.PickPointForAgentsBasedOnSsh;

public class Main {
	
	private static final MainWindow MAINWINDOW = MainWindow.getInstance();
	private static final PickPointForAgentsBasedOnSsh SSHAGENT = PickPointForAgentsBasedOnSsh.getPickPointForAgentsBasedOnSsh();
	private static final ModelManager MODELMANAGER = new ModelManager();

	public static void main(String[] args) {

		MODELMANAGER.initializeModel();
		SSHAGENT.getAccessToMRun();
		SSHAGENT.getAccessToSensorInfo();

	}

}
