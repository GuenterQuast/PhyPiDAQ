package edu.kit.freejdaq.main;

import edu.kit.freejdaq.backend.IAccessToMRun;
import edu.kit.freejdaq.backend.IAccessToSensorInfo;
import edu.kit.freejdaq.backend.PickPointForAgentsBasedOnSsh;
import edu.kit.freejdaq.gui.MainWindow;
import edu.kit.freejdaq.model.ModelManager;

/**
 * Initialisation/Main
 * 
 * @author Jan
 *
 */
public class Main {

	private static final MainWindow MAINWINDOW = MainWindow.getInstance();
	private static final PickPointForAgentsBasedOnSsh SSHAGENT = PickPointForAgentsBasedOnSsh.getPickPointForAgentsBasedOnSsh();
	private static final ModelManager MODELMANAGER = new ModelManager();

	public static void main(String[] args) {

		MODELMANAGER.initializeModel();

		IAccessToMRun mRunAccess = SSHAGENT.getAccessToMRun();
		IAccessToSensorInfo sensorInfoAccess = SSHAGENT.getAccessToSensorInfo();

	}

}
