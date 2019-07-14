package kit.edu.freejdaq.mockup;

public interface IAccessToMRun {
	public boolean start(String[] sensorIds, IMStreamListener[] dataListeners);
	public boolean pause();
	public boolean resume();
	public boolean reset();
}
