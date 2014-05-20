# @title saveFirstComp
# @description Prompts the user to nuke save path based on read node
# @author Richard Greenwood
# @version 1.1
# @compatible Nuke8
# @url www.richardgreenwood.ca

import nuke, nukescripts, re, os

if nuke.env["gui"]:
	class saveFirstComp ( nukescripts.PythonPanel ):
		def __init__( self, node ):

			#create dialogue box
			nukescripts.PythonPanel.__init__( self, "Save First Comp" )
			self.readNode = node

			#Set variables
			self.initials = os.getenv('ARTIST', 'IH').upper()
			self.path = self.readNode['file'].value()
			self.parent_dir = route(self.path)['parent_dir']
			self.shot = route(self.path)['shot']
			self.script_dir = os.path.join (self.parent_dir, self.shot, 'Scripts')
			self.filename = self.shot+'_C01_'+self.initials+'.nk'

			self.newPath = os.path.join( self.script_dir, self.filename)

			#define knobs
			self.artist = nuke.String_Knob ( "artist", "Your Initials" )
			#add knobs
			self.addKnob ( self.artist )
			#populate knobs
			self.artist.setValue( self.initials )

		#shows as modal dialogue (adds 'ok' and 'cancel' buttons)
		def showPanel( self ):
			result = nukescripts.PythonPanel.showModalDialog( self )
			if result:
				if nuke.ask('Save to %s' % self.newPath):
					if os.path.isdir(self.script_dir):
						nuke.scriptSaveAs( self.newPath )
					else:
						try:
							os.makedirs(self.script_dir)
						except OSError:
							nuke.message('Error making parent directory. Try making the Scripts directory manually.')
						nuke.scriptSaveAs( self.newPath )

# Returns saveFirstComp dialogue
def callPanel():
	node = nuke.selectedNode()
	if node.Class() == 'Read':
		return saveFirstComp(node).showPanel()
	else:
		nuke.tprint("Selected node must be a Read node.")
		nuke.message("Selected node must be a Read node.")

def route(path):
	m = re.match('(.*)/(.*)/plates', path, re.IGNORECASE )

	# return project directory
	r = { 'parent_dir' : m.group(1), 'shot' : m.group(2) } 

	return r 