import os, nuke, nukescripts
import sys, re

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

# Define function
def customWrite(folder = 'Comp', extension = 'exr', relative = 1):

	#variables
	printf = '.%04d'
	destination = '/media/Projects'
	shot = [route()['shot'],'[file tail [file dirname [file dirname [value root.name]]]]']
	filename = [route()['filename'], '[file rootname [file tail [value root.name]]]']

	w = nuke.nodes.Write()
	w.setInput(0, nuke.selectedNode())

	w["file_type"].setValue(extension)
	w["beforeRender"].setValue("pipeline.createWriteDir()")
	w["label"].setValue(folder.upper())
	w["file"].setValue('[value project_directory]' + folder + '/'+ filename[relative] + '/'+ filename[relative] + printf + '.' + extension)
	w["colorspace"].setValue('rec709')

	if extension == "mov":
		w["codec"].setValue('AVdn')
		w["writeTimeCode"].setValue('1')
		w["settings"].setValue('000000000000000000000000000001d27365616e000000010000000100000000000001be76696465000000010000000f00000000000000227370746c0000000100000000000000004156646e000000000020000003ff000000207470726c000000010000000000000000000000000017f9db00000000000000246472617400000001000000000000000000000000000000530000010000000100000000156d70736f00000001000000000000000000000000186d66726100000001000000000000000000000000000000187073667200000001000000000000000000000000000000156266726100000001000000000000000000000000166d70657300000001000000000000000000000000002868617264000000010000000000000000000000000000000000000000000000000000000000000016656e647300000001000000000000000000000000001663666c67000000010000000000000000004400000018636d66720000000100000000000000004156494400000014636c757400000001000000000000000000000038636465630000000100000000000000004156494400000001000000020000000100000011000000030000000000000000000000000000001c766572730000000100000000000000000003001c00010000')
		w["file"].setValue('[value project_directory]' + folder + '/'+ filename[relative] + '.' + extension)
	elif extension == "exr":
		w["metadata"].setValue(2)

def route():
	path = nuke.root().name()
	p = re.compile('.*?/Arctic_Air_3/shots/(.*?)/(.*?)/Scripts/(.*?).nk')
	m  = p.match (path)

	r = { 'episode' : m.group(1), 'shot' : m.group(2), 'filename' : m.group(3) }

	return r 


# # Define function
# def customWriteOLD(server = 'file', folder = 'Comp', extension = 'exr', relative = 1):

# 	#variables
# 	printf = '.%04d'
# 	destination = { 'file' : '/media/Projects', 'review' : '/media/Review' }
# 	project = 'Arctic_Air_3'
# 	shot = [route()['shot'],'[file tail [file dirname [file dirname [value root.name]]]]']
# 	episode = [route()['episode'], route()['episode']]
# 	filename = [route()['filename'], '[file rootname [file tail [value root.name]]]']

# 	shotpath = destination[server] + '/' + project + '/shots/' + episode[relative] + '/' + shot[relative]

# 	c = nuke.selectedNode()
# 	# We use the command below instead of w = nuke.createNode("Write") so that the user tab doesn't steal the focus
# 	w = nuke.nodes.Write()
# 	w.setInput(0, c)

# 	# add new knobs
# 	# k = nuke.String_Knob("shotpath", "Shot Path")
# 	# w.addKnob(k)
# 	# k = nuke.String_Knob("filename", "Filename")
# 	# w.addKnob(k)

# 	#set knob values
# 	# w["shotpath"].setValue(shotpath)
# 	# w["filename"].setValue(filename[relative]) 
# 	w["file_type"].setValue(extension)
# 	w["beforeRender"].setValue("pipeline.createWriteDir()")
# 	w["label"].setValue(server.upper())
# 	w["metadata"].setValue(2)

# 	# MOV
# 	if extension == "mov":
# 		w["colorspace"].setValue('rec709')
# 		w["codec"].setValue('AVdn')
# 		w["writeTimeCode"].setValue('1')
# 		w["settings"].setValue('000000000000000000000000000001d27365616e000000010000000100000000000001be76696465000000010000000f00000000000000227370746c0000000100000000000000004156646e000000000020000003ff000000207470726c000000010000000000000000000000000017f9db00000000000000246472617400000001000000000000000000000000000000530000010000000100000000156d70736f00000001000000000000000000000000186d66726100000001000000000000000000000000000000187073667200000001000000000000000000000000000000156266726100000001000000000000000000000000166d70657300000001000000000000000000000000002868617264000000010000000000000000000000000000000000000000000000000000000000000016656e647300000001000000000000000000000000001663666c67000000010000000000000000004400000018636d66720000000100000000000000004156494400000014636c757400000001000000000000000000000038636465630000000100000000000000004156494400000001000000020000000100000011000000030000000000000000000000000000001c766572730000000100000000000000000003001c00010000')

# 		# w["file"].setValue('[value shotpath]' + '/' + folder + '/[value filename]' + '.' + extension)
# 		w["file"].setValue(shotpath + '/' + folder + '/'+ filename[relative] + '.' + extension)
# 	else:
# 		# w["file"].setValue('[value shotpath]' + '/' + folder + '/[value filename]/[value filename]' + printf + '.' + extension)
# 		w["file"].setValue(shotpath + '/' + folder + '/'+ filename[relative] + '/'+ filename[relative] + printf + '.' + extension)


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
def filenameFix(filename):
	if nuke.env['WIN32']:
		filename = filename.replace( "/Volumes/Projects/", "Z:/" ).replace("/media/Projects/", "Z:/").replace( "/Volumes/Elements/", "Y:/" ).replace("/media/Elements/", "Y:/").replace( "/Volumes/Review/", "X:/" ).replace("/media/Review/", "X:/")
	elif nuke.env['MACOS']:
		filename = filename.replace( "Z:/", "/Volumes/Projects/" ).replace( "/media/Projects/", "/Volumes/Projects/" ).replace( "X:/", "/Volumes/Review/" ).replace( "/media/Review/", "/Volumes/Review/" ).replace( "Y:/", "/Volumes/Elements/" ).replace( "/media/Elements/", "/Volumes/Elements/" )
	elif nuke.env['LINUX']:
		filename = filename.replace("Z:/", "/media/Projects/").replace("/Volumes/Projects/", "/media/Projects/").replace("X:/", "/media/Review/").replace("/Volumes/Review/", "/media/Review/").replace("Y:/", "/media/Elements/").replace("/Volumes/Elements/", "/media/Elements/")
	return filename

nuke.addFilenameFilter(filenameFix)
	
# ADD FAVOURITE DIR
project = 'Arctic_Air_3'
vol = ''
if nuke.env['LINUX']:
	vol = '/media/Projects/'
	vol2 = '/media/Elements/'
	vol3 = '/media/Projects/Arctic_Air_3/editorial/from_vfx/'
elif nuke.env['MACOS']:
	vol = '/Volumes/Projects/'
	vol2 = '/Volumes/Elements/'
	vol3 = '/Volumes/Projects/Arctic_Air_3/editorial/from_vfx/'
elif nuke.env['WIN32']:
	vol = 'Z:/'
	vol2 = 'Y:/'
	vol3 = 'Z:/Projects/Arctic_Air_3/editorial/from_vfx/'

nuke.addFavoriteDir('Project', vol)
nuke.addFavoriteDir('Shots', vol + project + '/shots/')
nuke.addFavoriteDir('Assets', vol + project + '/assets/')
nuke.addFavoriteDir('Elements', vol2)
nuke.addFavoriteDir('Editorial', vol3)

