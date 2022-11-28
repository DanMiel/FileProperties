# -*- coding: utf-8 -*-
#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2022 Dan Miel                                           *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************
"""
This stores file properties in an object. 
The Files can be written to a drawing.
If you have a drwing with the properties you want,
open a file with the drawing and copy the propeties
to the dialog box. 
Saving the dialog saves the properties to the properties object.
You can copy the properties object to anther file.

"""

from typing import Collection
import os
import FreeCAD
import FreeCADGui
from PySide import QtGui, QtCore
from PySide.QtGui import *
#import math
#import numpy
#import Part
#import Draft
from numpy import f2py

class globaluseclass:
    def __init__(self, name):
        self.proplist = []
g = globaluseclass("g")

class info:
    def __init__(self):
        self.fname = 'Empty'
        self.type = 'None'

    def __str__(self):
        return f'{self.fname, self.type}'

class properties():
    def __init__(self):
        pass

    def openproperties(self):
        g.proplist = []
        doc = FreeCAD.activeDocument()
        propobj = doc.getObject('Properties')
        if propobj is None:
            msg = 'There are no properties Object\nDo you want to create one?'
            FreeCAD.activeDocument().addObject("App::FeaturePython", 'Properties')
        propobj = doc.getObject('Properties')
        if propobj == None:
            print("No properties made")
            return()
        else:
            pass 
        pl = []
        for e in propobj.PropertiesList:
            if e in 'ExpressionEngine, Label, Label2, Proxy, Visibility':
                pass
            else:
                pl.append(str(e))
        for w in pl:
            g.proplist.append([w, propobj.getPropertyByName(w)])
        form1.loadtable()
        form1.show()

    def createDefaultprops(self):

        doc = FreeCAD.ActiveDocument
        ob = doc.getObject('Properties')  #FreeCAD.activeDocument().addObject("App::FeaturePython", 'Properties')
        for e in ob.PropertiesList:
            ob.removeProperty(e)
        ob.addProperty("App::PropertyString", "FileName", "Prop").FileName = doc.Name        
        ob.addProperty("App::PropertyString", "Ver", "Prop").Ver = ''
        ob.addProperty("App::PropertyString", "FileType", "Prop").FileType = ''
        ob.addProperty("App::PropertyString", "CreatedBy", "Prop").CreatedBy = ''
        ob.addProperty("App::PropertyString", "CreatedDate", "Prop").CreatedDate = ''
        ob.addProperty("App::PropertyString", "Project", "Prop").Project = ''
        ob.addProperty("App::PropertyString", "Material", "Prop").Material = ''
        ob.addProperty("App::PropertyString", "MfgNumber", "Prop").MfgNumber = ''
        ob.addProperty("App::PropertyString", "Description", "Prop").Description = ''
        g.proplist = []
        for e in ob.PropertiesList:
            if e in 'ExpressionEngine, Label, Label2, Proxy, Visibility':
                pass
            else:
                g.proplist.append([e, ob.getPropertyByName(e)])
        print('proplist')
        print(g.proplist)
        form1.loadtable()

properties = properties()

class formMain(QtGui.QMainWindow):

    def __init__(self, name):
        self.name = name
        super(formMain, self).__init__()
        self.setWindowTitle('File Properties')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(280, 250, 300, 500)
        self.setStyleSheet("font:10pt arial MS")                
        
        self.btnSaveClose = QtGui.QPushButton(self)
        self.btnSaveClose.move(200, 4)
        self.btnSaveClose.setFixedWidth(70)
        self.btnSaveClose.setFixedHeight(24)
        self.btnSaveClose.setToolTip("Save the properties and close dialog")
        self.btnSaveClose.setText("Save&Close")
        self.btnSaveClose.clicked.connect(lambda:self.SaveClose())

        self.btnaddRow = QtGui.QPushButton(self)
        self.btnaddRow.move(4, 4)
        self.btnaddRow.setFixedWidth(70)
        self.btnaddRow.setFixedHeight(24)
        self.btnaddRow.setToolTip("Adds a row for a new Property")
        self.btnaddRow.setText("Add Row")
        self.btnaddRow.clicked.connect(lambda:self.addrow())

        self.btnCancel = QtGui.QPushButton(self)
        self.btnCancel.move(200, 30)
        self.btnCancel.setFixedWidth(60)
        self.btnCancel.setFixedHeight(24)
        self.btnCancel.setToolTip("Close this form.")
        self.btnCancel.setText("Cancel")
        self.btnCancel.clicked.connect(lambda:self.closeme())

        self.btnCreateDefault = QtGui.QPushButton(self)
        self.btnCreateDefault.move(300, 4)
        self.btnCreateDefault.setFixedWidth(60)
        self.btnCreateDefault.setFixedHeight(24)
        self.btnCreateDefault.setToolTip("Create default properties.")
        self.btnCreateDefault.setText("Defaults")
        self.btnCreateDefault.clicked.connect(lambda:self.createdefaultprop())

        self.btnPropsfromDrawing = QtGui.QPushButton(self)
        self.btnPropsfromDrawing.move(80, 4)
        self.btnPropsfromDrawing.setFixedWidth(100)
        self.btnPropsfromDrawing.setFixedHeight(24)
        self.btnPropsfromDrawing.setToolTip("Copy properties from drawing.")
        self.btnPropsfromDrawing.setText("From Drawing")
        self.btnPropsfromDrawing.clicked.connect(lambda:self.copyfromdrawing())
        
        self.btnAddDate = QtGui.QPushButton(self)
        self.btnAddDate.move(4, 30)
        self.btnAddDate.setFixedWidth(70)
        self.btnAddDate.setFixedHeight(24)
        self.btnAddDate.setToolTip("Add date to cell.")
        self.btnAddDate.setText("Add Date")
        self.btnAddDate.clicked.connect(lambda:self.addDate())

        self.btnAddFileName = QtGui.QPushButton(self)
        self.btnAddFileName.move(4, 58)
        self.btnAddFileName.setFixedWidth(70)
        self.btnAddFileName.setFixedHeight(24)
        self.btnAddFileName.setToolTip("Add file name to selected cell.")
        self.btnAddFileName.setText("Add Name")
        self.btnAddFileName.clicked.connect(lambda:self.addFilename())

        self.btnUpdateDraw = QtGui.QPushButton(self)
        self.btnUpdateDraw.move(80, 30)
        self.btnUpdateDraw.setFixedWidth(100)
        self.btnUpdateDraw.setFixedHeight(24)
        self.btnUpdateDraw.setToolTip("Save properties and update drawing title.")
        self.btnUpdateDraw.setText("Update Save")
        self.btnUpdateDraw.clicked.connect(lambda:self.updateandsave())

        self.btnAddScale = QtGui.QPushButton(self)
        self.btnAddScale.move(80, 58)
        self.btnAddScale.setFixedWidth(70)
        self.btnAddScale.setFixedHeight(24)
        self.btnAddScale.setToolTip("Add Scale to selected cell.")
        self.btnAddScale.setText("Add Scale")
        self.btnAddScale.clicked.connect(lambda:self.addscale())


        """ Main Table """
        self.tm = QtGui.QTableWidget(self)
        self.tm.setGeometry(10, 90, 250, 150) # xy,wh
        self.tm.setWindowTitle("Broken Constraints")
        self.tm.setRowCount(0)
        self.tm.setColumnCount(2)
        self.tm.setMouseTracking(True)
        self.tm.setHorizontalHeaderLabels(["Property", 'Value']) 
        self.tm.horizontalHeader().sectionClicked.connect(self.fun)

    def addFilename(self):
        filepath = FreeCAD.ActiveDocument.FileName.rsplit("/", 1)
        # Check for file being saved
        if filepath[0] == '':
            mApp('The file has not been ssaved. Save the file and try again.')
            return()
        name = filepath[1]
        name = name.replace('.FCStd', '')
        self.addTexttoCell(name)
    
    def addscale(self):       
        #from fractions import Fraction
        sheet = FreeCAD.ActiveDocument.Template
        page = sheet.InList[0]
        scale = page.Scale        
        #s = Fraction.from_float(1/scale)
        self.addTexttoCell(str(scale))

    def addDate(self):
        from datetime import date
        today = str(date.today())
        self.addTexttoCell(today)

    def addTexttoCell(self, txt):
        rownum = self.tm.currentRow()
        p = QtGui.QTableWidgetItem(txt)
        self.tm.setItem(rownum, 1, p)

    def createdefaultprop(self):
        properties.createDefaultprops()
        #self.createPropertyobject()
    
    def copyfromdrawing(self):
        updateclass.copyFromTemplate()

    def fun(self, i):
        # click in column header to sort column
        self.tm.sortByColumn(i)

    def updateandsave(self):
        self.saveProperties()
        updateclass.updatedrawingtitle()

    def SaveClose(self):
        self.saveProperties()
        self.closeme()

    def addrow(self):
        rows = self.tm.rowCount()
        self.tm.insertRow(rows)

    def saveProperties(self):
        # Saves upon closing
        doc = FreeCAD.activeDocument()
        propobj = doc.getObject('Properties')
        if propobj is None:
            return()
        pl = []
        for e in propobj.PropertiesList:
            if e in 'ExpressionEngine, Label, Label2, Proxy, Visibility':
                pass
            else:
                pl.append(str(e))
        # Delete props from properties
        plist1 = []
        for w in pl:
            plist1.append(w)
        for word in plist1:
            propobj.removeProperty(word)
        # Refresh properties
        propobj = doc.getObject('Properties')
        pvalue = ''
        for row in range(0, self.tm.rowCount()):
            item0 = self.tm.item(row, 0)
            item1 = self.tm.item(row, 1)
            if item0 is None:
                continue
            prop = item0.text()
            if prop != '':
                if item1 is None:
                    pvalue = ''
                else:
                    pvalue = item1.text()
                propobj.addProperty("App::PropertyString",prop,"Prop")
                setattr(propobj, prop, pvalue)

    def clearTable(self):
        self.tm.setRowCount(0)

    def loadtable(self):
        self.tm.setRowCount(0)
        row = 0
        for prop in g.proplist:
            if prop is not None:
                self.tm.insertRow(0)
                p = QtGui.QTableWidgetItem(prop[0])
                prop1 = prop[1]
                if prop1 is None:
                    prop1 = ''
                print(prop1)
                v = QtGui.QTableWidgetItem(prop1)
                self.tm.setItem(0, 0, p)
                self.tm.setItem(0, 1, v)
                row = row+1
        header = self.tm.horizontalHeader()
        header.setResizeMode(QtGui.QHeaderView.ResizeToContents)
        for row in range(self.tm.rowCount()):
            self.tm.setRowHeight(row, 15)
    
    def ClearAll(self):
        form1.txtboxReport.setText('')
        FreeCADGui.Selection.clearSelection()


    def resizeEvent(self, event):
        # resize table
        formx = self.width()
        formy = self.height()
        self.tm.resize(formx - 20, formy - 100)

    def showme(self, msg):
        properties.openproperties()
       

    def closeme(self):
        self.close()

    def closeEvent(self, event):
        print('Shut down in closeEvent')

form1 = formMain('form1')

class updateclass:
    def __init__(self):
        pass

    def updatedrawingtitle(self):
        doc = FreeCAD.ActiveDocument
        propobj = doc.getObject('Properties')
        if propobj is None:
            mApp('There is no property object in this file.\nStart the properties program to create one.')
            return()
        page = doc.getObject('Page')
        if page is None:
            mApp('No drawing in this file\nCreate a drwing and try again)')
            return()
        # retrieve dictionay from drawing
        texts = page.Template.EditableTexts
        dictnames = texts.keys()
        pl = propobj.PropertiesList
        for e in pl:
            dictname = e #.replace('FC_', 'FC-') # Need to change underscore back to minus sign
            if dictname in dictnames:
                try:
                    texts[dictname] = getattr(propobj, e)
                except Exception as err:
                    mApp('Error ' + str(err))
        page.Template.EditableTexts = texts



    def copyFromTemplate(self):
        doc = FreeCAD.ActiveDocument
        propobj = doc.getObject('Properties')
        if propobj is None:
            mApp('There is no property object in this file.\nStart the properties program to create one.')
            return()
        page = doc.getObject('Page')
        if page is None:
            mApp('No drawing in this file\nCreate a drawing and try again)')
            return()
        pl = propobj.PropertiesList
        for e in pl:
            if hasattr(propobj,e):
                propobj.removeProperty(e)
        texts = page.Template.EditableTexts
        g.proplist = []
        for key, val in texts.items():
            try:
                propobj.addProperty("App::PropertyString",key , "Prop")
                setattr(propobj, key, val)
            except Exception as err:
                msg = ''
                if 'Invalid property name' in str(err):
                    msg = f'Invalid symbol in the name {key}.\nTo fix: open the drawing template in a text editor'
                    msg1 = f'\nSearch for {key} and replace the invalid symbol\nwith an under-score or rename the variable'
                    msg = msg + msg1
                else:
                    msg = 'Error ' + str(err)
                mApp(msg)
                return()
            g.proplist.append([key, val])
        g.propobj = propobj
        form1.loadtable()
        
updateclass = updateclass()





toolTipText = \
"""
Stores properties inside files. Properties can be added or deleted
except for FileName, FilePath, Ver and Description. 
If a property object is not in the file when it is 
first started it will create one for you.
"""

class FileProperties:
    def GetResources(self):
        mypath = os.path.dirname(__file__)
        return {
             'Pixmap': mypath + "/Icons/CD_FileProperties.svg",
             'MenuText': 'File Properties',
             'ToolTip': toolTipText
             }

    def Activated(self, placeholder = None):
        if FreeCAD.activeDocument() is None:
            mApp('No file is opened.You must open a file first.')
            return
        form1.showme('Properties opened.')

FreeCADGui.addCommand('FilePropertyTool', FileProperties())
#==============================================================================


class updateDrawingProp:
    def GetResources(self):
        mypath = os.path.dirname(__file__)
        return {
             'Pixmap': mypath + "/Icons/UpDateDrawing.svg",
             'MenuText': 'Update Drawing Title',
             'ToolTip': 'Update the title Properties'
             }

    def Activated(self, placeholder = None):
        if FreeCAD.activeDocument() is None:
            mApp('No file is opened.You must open a file first.')
            return
        updateclass.updatedrawingtitle()

FreeCADGui.addCommand('updateDrawingPropTool', updateDrawingProp())
#==============================================================================

class mApp(QtGui.QWidget):
    """This message box was added to make this file a standalone file"""
    # for error messages
    def __init__(self, msg, msgtype ='ok'):
        super().__init__()
        self.title = 'Warning'
        self.initUI(msg)

    def initUI(self, msg):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        QtGui.QMessageBox.question(self, 'Warning', msg, QtGui.QMessageBox.Ok|QtGui.QMessageBox.Ok)
        self.show()   
