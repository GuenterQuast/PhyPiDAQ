package edu.kit.freejdaq.model;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.yaml.snakeyaml.Yaml;

import edu.kit.freejdaq.gui.configuration.BuildingBlockView;
import edu.kit.freejdaq.model.*;
import edu.kit.freejdaq.model.block.*;
import edu.kit.freejdaq.model.channel.*;
import edu.kit.freejdaq.model.core.*;
import edu.kit.freejdaq.model.igui.*;
import edu.kit.freejdaq.model.representation.*;
import edu.kit.freejdaq.model.sensor.*;
import edu.kit.freejdaq.model.transformation.*;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.*; 

class testModel {

	@BeforeAll
	static void setUpBeforeClass() throws Exception {
		
		
	}

	@AfterAll
	static void tearDownAfterClass() throws Exception {
	}

	@Test
	void test() throws IOException {
		ModelManager modMan = new ModelManager();
		Yaml yaml = new Yaml();
        InputStream in = new FileInputStream("src/main/resources/modelStuff/test2.yaml"); 
        LinkedHashMap<String, String> lhm = yaml.load(in);
        // id = BMP180
		BuildingBlock block = modMan.getDirector().constructBuildingBlock(lhm.get("id"));
		modMan.getBbDirectory().addInitBuildingBlock(block.getInitId(),block );
		BuildingBlock otherBlock = modMan.getBbDirectory().getInitBuildingBlock("BMP180" );
		assertEquals(block, otherBlock);
		
		//fail("Not yet implemented");
	}

}
