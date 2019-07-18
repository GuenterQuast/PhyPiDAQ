package edu.kit.freejdaq.backend.command;

import edu.kit.freejdaq.backend.IMStreamListener;
import edu.kit.freejdaq.backend.command.util.MRunThread;

public interface CommandFactory {
	
	public CommandGetSensorIds createGetSensorIds(int timeout);
	
	public CommandCopyFromPi createCopyFromPi(String nameOfFile, int timeout);
	
	public CommandCopyToPi createCopyToPi(String nameOfFile, int timeout);
	
	public MRunThread createMRunThread(String inChannelId, IMStreamListener listener);

	public CommandMRunAtPi createMRunAtPi(String inChannelId, IMStreamListener listener);
	
}
