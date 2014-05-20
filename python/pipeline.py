import os, nuke, nukescripts
import sys, re

# COMP UP
# Versions up C01 and A01 in filenames
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
def customWrite(folder = 'Comp', extension = 'dpx', relative = 1):

    #variables
    printf = '.%04d'
    project_dir = [route()['project_dir'], '[value project_directory]']
    filename = [route()['filename'], '[file rootname [file tail [value root.name]]]']

    w = nuke.nodes.Write()
    w.setInput(0, nuke.selectedNode())

    w['file_type'].setValue(extension)
    w['beforeRender'].setValue("pipeline.createWriteDir()")
    w['label'].setValue(folder.upper())
    w['file'].setValue(os.path.join(project_dir[relative], folder, filename[relative], filename[relative] + printf + '.' + extension))
    
    if nuke.env['LINUX']:
        if folder == 'Review':
            w['afterRender'].setValue('mrender.mconvert()')
            w['colorspace'].setValue('rec709')

    if extension == "mov":
        w['codec'].setValue('AVdn')
        w['writeTimeCode'].setValue('1')
        #1080p 36kbps
        w['settings'].setValue('000000000000000000000000000001d27365616e000000010000000100000000000001be76696465000000010000000f00000000000000227370746c0000000100000000000000004156646e000000000020000003ff000000207470726c000000010000000000000000000000000017f9db00000000000000246472617400000001000000000000000000000000000000530000010000000100000000156d70736f00000001000000000000000000000000186d66726100000001000000000000000000000000000000187073667200000001000000000000000000000000000000156266726100000001000000000000000000000000166d70657300000001000000000000000000000000002868617264000000010000000000000000000000000000000000000000000000000000000000000016656e647300000001000000000000000000000000001663666c67000000010000000000000000004400000018636d66720000000100000000000000004156494400000014636c757400000001000000000000000000000038636465630000000100000000000000004156494400000001000000020000000100000011000000030000000000000000000000000000001c766572730000000100000000000000000003001c00010000')
        w['file'].setValue(os.path.join(project_dir[relative], folder, filename[relative] + '.' + extension))
        w['colorspace'].setValue('rec709')
    elif extension == "exr":
        w['metadata'].setValue(2)
    elif extension == "dpx":
        w['transfer'].setValue('log')

def route():
    path = nuke.root().name()
    m = re.match('(.+)/(.+)/scripts/(.+).nk', path, re.IGNORECASE )

    r = { 'project_dir' : m.group(1), 'shot' : m.group(2), 'filename' : m.group(3) }

    return r 

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
# def filenameFix(filename):
# 	projects = { 'WIN32' : 'Z:/', 'MAXOS' : '/Volumes/Projects/', 'LINUX' : '/media/Projects/' }
# 	elements = { 'WIN32' : 'Y:/', 'MAXOS' : '/Volumes/Elements/', 'LINUX' : '/media/Elements/' }

# 	if nuke.env['WIN32']:
# 		filename = filename.replace( projects['MACOS'], projects['WIN32'] ).replace( projects['LINUX'], projects['WIN32'] ).replace( elements['MACOS'], elements['WIN32'] ).replace( elements['LINUX'], elements['WIN32'] )
# 	elif nuke.env['MACOS']:
# 		filename = filename.replace( projects['WIN32'], projects['MACOS'] ).replace( projects['LINUX'], projects['MACOS'] ).replace( elements['WIN32'], elements['MACOS'] ).replace( elements['LINUX'], elements['MACOS'] )
# 	elif nuke.env['LINUX']:
# 		filename = filename.replace( projects['WIN32'], projects['LINUX'] ).replace( projects['MACOS'], projects['LINUX'] ).replace( elements['WIN32'], elements['LINUX'] ).replace( elements['MACOS'], elements['LINUX'] )
# 	return filename

# nuke.addFilenameFilter(filenameFix)

