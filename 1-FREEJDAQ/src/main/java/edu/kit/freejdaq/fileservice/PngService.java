package edu.kit.freejdaq.fileservice;

import java.awt.image.BufferedImage;
import java.io.File;

import javax.imageio.ImageIO;

public class PngService {
	
	public void savePng(String path, BufferedImage image) {
		try {
			File file = new File(path);
				if(file.exists()) {
					System.out.println("File already exists");
				} else 
					
			ImageIO.write(image, "PNG", file);
		}
		catch(Exception e) {
			//throw Exception
		}
	}
}
