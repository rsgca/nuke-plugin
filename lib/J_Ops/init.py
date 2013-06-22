#  init.py
#  J_Ops
#
#  Created by Jack Binks on 14/02/2010.
#  Copyright (c) 2010 Jack Binks. All rights reserved.
import sys, nuke, os

for path in nuke.pluginPath():
    if os.path.exists(path+"/J_Ops/py"):
        sys.path.append(path+"/J_Ops/py")
    if os.path.exists(path+"/../J_Ops/py"):
        sys.path.append(path+"/py")
    if os.path.exists(path+"/../J_Ops/ndk"):
        nuke.pluginAddPath(path+"/ndk")
    if os.path.exists(path+"/../J_Ops/icons"):         
        nuke.pluginAddPath(path+"/icons")
        
        
