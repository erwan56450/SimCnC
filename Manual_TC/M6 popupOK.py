#this code to use in M6.py simply stops the Gcode with a popup window so that you can change tools, it's up to you to restart the gcode with the PLAY button of simcnc.

d.setSpindleToolNumber(d.getSelectedToolNumber( ))
d.setToolOffsetNumber(d.getSelectedToolNumber( ))

tool = d.getSelectedToolNumber( )

print("load tool number = " + str(tool))

msg.info( "load tool number = " + str(tool), "Info" )

d.stopTrajectory()
d.setGCodeNextLine()