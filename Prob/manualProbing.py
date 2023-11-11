# Disclaimer: The provided code is open-source and free to use, modify, and distribute. 
# The author shall not be held responsible for any injury, damage, or loss resulting from the use of this code.
# By using this code, you agree to assume all responsibility and risk associated with the use of the code.

# replace the probing.py of simcnc
import sys
# Get the tool number on the spindle and name it "hold_tool".
current_tool = d.getSpindleToolNumber()  

# Retrieve the machine's position and name it "position".
position = d.getPosition(CoordMode.Machine)


#MODIFY HERE WHAT NEEDED
probeIndex = 0  #see in simcnc what numeber is your prob
speed_down = 400
speed_up = 500
refToolProbePos = -100   #Height at which your reference tool touches the probe (if your reference tool touches at Z-100mm and you indicate - 100mm here, then it will be referenced to 0mm)
go_down = 3  # go down for 3mm

#-----------------------------------------------------------
# Start moving
#-----------------------------------------------------------

print(f"------------------\n Tool {current_tool} Launching the measurement process .\n------------------")

# Start measuring
position[Axis.Z.value] -= go_down
probeResult = d.executeProbing(CoordMode.Machine, position, probeIndex, speed_down)
if(probeResult == False):
    sys.exit((" probing failed!"))

# récupère la mesure lente
probeFinishPos = d.getProbingPosition(CoordMode.Machine)

# Calculate the tool offset
new_tool_length = probeFinishPos[Axis.Z.value] - refToolProbePos

# Print in console
print(f"Tool Z offset({current_tool}): {new_tool_length:.4f}")

# Export new tool info to simcnc
d.setToolLength(current_tool, new_tool_length)
d.setToolOffsetNumber(current_tool)
d.setSpindleToolNumber(current_tool)

# Z to 0
position[Axis.Z.value] = 0
d.moveToPosition(CoordMode.Machine, position, speed_up)

# Print in console
print("End")

#-----------------------------------------------------------
# End script probing
#-----------------------------------------------------------
