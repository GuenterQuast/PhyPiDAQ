package edu.kit.freejdaq.gui;

import edu.kit.freejdaq.gui.*;
import edu.kit.freejdaq.gui.button.*;
import edu.kit.freejdaq.gui.configuration.*;
import edu.kit.freejdaq.gui.configuration.blockproperties.*;
import edu.kit.freejdaq.gui.exception.*;
import edu.kit.freejdaq.gui.helpandoption.*;
import edu.kit.freejdaq.gui.imodel.*;
import edu.kit.freejdaq.gui.menues.*;





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
