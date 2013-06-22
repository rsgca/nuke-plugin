# @title setProjectFrameRange
# @description Prompts the user for received and deliverable handle ranges on the selected read node to calculate project frame range
# @author Richard Greenwood
# @version 1.0
# @compatible Nuke6v3
# @url www.richardgreenwood.ca

import nuke, nukescripts

if nuke.env["gui"]:
    class setProjectFrameRange ( nukescripts.PythonPanel ):
        def __init__( self ):
            #Set Project Handle Defaults
            handlesInHead = 48
            handlesInTail = 48
            handlesOutHead = 8
            handlesOutTail = 8

            #create dialogue box
            nukescripts.PythonPanel.__init__( self, "Set Project Frame Range" )
            #define knobs
            self.handlesInText = nuke.Text_Knob ( "handlesInText", "Received Handles" )
            self.handlesInHead = nuke.Int_Knob ( "handlesInHead", "Head" )
            self.handlesInTail = nuke.Int_Knob ( "handlesInTail", "Tail" )
            self.handlesInTail.clearFlag(nuke.STARTLINE)
            self.handlesOutText = nuke.Text_Knob ( "handlesOutText", "Deliverable Handles" )
            self.handlesOutHead = nuke.Int_Knob ( "handlesOutHead", "Head" )
            self.handlesOutTail = nuke.Int_Knob ( "handlesOutTail", "Tail" )
            self.handlesOutTail.clearFlag( nuke.STARTLINE )
            #add knobs
            self.addKnob ( self.handlesInText )
            self.addKnob ( self.handlesInHead )
            self.addKnob ( self.handlesInTail )
            self.addKnob ( self.handlesOutText )
            self.addKnob ( self.handlesOutHead )
            self.addKnob ( self.handlesOutTail )
            #populate knobs
            self.handlesInHead.setValue( handlesInHead )
            self.handlesInTail.setValue( handlesInTail )
            self.handlesOutHead.setValue( handlesOutHead )
            self.handlesOutTail.setValue( handlesOutTail )

        #shows as modal dialogue (adds 'ok' and 'cancel' buttons)
        def showPanel( self ):
            result = nukescripts.PythonPanel.showModalDialog( self )
            if result:
                setFrameRange( self.handlesInHead.value(), self.handlesInTail.value(), self.handlesOutHead.value(), self.handlesOutTail.value())

# Returns setProjectFrameRange dialogue
def callPanel():
    plate = nuke.selectedNode()
    if plate.Class() == 'Read':
        return setProjectFrameRange().showPanel()
    else:
        nuke.tprint("Selected node must be a Read node.")
        nuke.message("Selected node must be a Read node.")

# Calculates and sets project frame ranges from a selected read node
def setFrameRange(hInHead = 48, hInTail = 48, hOutHead = 8, hOutTail = 8):
    plate = nuke.selectedNode()
    # starts plate at frame 1
    plate["frame_mode"].setValue(1)
    plate["frame"].setValue("1")
    # calculates frame range
    firstFrame = str(1+hInHead-hOutHead)
    lastFrame = str(1+plate["last"].getValue()-plate["first"].getValue()-hInTail+hOutTail)
    #sets project frame range
    nuke.knob("root.first_frame",firstFrame)
    nuke.knob("root.last_frame",lastFrame)
    nuke.knob("root.lock_range", "1")
