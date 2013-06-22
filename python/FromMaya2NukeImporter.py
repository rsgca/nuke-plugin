#############################################################################################################
#  FromMaya2NukeImporter V1.2 - Date: 19.10.2010 - Created by Jan Oberhauser - jan.oberhauser@gmail.com     #
#  Imports Cameras, Lights & Locators which has been exported with FromMaya2Nuke into Nuke                  #
#  Check for a updateted Version at http://janoberhauser.gute-filme-enden-nie.de                            #
#############################################################################################################

#Imports the necessary stuff
import os
import sys
import nuke
import nukescripts

def importData(importFile, channelMatch, objectName):
	file = open(importFile, 'r')
	
	line = file.readline()
	
	values = line.split('\t')
	objectNodeType = values[1]
	if objectNodeType != 'camera' and objectNodeType != 'locator':
		if 'light_type' in objectName.knobs():
			objectName['light_type'].setValue (objectNodeType)
	
	line = file.readline()
	while line[:18] != '+++++Animated+++++':
		values = line.split('\t')
		
		destinationChannel = channelMatch[values[0]].split(':')
		
		objectName[destinationChannel[0]].clearAnimated()
		if destinationChannel[0] == 'rot_order':
			objectName[destinationChannel[0]].setValue(values[1])
		elif len(destinationChannel) == 2:
			objectName[destinationChannel[0]].setValue(float(values[1]), int(destinationChannel[1]))
		else:
			objectName[destinationChannel[0]].setValue(float(values[1]))
		
		line = file.readline()
		
	line = file.readline()

	destinationChannels = line.split('\t')
	destinationChannels[len(destinationChannels)-1] = destinationChannels[len(destinationChannels)-1].replace('\n', '')
	
	row = 0
	for channel in destinationChannels:
		if row > 0:
			destinationChannel = channelMatch[channel].split(':')			
			if len(destinationChannel) == 1:
				objectName[destinationChannel[0]].clearAnimated()
				objectName[destinationChannel[0]].setAnimated()
			else:
				objectName[destinationChannel[0]].clearAnimated(int(destinationChannel[1]))
				objectName[destinationChannel[0]].setAnimated(int(destinationChannel[1]))
				
		row += 1
	
	line = file.readline()
	while True:
		values = line.split('\t')
	
		row = 0
		for value in values:
			if row == 0:
				timevalue = value
			else:
				destinationChannel = channelMatch[destinationChannels[row]].split(':')
				
				if len(destinationChannel) == 2:
					objectName[destinationChannel[0]].setValueAt(float(value), int(timevalue), int(destinationChannel[1]))
				else:
					objectName[destinationChannel[0]].setValueAt(float(value), int(timevalue))
			
			row += 1
		
		line = file.readline()
		if line == '':
			file.close()
			break



def FromMaya2NukeImporter():
	importFile = True
	allSelectedNodes = nuke.selectedNodes()
	
	if len(allSelectedNodes) > 1:
		nuke.message("ERROR: You have more then one Node selected")
	else:
		a = nukescripts.PythonPanel('Choose File to import')
		a.addKnob(nuke.File_Knob('Import-File:'))
		finishedDialog = a.showModalDialog()
		
		if finishedDialog == True:
			filename = a.knobs()['Import-File:'].getValue()
			
			filenameParts = filename.split('.')
			if filenameParts[len(filenameParts)-1] != 'fm2n':
				nuke.message("ERROR: You have not selected a 'fm2n'-File. Please select a valid File!'")
				importFile = False

			file = open(filename, 'r')
			line = file.readline()
			file.close()
			
			values = line.split('\t')
	 
			objectName = values[0]
			objectNodeType = values[1]
			
			lightTypes = ['point', 'spot', 'directional']
			
			if objectNodeType == 'camera':
				channelMatch = {'transform.tx':'translate:0', 'transform.ty':'translate:1', 'transform.tz':'translate:2', 'transform.rx':'rotate:0', 'transform.ry':'rotate:1', 'transform.rz':'rotate:2', 'transform.sx':'scaling:0', 'transform.sy':'scaling:1', 'transform.sz':'scaling:2', 'transform.rotateOrder':'rot_order', 'camera.fl':'focal', 'camera.horizontalFilmAperture':'haperture', 'camera.verticalFilmAperture':'vaperture'}
			elif objectNodeType == 'locator':
				channelMatch = {'transform.tx':'translate:0', 'transform.ty':'translate:1', 'transform.tz':'translate:2', 'transform.rx':'rotate:0', 'transform.ry':'rotate:1', 'transform.rz':'rotate:2', 'transform.sx':'scaling:0', 'transform.sy':'scaling:1', 'transform.sz':'scaling:2', 'transform.rotateOrder':'rot_order'}
			elif objectNodeType in lightTypes:
				channelMatch = {'transform.tx':'translate:0', 'transform.ty':'translate:1', 'transform.tz':'translate:2', 'transform.rx':'rotate:0', 'transform.ry':'rotate:1', 'transform.rz':'rotate:2', 'transform.sx':'scaling:0', 'transform.sy':'scaling:1', 'transform.sz':'scaling:2', 'transform.rotateOrder':'rot_order', 'transform.intensity':'intensity', 'transform.cr':'color:0', 'transform.cg':'color:1', 'transform.cb':'color:2', 'transform.coneAngle':'cone_angle', 'transform.penumbraAngle':'cone_penumbra_angle', 'transform.dropoff':'cone_falloff'}
			else:
				nuke.message("ERROR: The Object-Type is not supported. Please make sure that you have selected the right File and it contains either Camera- or Light-Data!")
				importFile = False
			
			if len(allSelectedNodes) == 1:
				objectName = allSelectedNodes[0].knob('name').value()
				objectTypeGoal = allSelectedNodes[0].Class()
				
				thisNode = allSelectedNodes[0]
 
				if objectNodeType == 'spot':
					objectTypeOk = ['Spotlight', 'Light2']
				elif objectNodeType == 'point':
					objectTypeOk = ['Light', 'Light2']
				elif objectNodeType == 'directional':
					objectTypeOk = ['DirectLight', 'Light2']
				elif objectNodeType == 'camera':
					objectTypeOk = ['Camera', 'Camera2']			
				elif objectNodeType == 'locator':
					objectTypeOk = ['Axis', 'Axis2', 'TransformGeo', 'Card' , 'Card2', 'Cube', 'Cylinder', 'Sphere', 'ReadGeo', 'ReadGeo2', 'Light', 'Light2', 'Spotlight', 'DirectLight', 'Camera', 'Camera2']
									
				if objectTypeGoal not in objectTypeOk:
					nuke.message("ERROR: The File contains data for a " + objectNodeType + " but there is a " + objectTypeGoal + " selected. Please select the right node!")
					importFile = False
				
			else:
				if objectNodeType == 'camera':
					thisNode = nuke.nodes.Camera(name=objectName)
				elif objectNodeType == 'locator':
					thisNode = nuke.nodes.Axis2(name=objectName)
				else:
					thisNode = nuke.nodes.Light2(name=objectName)

			if importFile == True:
				importData(filename, channelMatch, thisNode)