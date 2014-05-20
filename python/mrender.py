"""
.. module:: mrender
	:synopsis: Send rendered image sequence to shell avconv call
	:url: http://www.richardgreenwood.ca/2012/05/send-to-ffmpeg-from-nuke-update/

.. moduleauthor:: Richard Greenwood <mail@richardgreenwood.ca>
"""
import os, nuke, nukescripts
import re, shlex, subprocess

def mconvert(codec = 'dnxhd', converter = 'avconv'):
	"""Send rendered image sequence to shell avconv call
	
	Args:
		codec (str, optional): dictionary name for codec string. Either 'dnxhd' (default) or 'x264'.
		converter (str, optional): dictionary name for commandline converter. Either 'avconv' (default) or 'ffmpeg'

	Returns:
		subprocess call

	add import mrender to init.py
	add mrender.mconvert() to a Write Node's afterRender callback
	"""

	# Configuration

	# Set defaults - must match program and vcodec dictionary keys
	programDefault = 'avconv' # 'ffmpeg'
	vcodecDefault = 'dnxhd' # 'x264'

	# Set vcodec command line flags
	vcodecOpt_x264 = 'libx264 -pre baseline'
	vcodecOpt_dnxhd = 'dnxhd -b 36M'

	# Output movie file extension
	extension = '.mov'

	# Show terminal output
	useXTerm = 1

	#end config

	# http://stackoverflow.com/a/103081
	program = { 'avconv' : 'avconv', 'ffmpeg' : 'ffmpeg' }.get(converter, programDefault)
	vcodec = { 'x264' : vcodecOpt_x264, 'dnxhd' : vcodecOpt_dnxhd }.get(codec, vcodecDefault)

	# grab Nuke file variables
	fps = nuke.root().knob('fps').value()
	firstFrame = nuke.root().knob('first_frame').value()

	# grabs the write node's file value and makes sure the path uses printf style filenames
	imgSeqPath = nukescripts.replaceHashes(nuke.filename(nuke.thisNode()))

	# generate mov path
	base, ext = os.path.splitext(os.path.basename(imgSeqPath))
	movPath = os.path.dirname(os.path.join(os.path.dirname(imgSeqPath), re.sub('\.?%0\d+d$', '', base))) + extension

	# make shell command
	cmd = program + ' -y -r %s -start_number %s -i \'%s\' -s \'hd1080\' -an -vcodec %s -threads 0 \'%s\'' % (fps, firstFrame, imgSeqPath, vcodec, movPath)
	enc = [ cmd, 'xterm -hold -e ' + cmd ]
	subprocess.Popen(shlex.split(enc[useXTerm]), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
