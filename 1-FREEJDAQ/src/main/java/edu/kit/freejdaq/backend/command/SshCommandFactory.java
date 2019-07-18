package edu.kit.freejdaq.backend.command;

import edu.kit.freejdaq.backend.IMStreamListener;
import edu.kit.freejdaq.backend.command.util.MRunThread;

public class SshCommandFactory implements CommandFactory {

	@Override
	public CommandGetSensorIds createGetSensorIds(int timeout) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public CommandCopyFromPi createCopyFromPi(String nameOfFile, int timeout) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public CommandCopyToPi createCopyToPi(String nameOfFile, int timeout) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public MRunThread createMRunThread(String inChannelId, IMStreamListener listener) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public CommandMRunAtPi createMRunAtPi(String inChannelId, IMStreamListener listener) {
		// TODO Auto-generated method stub
		return null;
	}

}
