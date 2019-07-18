package edu.kit.freejdaq.backend.command;

public class SshToPi extends ComToPi {
	
	private int port;
	private String ipAddressOfPi;
	private String username;
	private String password;

	public SshToPi(String id, String pathToRemoteDir, String pathToLocalDir) {
		super(id, pathToRemoteDir, pathToLocalDir);
		// TODO Auto-generated constructor stub
	}

	@Override
	public String[] fetchSensorIds(int timeout) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public boolean copyFileFromPi(String nameOfFile, int timeout) {
		// TODO Auto-generated method stub
		return false;
	}

	@Override
	public boolean copyFileToPi(String nameOfFile, int timeout) {
		// TODO Auto-generated method stub
		return false;
	}

	@Override
	public void startMRunAtPi(String inChannelId) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public String readLine() {
		// TODO Auto-generated method stub
		return null;
	}

}
