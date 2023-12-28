# Disclaimer: The provided code is open-source and free to use, modify, and distribute. 
# The author shall not be held responsible for any injury, damage, or loss resulting from the use of this code.
# By using this code, you agree to assume all responsibility and risk associated with the use of the code.

# replace the probing.py of simcnc
# TO WORK Correctly this code need to import the configmachine.py  like that it use the same parameter in m6.py & in probing.py

# update 26/11/2023 add moving tool rack

import sys
import time
from ConfigMachine import *



#-----------------------------------------------------------
# Fonction pour Activer n'importe quelle sorties numériques spécifiée exemple:
# allumé=   set_digital_output(valve_collet, DIOPinVal.PinSet)   
# eteinte=  set_digital_output(valve_collet, DIOPinVal.PinReset)
# remplacer 'valve_collet' pour géré d'autres sortie, voir au debut script)
#-----------------------------------------------------------

def set_digital_output(output_number, value):
    if output_number is None:
        return
    try:
        mod_IP = d.getModule(ModuleType.IP, 0) # pour cismo ipS
        mod_IP.setDigitalIO(output_number, value)
    except NameError:
        print(("------------------\nThe digital output has not been well defined."))

#-----------------------------------------------------------
# Function to activate air tool rack UNDER from spindel
#-----------------------------------------------------------

def tool_rack_under():
    #Call ouput tool rack under
    print("call tool rack under")
    mod_IP.setDigitalIO(ToolRackUnder, DIOPinVal.PinSet)

    time.sleep(2)#time for piston to expend


#-----------------------------------------------------------
# Function to activate air tool rack OUT from spindel
#-----------------------------------------------------------

def tool_rack_out():

    #close the air out Valve of tool rack
    mod_IP.setDigitalIO(ToolRackUnder, DIOPinVal.PinReset)
    time.sleep(0.2)

    #Call ouput  tool rack out
    print("Start removing the tool holder")
    mod_IP.setDigitalIO(ToolRackOut, DIOPinVal.PinSet)

    time.sleep(2) #time for piston to expend

    print("tool rack is out")
    mod_IP.setDigitalIO(ToolRackOut, DIOPinVal.PinReset) #stop output 

#stop spindel (just in case)
d.setSpindleState(SpindleState.OFF) 


#-----------------------------------------------------------
# Ask the Csmio , and name the returned values with names.
#-----------------------------------------------------------

#Get the tool number on the spindle and name it "hold_tool".
current_tool = d.getSpindleToolNumber()  

# Retrieve the machine's position and name it "position".
position = d.getPosition(CoordMode.Machine)

#-----------------------------------------------------------
#see if there is a tool in the spindle, If "no" indicates in Simcnc tool "Zero".
#-----------------------------------------------------------

mod_IP = d.getModule(ModuleType.IP, 0)

if mod_IP.getDigitalIO(IOPortDir.InputPort, check_tool_in_spindel) == DIOPinVal.PinReset:
    d.setSpindleToolNumber("0")
    print(("------------------\nNO TOOL IN SPINDEL.\n------------------"))
    msg.info("NO TOOL IN SPINDEL", "Info")  #error message
    sys.exit(1) # stop the programe

#-----------------------------------------------------------
#Start moving
#-----------------------------------------------------------

print((f"------------------\n Tool {current_tool} Launching the measurement process .\n------------------"))

# Up Z
position[Z] = 0
d.moveToPosition(CoordMode.Machine, position, YX_speed)

# displacement in XY above the prob
position[X] = probeStartAbsPos['X_probe']
position[Y] = probeStartAbsPos['Y_probe']
d.moveToPosition(CoordMode.Machine, position, YX_speed)

# Move air tool rack under the spindel
tool_rack_under()

# Z rapid descent, the tool must not touch the prob yet
position[Axis.Z.value] = probeStartAbsPos['Z_probe']
d.moveToPosition(CoordMode.Machine, position, Z_down_fast_speed)

# a quick blow of compressed air (see machineconfig.py for number output)
set_digital_output(valve_blower, DIOPinVal.PinSet)
time.sleep (blowing_time) #temps du soufflage
set_digital_output(valve_blower, DIOPinVal.PinReset)

# start speed mesurement
position[Axis.Z.value] = zEndPosition
probeResult = d.executeProbing(CoordMode.Machine, position, probeIndex, fastProbeVel)
if(probeResult == False):
    sys.exit(("fast probing failed!"))

# Retrieve the quick measurement.
fastProbeFinishPos = d.getProbingPosition(CoordMode.Machine)

# Raise Z between the two measurements.
d.moveAxisIncremental(Axis.Z, goUpDist, Z_up_speed)

#Pause between the two measurements
time.sleep(fineProbingDelay)

# Start of the slow measurement
probeResult = d.executeProbing(CoordMode.Machine, position, probeIndex, slowProbeVel)
if(probeResult == False):
    sys.exit(("slow probing failed!"))

# Retrieve the slow measurement
probeFinishPos = d.getProbingPosition(CoordMode.Machine)

# Look at the difference between the two measurements if to mutch difference error
probeDiff = abs(fastProbeFinishPos[Axis.Z.value] - probeFinishPos[Axis.Z.value])
print("Fast Probe (axe Z): {:.4f}, Fine Probe (axe Z): {:.4f}".format(fastProbeFinishPos[Axis.Z.value], probeFinishPos[Axis.Z.value]))
if(probeDiff > fineProbeMaxAllowedDiff and checkFineProbingDiff == True):
    errMsg = "ERROR: Difference between the two measurements is too large (diff: {:.3f})".format(probeDiff)
    sys.exit( errMsg)

# calculate  tool length
new_tool_length = probeFinishPos[Axis.Z.value] - refToolProbePos

# Export the new tool information to SimCNC.)
d.setToolLength (current_tool,new_tool_length)
d.setToolOffsetNumber(current_tool)
d.setSpindleToolNumber(current_tool)

#  up Z to O
position[Axis.Z.value] = 0
d.moveToPosition(CoordMode.Machine, position, Z_up_speed)

#move tool rack out from spindel
tool_rack_out()

# Print in the console the offset of the new tool
print(("tool Z offset({:d}) : {:.4f}".format(current_tool, new_tool_length)))

#-----------------------------------------------------------
#fin script probing
#-----------------------------------------------------------