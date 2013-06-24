import os, nuke, nukescripts
import re, shlex, subprocess
import sys

# sendToAvconv

# @description: Send rendered image sequence to shell avconv call
# 	renderSlug
# 		false: the movie start frame = the nuke project start frame*
# 		true: the movie start frame = 0
#		*Note: Avconv image sequences always start at 0
# @url: http://www.richardgreenwood.ca/2012/05/send-to-ffmpeg-from-nuke-update/
# @usage: add sendToAvconv.sendToAvconv() to Write Node's afterRender callback

def sendToAvconv(codec = 'dnxhd'):
	# Configuration
	renderSlug = False
	vcodec = {
		'x264' : 'libx264 -pre baseline',
		'dnxhd' : 'dnxhd -b 36M',
	}
	extension = '.mov'

	# set some variables
	fps = nuke.root().knob('fps').value()
	firstFrame = nuke.root().knob('first_frame').value()
	ss = 0 if renderSlug == True else secondsToStr(firstFrame/fps)

	# grabs the write node's file value and makes sure the path uses printf style filenames
	imgSeqPath = nukescripts.replaceHashes(nuke.filename(nuke.thisNode()))

	# generate mov path
	base, ext = os.path.splitext(os.path.basename(imgSeqPath))
	movPath =  os.path.dirname(os.path.dirname(imgSeqPath)) + '/' + re.sub('\.?%0\d+d$', '', base) + extension

	# make shell command
	enc = 'avconv -y -r %s -i \'%s\' -s \'hd1080\' -an -ss %s -vcodec %s -threads 0 \'%s\'' % (fps, imgSeqPath, ss, vcodec[codec], movPath)
	#print enc
	subprocess.Popen(shlex.split(enc), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# returns HH:MM:SS.SSS formatted string
# http://code.activestate.com/recipes/511486/
def secondsToStr(t):
	rediv = lambda ll,b : list(divmod(ll[0],b)) + ll[1:]
	return "%02d:%02d:%02d.%03d" % tuple(reduce(rediv,[[t*1000,],1000,60,60]))
