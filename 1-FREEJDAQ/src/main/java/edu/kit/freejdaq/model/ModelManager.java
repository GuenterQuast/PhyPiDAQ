package edu.kit.freejdaq.model;


import edu.kit.freejdaq.gui.configuration.BuildingBlockView;
import edu.kit.freejdaq.model.*;
import java.util.ArrayList;
import edu.kit.freejdaq.model.block.*;
import edu.kit.freejdaq.model.channel.*;
import edu.kit.freejdaq.model.core.*;
import edu.kit.freejdaq.model.igui.*;
import edu.kit.freejdaq.model.representation.*;
import edu.kit.freejdaq.model.sensor.*;
import edu.kit.freejdaq.model.transformation.*;

public class ModelManager {
	
	private BuildingBlockDirectory bbDirectory;
	private MeasurementConfiguration mConfig;
	private Director director;
	
	public ModelManager() {
		this.setBbDirectory(new BuildingBlockDirectory());
		this.setmConfig(new MeasurementConfiguration());
		this.setDirector(new Director());
	}
	public boolean initializeModel() {
		
		return true;
	}
	
	
	
	private MeasurementConfiguration createNewMeasurementConfiguration() {
		return 	new MeasurementConfiguration();
	}
	//-createTransformationPrototypesFromYaml():boolean
	//-createRepresentationPrototypesFromYaml():boolean
	//-fetchSensorPrototypesFromBackedn():boolean
	//-pushNetworkConfigToBackend(path: String):boolean
	public Director getDirector() {
		return director;
	}
	public void setDirector(Director director) {
		this.director = director;
	}
	public MeasurementConfiguration getmConfig() {
		return mConfig;
	}
	public void setmConfig(MeasurementConfiguration mConfig) {
		this.mConfig = mConfig;
	}
	public BuildingBlockDirectory getBbDirectory() {
		return bbDirectory;
	}
	public void setBbDirectory(BuildingBlockDirectory bbDirectory) {
		this.bbDirectory = bbDirectory;
	}
	

}

