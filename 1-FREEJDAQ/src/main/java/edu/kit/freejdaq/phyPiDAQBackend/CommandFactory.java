package edu.kit.freejdaq.phyPiDAQBackend;

public interface CommandFactory {
	
	public CommandGetSensorIds createGetSensorIds(int timeout);
	
	public CommandCopyFromPi createCopyFromPi(String nameOfFile, int timeout);
	
	public CommandCopyToPi createCopyToPi(String nameOfFile, int timeout);
	
	public MRunThread createMRunThread(String inChannelId, IMStreamListener listener);

	public CommandMRunAtPi createMRunAtPi(String inChannelId, IMStreamListener listener);
	
}
