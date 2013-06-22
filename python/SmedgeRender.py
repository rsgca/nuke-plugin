# SmedgeRender.py
#
# Smedge integration with Nuke
#
# Smedge
# Copyright (c) 2004 - 2011 Uberware. All Rights Reserved 
# @URL http://www.uberware.net/download/SmedgeRender.py
# @edits by Richard Greenwood

# import required modules
import os, platform, random, nuke, shlex, subprocess

# Path to the Submit executable
# Adjust this path to the correct executable path for your system. 
# On Windows, you must include the .exe extension
if platform.system() in ("Windows", "Microsoft"):
  SUBMIT_PATH = "C:\Program Files (x86)\Smedge\Submit.exe"
elif platform.system() in ("Linux"):
  SUBMIT_PATH = "/opt/Smedge2012.2_x64/Submit"
else:
  SUBMIT_PATH = "/Applications/Smedge.app/Contents/MacOS/Submit"


# define the main entry point
def SmedgeRender():
  sr = SmedgeRenderJob()
  

# define the class
class SmedgeRenderJob (object):

    # create the window
    def __init__(self):
        # basic variables used by the script
        self.nukeScriptPath = nuke.Root().name()
        self.nukeFromFrame = nuke.Root().firstFrame()
        self.nukeToFrame = nuke.Root().lastFrame()

        # determine if there are selected write nodes
        try:
            if nuke.selectedNode().Class()!='Write' or nuke.selectedNode().knob("disable").value() == True :
                raise StandardError
            self.nukeSelectedNode=nuke.selectedNode().name()
        except:
             self.nukeSelectedNode=""

        # get the executable path
        self.submitExecutablePath = '\"' + SUBMIT_PATH + '\"'
        if not os.path.exists(self.submitExecutablePath.strip("\"")): 
        #"
            nuke.tprint("Smedge Submit executable could not be found. Check the script configuration SUBMIT_PATH variable")
            nuke.message("Smedge not installed. Press OK to cancel.")
            return None

        # default packet size is 5
        self.packetSize = "1"

        # determine the job name
        try:
           self.jobName = self.nukeScriptPath.split('/')[ - 1].split('.')[ - 2]
        except:
            nuke.tprint("script not saved")
            nuke.message("This script hasn't been saved yet. Press OK to cancel.")
            return None

        # build the interface
        self.srPanel = nuke.Panel("SmedgeRenderJob (c) Uberware")
        self.srPanel.addSingleLineInput("start frame", self.nukeFromFrame)
        self.srPanel.addSingleLineInput("end frame", self.nukeToFrame)
        self.srPanel.addBooleanCheckBox("proxy mode", 0)
        if self.nukeSelectedNode == "":
            self.srPanel.addEnumerationPulldown("write nodes", "all")
        else:
            self.srPanel.addEnumerationPulldown("write nodes", "selected all")
        self.srPanel.addSingleLineInput("packet size", self.packetSize)
        self.srPanel.addEnumerationPulldown("priority", "0 1 2 3 4 5 6 7 8 9")
        self.srPanel.addEnumerationPulldown("pool", "2D 3D")
        self.srPanel.addSingleLineInput("note", "")
        self.srPanel.addBooleanCheckBox("h264", 0)
        self.srPanel.addBooleanCheckBox("dnxhd", 0)
        self.srPanel.addBooleanCheckBox("paused", 0)
        self.srPanel.addButton("Cancel")
        self.srPanel.addButton("Submit")

        # show the panel and get the result
        self.action_result = self.srPanel.show()
        if self.action_result == 1:
            nuke.tprint("Submitting to Smedge...\n")
            self.checkUserInput()
            self.executeCmdJob()
            return None
        else:
            nuke.tprint("Smedge submit canceled\n")
            return None


    # Validate the user input from the window
    def checkUserInput(self):
        self.nukeFromFrame = self.srPanel.value("start frame")
        self.nukeToFrame = self.srPanel.value("end frame")
        self.packetSize = self.srPanel.value("packet size")

        try:
            if self.nukeFromFrame != str(int(self.nukeFromFrame)):
                nuke.message("Please enter numeric values only for start frame!")
            else:
                self.nukeFromFrame = int(self.srPanel.value("start frame"))
        except StandardError, x:
            nuke.message("Please enter numeric values only for start frame!")
            return None

        try:
            if self.nukeToFrame != str(int(self.nukeToFrame)):
                nuke.message("Please enter numeric values only for end frame!")
            else:
                self.nukeToFrame = int(self.srPanel.value("end frame"))
        except StandardError, x:
            nuke.message("Please enter numeric values only for end frame!")
            return None

        try:
            if self.packetSize != str(int(self.packetSize)):
                nuke.message("Please enter numeric values only for packet size!")
            else:
                self.packetSize = int(self.srPanel.value("packet size"))
        except StandardError, x:
            nuke.message("Please enter numeric values only for packet size!")
            return None        


    # build and execute the command line
    def executeCmdJob(self):
        # filename fix for PC Farm
        self.nukeScriptPath = self.nukeScriptPath.replace( "/Volumes/Projects/", "Z:/" ).replace("/media/Projects/", "Z:/").replace("/Volumes/Wilde/", "Y:/").replace("/media/Wilde/", "Y:/").replace("/Volumes/Elements/", "X:/").replace("/media/Elements/", "X:/")
        
        # compute -p render string
        if self.srPanel.value("proxy mode") == True:
            renderProxyString = " -p"
        else:
            renderProxyString = ""

        # compute nuke render string
        if self.srPanel.value("render nodes") == "all":
            renderNodeString = ""
        else:
            renderNodeString = self.nukeSelectedNode
                               
        # computer -paused flag string
        if self.srPanel.value("paused") == True:
            renderPaused = ' -paused'
        else:
            renderPaused = ""
        
        # computer -note flag string
        if self.srPanel.value("h264") == True:
            renderNote = 'h264 ' + self.srPanel.value("note")
        else:
            renderNote = self.srPanel.value("note")
            
        # computer -note flag string
        if self.srPanel.value("dnxhd") == True:
            renderNote2 = 'dnxhd ' + self.srPanel.value("note")
        else:
            renderNote2 = self.srPanel.value("note")


        # get everything together
        cmdText = '%s script -type Nuke -scene %s -name \"%s\" -priority %s -pool \"%s\" -note \"%s %s\" %s -range %i-%i -packetsize %i -writenode \"%s\" -extra \"%s\" -creator \"godzilla\"' % (self.submitExecutablePath, self.nukeScriptPath, self.jobName, self.srPanel.value("priority"), self.srPanel.value("pool"), renderNote, renderNote2, renderPaused, self.nukeFromFrame, self.nukeToFrame, self.packetSize, renderNodeString, renderProxyString)
        nuke.tprint(cmdText)
        # split into chunks so it works correctly on Unix platforms
        args = shlex.split(cmdText)

        try:
            # create the child process
            handle=subprocess.Popen(args)
            # wait for it to finish
            returncode=handle.wait()
            # make sure it worked
            if returncode>0:
                nuke.tprint("Smedge job could not be submitted, error code: %s\nSee nuke terminal for details." % (returncode))
                nuke.message("Smedge job could not be submitted, error code: %s\nSee nuke terminal for details." % (returncode))
                return None
            else:
                nuke.tprint("Smedge job successfully submitted. See nuke terminal for details.")
                nuke.message("Smedge job successfully submitted. See nuke terminal for details.")
        except StandardError,x:
            nuke.tprint("Smedge job could not be submitted, error:\n%s\nSee nuke terminal for details." % (x))
            nuke.message("Smedge job could not be submitted, error:\n%s\nSee nuke terminal for details." % (x))
            return None
