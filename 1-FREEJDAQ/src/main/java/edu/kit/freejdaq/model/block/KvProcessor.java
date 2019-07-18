package edu.kit.freejdaq.model.block;

import java.util.LinkedHashMap;

import edu.kit.freejdaq.gui.configuration.BuildingBlockView;
import edu.kit.freejdaq.model.*;
import edu.kit.freejdaq.model.block.*;
import edu.kit.freejdaq.model.channel.*;
import edu.kit.freejdaq.model.core.*;
import edu.kit.freejdaq.model.igui.*;
import edu.kit.freejdaq.model.representation.*;
import edu.kit.freejdaq.model.sensor.*;
import edu.kit.freejdaq.model.transformation.*;

public abstract class KvProcessor {
	
	
	protected KvProcessor successor;
	protected BuildingBlock block;

	public KvProcessor() {
		// TODO Auto-generated constructor stub
	}
	
	public abstract void processKvPair(LinkedHashMap<String, String> lhm);

	public KvProcessor getSuccessor() {
		return successor;
	}

	public void setSuccessor(KvProcessor successor) {
		this.successor = successor;
	}
}
