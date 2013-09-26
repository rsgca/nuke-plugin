###########################################################
# SubmitToDeadline.tcl
# Ryan Russell (Thinkbox Software Inc), 2009
#
# Proxy Nuke tcl script that sources the repository
# submission script.
###########################################################

proc SubmitToDeadline {} {
	global env
	global WIN32
	
	set tempPath ""
	if {$WIN32} {
		set tempPath $env(TEMP)
	} else {
		set tempPath "/tmp"
	}
	
	set outputFilename "$tempPath/output.txt"
	set exitCodeFilename "$tempPath/exitCode.txt"
	
	# Call DeadlineCommandBG to get the repository root.
	if {[file exists "/Applications/Deadline/Resources/bin/deadlinecommandbg"] == 1} {
		catch {exec "/Applications/Deadline/Resources/bin/deadlinecommandbg" "-outputFiles" $outputFilename $exitCodeFilename "-getrepositoryroot"}
	} else {
		catch {exec "deadlinecommandbg" "-outputFiles" $outputFilename $exitCodeFilename "-getrepositoryroot"}
	}
	
	# Read in the output file which contains the repository root.
	catch {set fileid [open $outputFilename r]}
	gets $fileid repositoryRoot
	close $fileid
	
    #trim if we find a non printable character at the start
	set firstChar [string index $repositoryRoot 0]
	if {![string is print $firstChar]} {
		set repositoryRoot [string trim $repositoryRoot $firstChar]
	}
    
	# Prepend the root to the submission script path and execute it.
	set scriptFilename [file join $repositoryRoot "submission/Nuke/SubmitNukeToDeadline.tcl"]
	if {[file exists $scriptFilename] == 1} {
		source $scriptFilename
	} else {
		error "The SubmitNukeToDeadline.tcl script could not be found in the Deadline Repository. Please make sure that the Deadline Client has been installed on this machine, that the Deadline Client bin folder is in your PATH, and that the Deadline Client has been configured to point to a valid Repository."
	}
}