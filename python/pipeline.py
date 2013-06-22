import os, nuke, nukescripts
import sys

# COMP UP
# Versions up c01 and a01 in filenames
# ////////////////////////////////////////////////////////////////////////////////

def script_comp_version_up():
	"""Adds 1 to the _c## at the end of the script name and saves a new version."""
	root_name = nuke.toNode("root").name()
	(prefix, v) = nukescripts.version_get(root_name, "c")
	if v is None: return

	v = int(v)
	nuke.scriptSaveAs(nukescripts.version_set(root_name, prefix, v, v + 1))

def script_anim_version_up():
	"""Adds 1 to the _a## at the end of the script name and saves a new version."""
	root_name = nuke.toNode("root").name()
	(prefix, v) = nukescripts.version_get(root_name, "a")
	if v is None: return

	v = int(v)
	nuke.scriptSaveAs(nukescripts.version_set(root_name, prefix, v, v + 1))

# WRITE NODES
# ////////////////////////////////////////////////////////////////////////////////

# Variable declaration
shotDir = '[file dirname [value root.name]]/../'
if nuke.env['WIN32']:
	reviewDir = "Y:/"
	editorialDir = "Z:/Projects/Arctic_Air_2/editorial/from_vfx/"
elif nuke.env['MACOS']:
	reviewDir = "/Volumes/Wilde/"
	editorialDir = "/Volumes/Projects/Arctic_Air_2/editorial/from_vfx/"
elif nuke.env['LINUX']:
	reviewDir = "/media/Wilde/"
	editorialDir = "media/Projects/Arctic_Air_2/editorial/from_vfx/"
episodeName = '[file tail [file dirname [file dirname [file dirname [value root.name]]]]]'
shotName = '[file tail [file dirname [file dirname [value root.name]]]]'
parentDir = '[file rootname [file tail [value root.name]]]'
filename = '[file rootname [file tail [value root.name]]]'
printf = '.%04d'

# Define function
def customWrite(extension = 'exr', destination = 'server'):
	w = nuke.createNode("Write")
	w.knob("name").setValue('Write_' + extension.upper() + '_' + destination.upper())
	w.knob("file_type").setValue(extension)
	w.knob("beforeRender").setValue("pipeline.createWriteDir()")
	# EXR
	if extension == "exr":
		if destination == "review":
			w.knob("file").setValue(reviewDir + 'shots/' + episodeName + '/' + shotName + '/Comp/' + parentDir + '/' + filename + printf + '.' + 'exr')
		elif destination == "editorial":
			w.knob("file").setValue(editorialDir + 'Planes/'  + shotName + '/EXR/' + parentDir + '/' + filename + printf + '.' + 'exr')
			w.knob("channels").setValue("rgba")
		else:
			w.knob("file").setValue(shotDir + 'Comp/' + parentDir + '/' + filename + printf + '.' + extension)
		w.knob("compression").setValue("0")
		w.knob("colorspace").setValue("rec709")
	#DPX
	if extension == "dpx":
		if destination == "review":
			w.knob("file").setValue(reviewDir + 'shots/' + episodeName + '/' + shotName + '/Comp/' + parentDir + '/' + filename + printf + '.' + 'dpx')
		elif destination == "editorial":
			w.knob("file").setValue(editorialDir + 'Planes/'  + shotName + '/EXR/' + parentDir + '/' + filename + printf + '.' + 'dpx')
			w.knob("channels").setValue("rgba")
		else:
			w.knob("file").setValue(shotDir + 'Comp/' + parentDir + '/' + filename + printf + '.' + extension)
	# PNG
	elif extension == "png":
		if destination == "editorial":
			w.knob("file").setValue(editorialDir + 'Planes/' + shotName + '/PNG/' + parentDir + '/' + filename + printf + '.' + 'png')
		else:
			w.knob("file").setValue(shotDir + 'Review/' + parentDir + '/' + filename + printf + '.' + extension)
		w.knob("colorspace").setValue("rec709")
		w.knob("channels").setValue("rgba")
	# MOV
	elif extension == "mov":
		w.knob("file").setValue(shotDir + 'Review/' + '/' + filename + printf + '.' + extension)
		w.knob("codec").setValue("avc1")
		w.knob("quality").setValue("High")


# PATHS
# ////////////////////////////////////////////////////////////////////////////////

# CREATE DIR
# Make directory on Save if they don't exist
def createWriteDir():
	file = nuke.filename(nuke.thisNode())
	dir = os.path.dirname( file )
	osdir = nuke.callbacks.filenameFilter( dir )
	try:
		os.makedirs(osdir)
	except OSError:
		pass

# FILENAME FIX
# Arctic Air

#def filenameFix(filename):
#	if nuke.env['WIN32']:
#		filename = filename.replace( "/Volumes/Projects/", "Z:/" ).replace("/media/Projects/", "Z:/").replace( "/Volumes/Wilde/", "Y:/" ).replace("/media/Wilde/", "Y:/").replace( "/Volumes/Elements/", "X:/" ).replace("/media/Elements/", "X:/")
#	elif nuke.env['MACOS']:
#		filename = filename.replace( "Z:/", "/Volumes/Projects/" ).replace( "/media/Projects/", "/Volumes/Projects/" ).replace( "Y:/", "/Volumes/Wilde/" ).replace( "/media/Wilde/", "/Volumes/Wilde/" ).replace( "X:/", "/Volumes/Elements/" ).replace( "/media/Elements/", "/Volumes/Elements/" )
#	elif nuke.env['LINUX']:
#		filename = filename.replace("Z:/", "/media/Projects/").replace("/Volumes/Projects/", "/media/Projects/").replace("Y:/", "/media/Wilde/").replace("/Volumes/Wilde/", "/media/Wilde/").replace("X:/", "/media/Elements/").replace("/Volumes/Elements/", "/media/Elements/")
#	return filename

# ADD FAVOURITE DIR
# Arctic Air

#project = 'Arctic_Air_2'
#vol = ''
#if nuke.env['LINUX']:
#	vol = '/media/Projects/'
#	vol2 = '/media/Elements/'
#	vol3 = '/media/Projects/Arctic_Air_2/editorial/from_vfx/'
#elif nuke.env['MACOS']:
#	vol = '/Volumes/Projects/'
#	vol2 = '/Volumes/Elements/'
#	vol3 = '/Volumes/Projects/Arctic_Air_2/editorial/from_vfx/'
#elif nuke.env['WIN32']:
#	vol = 'Z:/'
#	vol2 = 'X:/'
#	vol3 = 'Z:/Projects/Arctic_Air_2/editorial/from_vfx/'

#nuke.addFavoriteDir('Project', vol)
#nuke.addFavoriteDir('Shots', vol + project + '/shots/')
#nuke.addFavoriteDir('Assets', vol + project + '/assets/')
#nuke.addFavoriteDir('Elements', vol2)
#nuke.addFavoriteDir('Editorial', vol3)

