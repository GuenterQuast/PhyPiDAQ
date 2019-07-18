package edu.kit.freejdaq.gui.helpandoption;

import edu.kit.freejdaq.gui.*;
import edu.kit.freejdaq.gui.button.*;
import edu.kit.freejdaq.gui.configuration.*;
import edu.kit.freejdaq.gui.configuration.blockproperties.*;
import edu.kit.freejdaq.gui.exception.*;
import edu.kit.freejdaq.gui.helpandoption.*;
import edu.kit.freejdaq.gui.imodel.*;
import edu.kit.freejdaq.gui.menues.*;


public interface OptionsWindowHandler {
	public void optionsOpened();
	public void colorChanged(String color); 
	public void fontSizeChanged(int size); 

}
