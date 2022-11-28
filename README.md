# FileProperties
## FileProperties
Stores file properties in a properties object.

## Screenshots

![fileproperties](https://user-images.githubusercontent.com/42722171/202273600-e83bcccf-a2e7-4666-b5dd-3d5e33c5f1be.JPG)

## Installation

Copy zip file to your machine. Unzip file an copy/Paste folder to FreeCAD/Mod folder

* Restart FreeCAD.

## Usage

* Select the file Properties icon. If this is the first time you have ran this on a file an Object called Properties will be created in your FreeCAD file. Highlighting this object will not show any properties.  
* To add properties manually, click the new row button, then enter the Name in the left column and the value on the right. Press "SaveClose to save the properties and close the dialog. 
* To add properties from a TechDraw drawing, open a file that has a Drawing page. Click the "From Drawing" button and the dialog box will fill with the properties from the drawing. This program will only use symbols which can be used in python. If you get an error message that an invalad symbol such as -, +, *, $ was used you will need to change the charater to an underscore or change the Name of the property. This can be done using a text editor and searching for the reported word. 
* Change the property valus in the  right hand column and click "UpdateSave" to write the new values to the drawing and save them or click "SaveClose". 
* Values can also be made in the data tab by highlighting the properties icon in the tree.
* 

## Developer

Dan Miel ([@DanMiel](https://github.com/DanMiel))

## License

GPLv3 ([LICENSE](LICENSE))
