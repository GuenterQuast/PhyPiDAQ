package edu.kit.freejdaq.mockuptest;

public interface IMStreamListener {
	public void receiveMDataSet(String channelId, long timeStamp, double value);
	public void connectionTerminated();
}
