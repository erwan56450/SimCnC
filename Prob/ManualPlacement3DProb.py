# Disclaimer: The provided code is open-source and free to use, modify, and distribute. 
# The author shall not be held responsible for any injury, damage, or loss resulting from the use of this code.
# By using this code, you agree to assume all responsibility and risk associated with the use of the code.

# author Erwan Le Foll 11/11/2023


# creat a buton for 3dprob with manual placement


import sys
# Get the tool number
current_tool = d.getSpindleToolNumber()  

# Retrieve the machine's position and name it "position".
position = d.getPosition(CoordMode.Machine)


#MODIFY HERE WHAT NEEDED
probeIndex = 2  #see in simcnc what number is your prob 0 1 2 or 3
speed_down = 100
speed_up = 800
TreeDProbOvertravel = 1   #There is a slight overtravel, a few millimeters of additional movement occurring between the moment the probe makes contact with the workpiece  and the activation of the probe switch.
probMovment = 5  # go down for **mm , if no prob touch during those  mm dissent it stop moving

#-----------------------------------------------------------
# Start moving
#-----------------------------------------------------------

print("------------------\n  Launching the measurement process .\n------------------")

if current_tool != 1:
    sys.exit("Wrong tool number")


# Start measuring
position[Axis.Z.value] -= probMovment
probeResult = d.executeProbing(CoordMode.Machine, position, probeIndex, speed_down)
if(probeResult == False):
    sys.exit((" probing failed!"))

# récupère la mesure lente
probeFinishPos = d.getProbingPosition(CoordMode.Machine)

# Calculate the tool offset
newZhigt = probeFinishPos[Axis.Z.value] - TreeDProbovertravel

# Export new tool info to simcnc
d.setAxisProgPosition( Z, newZhigt )

# Z up
position[Axis.Z.value] += probMovment
d.moveToPosition(CoordMode.Machine, position, speed_up)

# Print in console
print("End Z probing")

#-----------------------------------------------------------
# End script probing
#-----------------------------------------------------------
