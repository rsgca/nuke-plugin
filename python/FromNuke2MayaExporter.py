#############################################################################################################
#  FromNuke2MayaExporter V1.0 - Date: 17.10.2010 - Created by Jan Oberhauser - jan.oberhauser@gmail.com     #
#  Exports Cameras as fm2n-File to import into Maya                                                         #
#  Check for a updateted Version at http://janoberhauser.gute-filme-enden-nie.de                            #
#############################################################################################################

import os
import sys
import nuke
import nukescripts

def exportData(object, channels, startF, endF, exportFile):
	channalsAnimated = []
	channalsNotAnimated = []
	
	objectNameWrite = object.name()
	objectNodeTypeWrite = 'camera'

	for channel in channels:
		channelSplit = channels[channel].split(':')
		channelName = channelSplit[0]
		if len(channelSplit) == 1:
			channelIndex = 0
		else:
			channelIndex = channelSplit[1]
			 
		isAnimated = object[channelName].isAnimated()
		
		if isAnimated == True:
			channalsAnimated.append(channel)
		else:
			channalsNotAnimated.append(channel)
	
	writeOut = objectNameWrite + '\t'  + objectNodeTypeWrite + '\t\n'
		
	rotateOrders = {'0':'XYZ', '3':'YZX', '4':'ZXY', '1':'XZY', '2':'YXZ', '5':'ZYX'}	
	for channel in channalsNotAnimated:
		channelSplit = channels[channel].split(':')
		channelName = channelSplit[0]
		
		if len(channelSplit) == 1:
			thisValue = object[channelName].getValue()
		else: 
			thisValue = object[channelName].getValue(int(channelSplit[1]))		
		
		if channelName == 'rot_order':
			thisValue = int(thisValue)
			thisValue = rotateOrders[str(thisValue)]

		writeOut += channel + '\t' + str(thisValue) + '\n'
	
	writeOut += '+++++Animated+++++\n'

	if len(channalsAnimated) > 0:
		writeOut += 'Frame'
		for channel in channalsAnimated:
			writeOut += '\t' + channel
		writeOut += '\n'
			
		for i in range(int(startF), int(endF)+1):
			writeOut += str(i)
			for channel in channalsAnimated:
				channelSplit = channels[channel].split(':')
				channelName = channelSplit[0]
				
				if len(channelSplit) == 1:
					thisValue = object[channelName].getValueAt(i)
				else: 
					thisValue = object[channelName].getValueAt(i, int(channelSplit[1]))			
			
				writeOut += '\t' + str(thisValue)

			writeOut += '\n'
	
	f = open(exportFile, 'w')
	f.write(writeOut)
	f.close()	

	
def FromNuke2MayaExporter():
	allSelectedNodes = nuke.selectedNodes()
	
	firstFrame = nuke.root().knob('first_frame').getValue()
	lastFrame = nuke.root().knob('last_frame').getValue()
	
	if len(allSelectedNodes) == 1:
		selectedNode = allSelectedNodes[0]
		selectedNodeType = selectedNode.Class()
		
		channelMatch = {'transform.tx':'translate:0', 'transform.ty':'translate:1', 'transform.tz':'translate:2', 'transform.rx':'rotate:0', 'transform.ry':'rotate:1', 'transform.rz':'rotate:2', 'transform.sx':'scaling:0', 'transform.sy':'scaling:1', 'transform.sz':'scaling:2', 'transform.rotateOrder':'rot_order', 'camera.fl':'focal', 'camera.horizontalFilmAperture':'haperture', 'camera.verticalFilmAperture':'vaperture'}
		objectTypeOk = ['Camera', 'Camera2']
		
		cameraName = selectedNode.name()
		
		if selectedNodeType in objectTypeOk:
			
			exportPath = os.environ["HOME"].replace('\\', '/') + '/Desktop/'
			
			a = nukescripts.PythonPanel('File to Export')
			a.addKnob(nuke.Int_Knob('Start-Frame:'))
			a.knobs()['Start-Frame:'].setValue(int(firstFrame))
			a.addKnob(nuke.Int_Knob('End-Frame:'))
			a.knobs()['End-Frame:'].setValue(int(lastFrame))
			a.addKnob(nuke.File_Knob('Export-File:'))
			a.knobs()['Export-File:'].setValue(exportPath+cameraName + '.fm2n')
			finishedDialog = a.showModalDialog()
			
			startFrame = int(a.knobs()['Start-Frame:'].getValue())
			lastFrame = int(a.knobs()['End-Frame:'].getValue())
			filename = a.knobs()['Export-File:'].getValue()
			
			filename = filename.replace('\\', '/')
			
			filenameParts = filename.split('.')
			if filenameParts[len(filenameParts)-1] != 'fm2n':
				filename = filename + ".fm2n"
			
			exportData(selectedNode, channelMatch, firstFrame, lastFrame, filename)	
		else:
			nuke.message("ERROR: The Node you have selected is not a Camera.")
	
	else:
		nuke.message("ERROR: You have more then one Node selected")