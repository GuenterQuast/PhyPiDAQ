package Mock;

public class ControllerMockUp {
	
	ControllerModelImplement toModel = new ControllerModelImplement();
	
	public boolean blockAdded(String id) {
		toModel.addBlock(id);
		return true;
		
	}
	
	public boolean blockRemoved(String id) {
		toModel.removeBlock(id);
		return true;
	}
	
	public boolean connectionAdded(String id1, String id2) {
		toModel.addConnection(id1, id2);
		return true;
		
	}
	
	public boolean connectionRemoved(String id1, String id2) {
		toModel.removeConnection(id1, id2);
		return true;
	}
	
	public void start() {
		toModel.start();
		
	}
	
	public void pause() {
		toModel.pause();
		
		
	}
	
	public void resume() {
		toModel.resume();
		
		
	}
	
	public void reset() {
		toModel.reset();
		
	}

}
