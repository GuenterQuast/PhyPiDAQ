package edu.kit.freejdaq.mockup;

public interface IMStreamListener {
	public void receiveMDataSet(String channelId, long timeStamp, double value);
	public void connectionTerminated();
}
