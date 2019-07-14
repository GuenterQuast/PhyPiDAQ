package edu.kit.freejdaq.GUI;

import edu.kit.freejdaq.GUI.*;
import edu.kit.freejdaq.GUI.Configuration.*;
import edu.kit.freejdaq.GUI.Menues.*;
import edu.kit.freejdaq.GUI.Exception.*;
import edu.kit.freejdaq.GUI.Configuration.BuildingBlockProperties.*;
import edu.kit.freejdaq.GUI.HelpAndOption.*;
import edu.kit.freejdaq.GUI.FacadeModelView.*;
import edu.kit.freejdaq.GUI.Button.*;





public class MainWindow {

	private String colorScheme;
	private long fontSize;
	// private OptionsWindow optionsWindow;
	// private HelpWindow helpWindow;
	// private ButtonField buttonField;
	private ConfigurationField configurationField;
	private static MainWindow instance = null;
	private PrototypeField prototypeField;
    
    private MainWindow(){
    	//this.optionsWindow = new OptionsWindow();
    	//this.helpWindow = new HelpWindow();
    	// this.prototypField = new PrototypField();
    	// this.buttonField = new ButtonField();
    	configurationField = new ConfigurationField(this);
    	prototypeField = new PrototypeField(this);
    }
    public static MainWindow getInstance(){
          if(instance == null){
                 instance = new MainWindow();
                 
          }
          return instance;
    }
   // public static void exit(){}
	public PrototypeField getPrototypeField() {
		return prototypeField;
	}
	public void setPrototypeField(PrototypeField prototypeField) {
		this.prototypeField = prototypeField;
	}
	
	
}
