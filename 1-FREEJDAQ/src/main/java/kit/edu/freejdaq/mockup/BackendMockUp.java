package kit.edu.freejdaq.mockup;

public class BackendMockUp {

	public BackendMockUp() {

	}
	//IAccessToMRun
	public boolean start(String[] sensorIds, IMStreamListener[] dataListeners) {
		System.out.println("started");
		return true;
	}
	public boolean pause(){
		System.out.println("paused");
		return true;
	}
	public boolean resume(){
		System.out.println("resumed");
		return true;
	}
	public boolean reset(){
		System.out.println("resetted");
		return true;
	}
	//IAccessToSensorInfo
	public String[] getIdsOfAvailableSensorsSensors(){
		String[] mockGetIdsOfAvailableSensorsSensors = new String[] {"ID1","ID2","ID3"};
		System.out.println("ID1, ID2, ID3");
		return mockGetIdsOfAvailableSensorsSensors;
	}
	public boolean copyYamlFileFromPi(String sensorId){
		System.out.println("Yaml File copyed from Pi");
		return true;
	}
	public boolean copyYamlFileToPi(String sensorId){
		System.out.println("Yaml File copyed to Pi");
		return true;
	}
	//IMStreamListener
	public void receiveMDataSet(String channelId, long timeStamp, double value){
		System.out.println("Data recieved");
	}
	public void connectionTerminated(){
		System.out.println("connection terminated");
	}
}
