package edu.kit.freejdaq.mockupTest;

public interface IMStreamListener {
	public void receiveMDataSet(String channelId, long timeStamp, double value);
	public void connectionTerminated();
}
