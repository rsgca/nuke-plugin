import nuke, pipeline, setProjectFrameRange

# TOOLS
# ////////////////////////////////////////////////////////////////////////////////
menubar=nuke.menu("Nodes")
m=menubar.addMenu("Tools")
m.addCommand("Slate", "nuke.createNode('Slate')", index=1, icon="slate.png")
m.addCommand("Owerlays", "nuke.createNode('Overlays')", index=2, icon="slate.png")
m.addSeparator()

n=m.addMenu("WRITE", icon="Write.png")
n.addCommand("Write EXR File Server", "pipeline.customWrite(extension = 'exr')", index=1, icon="Write.png")
n.addCommand("Write EXR Review", "pipeline.customWrite(server = 'review', extension = 'exr')", index=2, icon="Write.png")

if (nuke.env['LINUX'] != 1):
	n.addCommand("Write MOV File Server", "pipeline.customWrite('file', 'Review', 'mov' )", index=4, icon="Write.png")

n=m.addMenu("LUT", icon=":qrc/images/Toolbar3DLUT.png")

n=m.addMenu("Colour", icon=":qrc/images/ToolbarColor.png")
n.addCommand("Despill Madness", "nuke.createNode('DespillMadness')",  icon="Sphere.png")

n=m.addMenu("Draw", icon=":qrc/images/ToolbarDraw.png")
n.addCommand("FlareFactory Plus", "nuke.createNode('FlareFactory_Plus')", icon="FlareFactoryPlus.png")
n.addCommand("AutoFlare", "nuke.createNode('AutoFlare2')")
n.addCommand("4 Point Gradient", "nuke.createNode('magicCarpet')", icon="magicCarpet.png")

n=m.addMenu("Filter", icon=":qrc/images/ToolbarFilter.png")
n.addCommand("AlphaEdge", "nuke.createNode('AlphaEdge')", icon=":qrc/images/ToolbarFilter.png")
n.addCommand("FieldsKit", "nuke.createNode('FieldsKit')", icon=":qrc/images/ToolbarFilter.png")
n.addCommand("EdgeExtend", "nuke.createNode('EdgeExtend')", icon=":qrc/images/ToolbarFilter.png")
n.addCommand("Chromatic Aberation", "nuke.createNode('akromatism_stRub')", icon=":qrc/images/ToolbarFilter.png")
n.addCommand("Directional Blur", "nuke.createNode('directionalBlur_rk')", icon=":qrc/images/ToolbarFilter.png")
n.addCommand("Bokeh Blur", "nuke.createNode('BokehBlur_4')", icon=":qrc/images/ToolbarFilter.png")

n=m.addMenu("Grain", icon="grain.png")
n.addCommand("REDNoise4", "nuke.createNode('REDNoise4')", index=1, icon="red-noise.png")
n.addCommand("GrainEdge", "nuke.createNode('GrainEdge')", index=2, icon="grain.png")
n.addCommand("GrainControl", "nuke.createNode('GrainControl')", index=3, icon="grain.png")

n=m.addMenu("Transform", icon=":qrc/images/ToolbarTransform.png")
n.addCommand("SmartPin", "nuke.createNode('SmartPin')", icon="ConerPin.png")

n=m.addMenu("Generate")
n.addCommand("Random", "nuke.createNode('Random')", index=3, icon='smokey-ryan.png')

# MENUS
# ////////////////////////////////////////////////////////////////////////////////
menubar=nuke.menu("Nuke")

m=menubar.addMenu("&File")
#Version up Comp number
m.addCommand("Save New Comp Version", "pipeline.script_comp_version_up()", index=5 )
m.addCommand("Save New Anim Version", "pipeline.script_anim_version_up()", index=6 )

m=menubar.addMenu("&Edit")
#Set Project Frame Range
m.addCommand("&Node/Set Project Frame Range From Node", setProjectFrameRange.callPanel, '^R')

m=menubar.addMenu("&Render")
#Render Manager - SMEDGE
import SmedgeRender
m.addSeparator(index=5)
m.addCommand("Submit to Smedge", "SmedgeRender.SmedgeRender()", "^F5", index=6)

m = menubar.addMenu("Extra", index=6)
# Nuke2Maya
import FromNuke2MayaExporter, FromMaya2NukeImporter
m.addCommand("Export Camera as fm2n-File", "FromNuke2MayaExporter.FromNuke2MayaExporter()")
m.addCommand("Import fm2n-File", "FromMaya2NukeImporter.FromMaya2NukeImporter()")
#Collect Files Menu Node
m.addSeparator()
import collectFiles
m.addCommand('Collect Files', 'collectFiles.collectFiles()')
#reveal in OS
import revealInOS
m.addCommand('Reveal In Finder','revealInOS.revealInOS()', icon='Read.png')
m.addSeparator()
#Metadata
import showMetaData
m.addCommand("Show MetaData","nuke.display('showMetaData.showMeta()', nuke.selectedNode(),'MetaData at ' + nuke.selectedNode().name(), 1000)","ctrl+m")
m.addCommand("Mirror Nodes X Axis", "nuke.tcl('MirrorNodePos x')")


#Templates

tempPath = [s for s in nuke.pluginPath() if 'templates' in s]

m = menubar.addMenu("&Templates", index=7)

m.addCommand("Additive Key", "nuke.nodePaste( '%s/additive_key.nk' % (tempPath[0]) )", index=1)
m.addCommand("Advanced Despill", "nuke.nodePaste('%s/advanced_despill.nk' % (tempPath[0]))", index=2)
m.addCommand("AOV", "nuke.nodePaste('%s/AOVs.nk' % (tempPath[0]))", index=3)
m.addCommand("Fine Key", "nuke.nodePaste('%s/fine_key.nk' % (tempPath[0]))", index=4)

