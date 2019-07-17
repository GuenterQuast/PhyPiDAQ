package edu.kit.freejdaq.fileservice;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStreamWriter;

import org.yaml.snakeyaml.Yaml;

/**
 * Service to load data from / save data in YAML files. Wrapper for SnakeYaml.
 * 
 * PROTOTYPE
 * 
 * @author Jan
 *
 */
public class YamlService {
	
	//TODO make sure that it actually works (mostly) as intended.

	private static Yaml yaml = new Yaml();

	private YamlService() {

	};

	/**
	 * Loads the data from a YAML file at the specified path.
	 * 
	 * @param path file path in the local file system
	 * @return Java Object containing the YAML file's data
	 * @throws FileNotFoundException if the file at 'path' does not exist, is a
	 *                               directory rather than a regular file, or for
	 *                               some other reason cannot be opened for reading.
	 */
	public static Object load(String path) throws FileNotFoundException {

		InputStream input = new FileInputStream(new File(path));

		return yaml.load(input);

	}

	/**
	 * 
	 * @param path file path in the local file system
	 * @param data Java Object to be saved
	 * @throws FileNotFoundException if the file at 'path' exists but is a directory
	 *                               rather than a regular file, does not exist but
	 *                               cannot be created, or cannot be opened for any
	 *                               other reason
	 */
	public static void save(String path, Object data) throws FileNotFoundException {

		OutputStreamWriter writer = new OutputStreamWriter(new FileOutputStream(path));

		yaml.dump(data, writer);

	}

}
