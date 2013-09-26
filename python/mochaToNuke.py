####################################################################################################
#
#mochaToNuke v1.1
#By:Hiroshi Iwamoto
#
#example line in menu.py
#
#import mochaToNuke
#toolbar = nuke.toolbar("Nodes")
#toolbar.addCommand('Mocha To Nuke', 'mochaToNuke.mochaToNuke()')
####################################################################################################


import nuke
import nukescripts


def mochaToNuke():

	p = nuke.Panel( "Select track data or paste track data" )
	p.addSingleLineInput( "Start Frame:", 1 )
	p.addFilenameSearch("Mocha text data:", '')
	p.addMultilineTextInput("Paste track data:", '')
	result = p.show()
	frameOffset = p.value("Start Frame:")
	mochaTrackFile = p.value("Mocha text data:")
	mochaTrackData = p.value("Paste track data:")
	if mochaTrackFile:
		#open txt file
		f = open( mochaTrackFile )
		#read txt file
		mochaData = f.read()
		#close txt file
		f.close()
	if mochaTrackData:
		mochaData = mochaTrackData
	
	if mochaTrackFile or mochaTrackData:
		
		#delete footer
		list1 = mochaData.split('\nEnd of Keyframe Data\n')[0]

    		#split tracker data    
    		list2 = list1.split('Effects\tADBE Corner Pin #1\tADBE Corner Pin-')

    		#get header
    		header = list2[0]

    		#get line including source height 
    		heightLine = header.split('\n')[4] 
    
    		#get source Height and convert to float
    		sourceHeight = float(heightLine.split('\t')[2])

    		#delete header
    		del list2[0]

		#move to start frame
		nuke.frame(float(frameOffset))
		
		

		myTrack = nuke.createNode('Tracker4')
	
		trackCount = len(list2)
		for n in range(trackCount):
			myTrack['add_track'].execute()
			t = myTrack['tracks']
			NumColumns = 31
	
			TrackXColumnIndex = 2
			TrackYColumnIndex = 3
	
			dataNum = n+1
	
			track = list2[n]
			track = track.replace('\n', '')
			trackdata = track.split('\t')
	
			#delete empty object
			while '' in trackdata: trackdata.remove('')
			trackNumber = int(trackdata[0])
			del trackdata[:4] #delete Header
	
			#get start and end frame
			startFrame = int(trackdata[0])
			endFrame = int(trackdata[-3])
	
			#get trackdata
			trackBodyXdata = trackdata[1::3]
			trackBodyYdata = trackdata[2::3]
			#convert to float
			trackBodyX = [float(i) for i in trackBodyXdata]
			trackBodyY = [float(i) for i in trackBodyYdata]
	
			#convert AE Y Axis to Nuke Y Axis
			trackBodyY =  [sourceHeight-y for y in trackBodyY]
	
			for time in range(startFrame,endFrame+1):
				#x, y set value into teh cell
				TrackIdx = n
				t.setValueAt( trackBodyX[time], time + int(frameOffset), NumColumns * TrackIdx + TrackXColumnIndex )
				t.setValueAt( trackBodyY[time], time + int(frameOffset), NumColumns * TrackIdx + TrackYColumnIndex )
				
			t.setValueAt( 1, time + int(frameOffset), NumColumns * TrackIdx + 6 ) #Transform On
			t.setValueAt( 1, time + int(frameOffset), NumColumns * TrackIdx + 7 ) #Rotation On
			t.setValueAt( 1, time + int(frameOffset), NumColumns * TrackIdx + 8 ) #Scale on

