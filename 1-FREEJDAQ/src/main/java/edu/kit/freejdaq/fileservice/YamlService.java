package edu.kit.freejdaq.fileservice;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStreamWriter;
import java.util.Map;

import org.yaml.snakeyaml.Yaml;

public class YamlService {
	
	private static Yaml yaml = new Yaml();
	
	
	public static Map<String, Object> readFromYaml(String path) {
		
		Map<String, Object> object = null;
		try {
		InputStream inputStream = new FileInputStream(new File(path));
			object = yaml.load(inputStream);
		}
		catch (FileNotFoundException e) {
			System.out.println("here");
		}
		return object;
	}
	
	public static void saveIntoYaml(String path, Map<String, Object> object) throws FileNotFoundException {
		OutputStreamWriter writer = new OutputStreamWriter(new FileOutputStream(path));
		yaml.dump(object, writer);
	}
}
 