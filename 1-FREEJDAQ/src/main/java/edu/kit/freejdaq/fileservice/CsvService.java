package edu.kit.freejdaq.fileservice;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

import com.opencsv.CSVReader;
import com.opencsv.CSVWriter;

public class CsvService {

	public void writeDataIntoCsv(String filePath, List<String[]> data) { 

	    // specify filepath and filename by filepath  
	    File file = new File(filePath); 
	    	if (file.exists()) {
	    		System.out.println("This file already exists");
	    	} else 
	    		

	    try { 

	        // create CSVWriter object filewriter object as parameter 
	        CSVWriter writer = new CSVWriter(new FileWriter(file), ',', 
	        		CSVWriter.NO_QUOTE_CHARACTER, 
                    CSVWriter.DEFAULT_ESCAPE_CHARACTER, 
                    CSVWriter.DEFAULT_LINE_END); 

	        writer.writeAll(data); 

	        // closing writer connection 
	        writer.close(); 
	    } 
	    catch (IOException e) { 
	        // TODO Auto-generated catch block 
	        e.printStackTrace(); 
	    } 
	}
	//This method reads out all lines of data inside the given csv-file and stores it in an Array-List
	public List<String[]> readDataFromCsv(String path) {
		
		//List of data inside the csv
		List<String[]> records = new ArrayList<String[]>();
		try (CSVReader csvReader = new CSVReader(new FileReader(path));) {
		    String[] values = null;
		    while ((values = csvReader.readNext()) != null) {
		        records.add(values);
		    }
		} catch (FileNotFoundException e) {
			//throwException
			e.printStackTrace();
		} catch (IOException e) {
			//throwException
			e.printStackTrace();
		}
		return records;
	}
	
	public void renameOrMoveCsvFile(String oldFilePath, String newFilePath) {
		
		boolean succes = false;
		
		//old File or Directory
		File file = new File(oldFilePath);
		//new File or Directory
		File newFile = new File(newFilePath);
		
		if(newFile.exists()) {
			//throwException
		} else {
			succes = file.renameTo(newFile);
		}
			
		if(!succes) {
			//throwException
		}
	}
}
