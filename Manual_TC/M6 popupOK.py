d.setSpindleToolNumber(d.getSelectedToolNumber( ))
d.setToolOffsetNumber(d.getSelectedToolNumber( ))

tool = d.getSelectedToolNumber( )

print("load tool number = " + str(tool))

msg.info( "load tool number = " + str(tool), "Info" )

d.stopTrajectory()
d.setGCodeNextLine()