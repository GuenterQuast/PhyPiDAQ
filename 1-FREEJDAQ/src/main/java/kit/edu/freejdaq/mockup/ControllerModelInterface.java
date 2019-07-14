package Mock;

public interface ControllerModelInterface {
	
	public boolean addBlock(String id);
	
	public boolean removeBlock(String id);
	
	public boolean addConnection(String chId1, String chId2);
	
	public boolean removeConnection(String chId1, String chId2);
	
	public boolean saveConfig(String path);
	
	public boolean loadConfig(String path);
	
	public boolean start();
	
	public boolean pause();
	
	public boolean resume();
	
	public boolean reset();

}
