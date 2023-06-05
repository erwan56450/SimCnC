# work in progresse DOn't USE 
# work in progresse DOn't USE 
# work in progresse DOn't USE 
# work in progresse DOn't USE 
# work in progresse DOn't USE 

# Disclaimer: The provided code is open-source and free to use, modify, and distribute. 
# The author shall not be held responsible for any injury, damage, or loss resulting from the use of this code.
# By using this code, you agree to assume all responsibility and risk associated with the use of the code.

# If like me you have bought a Simcnc card but your Atc is not ready, you will need to change the tool manually.
# Replace the M6.py 

# where you want the spindel for the change of tools
Y_pos_chang_tool = -1500
X_pos_chang_tool = -1000
Z_pos_chang_tool = 0

# speed 
speed = 2000

# other
mesure_the_tool = True      #if probing.py is configure you can mesure the tool after clique OK 

# name for d.getposition axis
X = 0
Y = 1
Z = 2


# Get the tool number from the gcode and name it "new tool".
new_tool = d.getSelectedToolNumber()

# Get the known size in simcnc of the new tool name it "new_tool_length"
new_tool_length = d.getToolLength(new_tool)

# Get the machine's position and name it "position".
position = d.getPosition(CoordMode.Machine)



########################################################
# macro start
########################################################

# move Z 
position[Z] = Z_pos_chang_tool
d.moveToPosition(CoordMode.Machine, position, speed)

# move to change tool place
position[Y] = Y_pos_chang_tool
position[X] = X_pos_chang_tool
d.moveToPosition(CoordMode.Machine, position, speed)

# window popup 
msg.info( "inséré l'outil  = " + str(new_tool), "Info" )

#d.stopTrajectory()
#d.setGCodeNextLine()

# Export the new tool information to SimCNC.
d.setToolLength (new_tool,new_tool_length)
d.setToolOffsetNumber(new_tool)
d.setSpindleToolNumber(new_tool)

if mesure_the_tool == True
    exec(open('probing.py').read())


print ("Manuel change tool finish")