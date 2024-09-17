# Disclaimer: The provided code is open-source and free to use, modify, and distribute.
# The author shall not be held responsible for any injury, damage, or loss resulting from the use of this code.
# By using this code, you agree to assume all responsibility and risk associated with the use of the code.

# Change tool script for SIMCNC & CSMIO-S
# Erwan Le Foll 24/05/2022   Version 1.2   https://youtube.com/@erwan3953

# Automatic tool change script for a tool changer with CAROUSEL
# Here, the carousel motor is on the C axis in degrees (or Linear mm).
# For axes in degrees, configure > axes > C > RotaryType (1->360) to take the shortest path

# Watch out! The tool sensor of this spindle needs to turn to verify that a tool is in place
# https://www.usinages.com/threads/projet-de-retrofit-complet-dune-cnc-axyz.162287/

from ConfigMachine import *  # Import the ConfigMachine.py file, which must be in the same directory as m6.py
import time   # Import time for the function time.sleep
import sys    # To use the sys.exit() function

#-----------------------------------------------------------
# Function checks if a tool is in place; otherwise, stops the program
# Copy/Paste the two lines below to the desired location in the code starting from #Start of the macro
# Read_if_tool_in(check_tool_in_spindle)
# Read_if_tool_in(check_clamp_status)
#-----------------------------------------------------------

def Read_if_tool_in(input_number):
    if input_number == None:  # Ignore the code if the input is configured as None
        return
    elif input_number == check_tool_in_spindle:  # Indicates the input number to control configured at the beginning of the code
        mod_IP = d.getModule(ModuleType.IP, 0)  # Call the CSMIO IP-S
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet:  # PinSet = On
            print("A tool has been detected in the spindle.")  # Message in the console
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:  # PinReset = Off
            print("There is no tool in the spindle.")  # Message in the console
            msg.info("There is no tool in the spindle.")
            sys.exit(1)  # Stop the program
    elif input_number == check_clamp_status:  # Second input check
        mod_IP = d.getModule(ModuleType.IP, 0)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:
            print("The clamp is closed")
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet:
            print("The clamp is open")
            msg.info("The clamp is open")
            sys.exit(1)   # Stop the program

#-----------------------------------------------------------
# Function checks if the tool has been properly released; otherwise, stops the program
# Copy/Paste the two lines below to the desired location in the code
# Read_if_tool_out(check_tool_in_spindle)
# Read_if_tool_out(check_clamp_status)
#-----------------------------------------------------------

def Read_if_tool_out(input_number):
    if input_number == None:  # Ignore the code if the input is configured as None
        return
    elif input_number == check_tool_in_spindle:
        mod_IP = d.getModule(ModuleType.IP, 0)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet:
            print("The tool remains in the spindle")
            msg.info("The tool remains in the spindle")
            sys.exit(1)  # Stop the program
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:
            print("There is no tool in the spindle")
    elif input_number == check_clamp_status:
        mod_IP = d.getModule(ModuleType.IP, 0)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:
            print("The clamp remained closed")
            msg.info("The clamp remained closed")
            sys.exit(1)  # Stop the program
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet:
            print("The clamp is open.")

#-----------------------------------------------------------
# Function to activate any specified digital outputs.
# Copy/Paste one of the lines below to the desired location in the code
# On:    set_digital_output(valve_collet, DIOPinVal.PinSet)
# Off:   set_digital_output(valve_collet, DIOPinVal.PinReset)
# Replace 'valve_collet' in the lines above to handle other outputs; see at the beginning of the script
#-----------------------------------------------------------

def set_digital_output(output_number, value):
    if output_number is None:
        return
    try:
        mod_IP = d.getModule(ModuleType.IP, 0)  # For CSMIO IP-S
        mod_IP.setDigitalIO(output_number, value)
    except NameError:
        msg.info("The digital output has not been properly defined")

############################################################
# Start of the macro
############################################################

#-----------------------------------------------------------
# Query the CSMIO and assign the returned values with names
#-----------------------------------------------------------
# Get the tool number on the spindle and name it 'hold_tool'
hold_tool = d.getSpindleToolNumber()
# Get the tool number from the G-code and name it 'new_tool'
new_tool = d.getSelectedToolNumber()
# Get the known length of the new tool
new_tool_length = d.getToolLength(new_tool)
# Get the machine position
position = d.getPosition(CoordMode.Machine)
# Save the Y coordinate as 'Y_coord' so that at the end of the script Y returns to this position
Y_coord = position[Y]
# Remove soft limits
d.ignoreAllSoftLimits(True)

#-----------------------------------------------------------
# Check if there is a tool in the spindle; if "no tool," indicate tool zero in SimCNC.
#-----------------------------------------------------------

# Move the Z axis to the zero position
position[Z] = 0
d.moveToPosition(CoordMode.Machine, position, Z_speed_up)
# Small spindle start (for a capricious sensor)
d.executeGCode("M3 S5000")
time.sleep(1)
d.setSpindleState(SpindleState.OFF)
time.sleep(2)

mod_IP = d.getModule(ModuleType.IP, 0)
if mod_IP.getDigitalIO(IOPortDir.InputPort, check_tool_in_spindle) == DIOPinVal.PinReset:
    d.setSpindleToolNumber("0")  # Name tool 0 in SimCNC
    print("------------------\nNo tool detected in the spindle.\n------------------")

# Get the tool number on the spindle and name it 'hold_tool'
hold_tool = d.getSpindleToolNumber()

#-----------------------------------------------------------
# Stop spindle
#-----------------------------------------------------------

d.setSpindleState(SpindleState.OFF)  # Turn off the spindle
start_time_stop_spin = time.time()  # Start a timer

# Raise the dust collector if the input is defined
set_digital_output(valve_dust_collector, DIOPinVal.PinSet)

# Open the carousel door
set_digital_output(valve_door, DIOPinVal.PinSet)

#-----------------------------------------------------------
# Movements
#-----------------------------------------------------------

if hold_tool != new_tool and hold_tool != 0:  # If hold_tool is not equal to new_tool and not zero, execute the following lines
    #-----------------------------------------------------------
    # Carousel movement to 'hold_tool'
    #-----------------------------------------------------------

    if hold_tool <= Tool_Count:  # Verify that the tool is not greater than Tool_Count
        hold_tool_position_C = ((C_position_last_tool - C_position_first_tool) / (Tool_Count - 1) * (hold_tool - 1)) + C_position_first_tool  # Calculate the spacing between each storage location
        print(f"hold_tool will be stored at position: {hold_tool}")
    else:
        print(f"The current tool number ({hold_tool}) exceeds the maximum allowed tools ({Tool_Count})")
        sys.exit(1)

    # Move C axis to 'hold_tool' position
    position[C] = hold_tool_position_C
    d.moveToPosition(CoordMode.Machine, position, C_speed)

    #-----------------------------------------------------------
    # Start of gantry movements
    #-----------------------------------------------------------

    # Move the Z axis up
    position[Z] = 0
    d.moveToPosition(CoordMode.Machine, position, Z_speed_up)

    # Move Y before the carousel
    position[Y] = Y_approach
    d.moveToPosition(CoordMode.Machine, position, Y_speed)

    # Calculate the elapsed time since the timer was started and pause if the configured 'time_spindle_stop' has not elapsed
    time_spent = time.time() - start_time_stop_spin
    remaining_time = time_spindle_stop - time_spent
    if remaining_time > 0:
        time.sleep(remaining_time)

    # Descend Z to the height of the tools
    position[Z] = Z_position_tools
    d.moveToPosition(CoordMode.Machine, position, Z_speed_down)

if hold_tool == 0:  # If hold_tool == 0, execute the following lines

    # Move the Z axis up only if hold_tool == 0
    position[Z] = 0
    d.moveToPosition(CoordMode.Machine, position, Z_speed_up)

if hold_tool != new_tool:  # If hold_tool is not equal to new_tool, execute the following lines

    # Move Y into the clamp or above if hold_tool == 0
    position[Y] = Y_tool_clamp
    d.moveToPosition(CoordMode.Machine, position, Y_speed_final)

if hold_tool != new_tool and hold_tool != 0:  # If hold_tool is not equal to new_tool and not zero, execute the following lines

    # Release the tool OR open the clamp if tool zero
    set_digital_output(valve_collet, DIOPinVal.PinSet)

    # Indicate to SimCNC that the new tool zero is in place
    d.setSpindleToolNumber('0')

    # Pause for clamp opening
    time.sleep(0.5)

    # Verify that the clamp is open
    Read_if_tool_out(check_clamp_status)

    # Raise Z to zero
    position[Z] = 0
    d.moveToPosition(CoordMode.Machine, position, Z_speed_up)

    # Close the clamp
    set_digital_output(valve_collet, DIOPinVal.PinReset)
    time.sleep(0.5)

if hold_tool != new_tool:  # If hold_tool is not equal to new_tool, execute the following lines

    # Small spindle start (for a capricious sensor on our spindle)
    d.executeGCode("M3 S5000")
    time.sleep(1)
    d.setSpindleState(SpindleState.OFF)
    time.sleep(2)

    # Verify that there is no tool in the spindle
    Read_if_tool_out(check_tool_in_spindle)

    #-----------------------------------------------------------
    # Carousel movement to 'new_tool'
    #-----------------------------------------------------------

    if new_tool <= Tool_Count:  # Verify that new_tool is not greater than Tool_Count
        New_tool_position_C = ((C_position_last_tool - C_position_first_tool) / (Tool_Count - 1) * (new_tool - 1)) + C_position_first_tool  # Calculate the spacing between each storage location
        print(f"Retrieving tool: {new_tool}")
    else:
        print(f"The new tool number ({new_tool}) exceeds the maximum allowed tools ({Tool_Count})")
        sys.exit(1)

    # Move C axis to 'new_tool' position
    position[C] = New_tool_position_C
    d.moveToPosition(CoordMode.Machine, position, C_speed)

    #-----------------------------------------------------------
    # Movement to fetch 'new_tool'
    #-----------------------------------------------------------

    # Open the clamp
    set_digital_output(valve_collet, DIOPinVal.PinSet)

    # Descend Z for cleaning
    position[Z] = Z_position_clean
    d.moveToPosition(CoordMode.Machine, position, Z_speed_down)

    # Open valve to clean the cone
    set_digital_output(valve_clean_cone, DIOPinVal.PinSet)

    # Descend Z onto 'new_tool'
    position[Z] = Z_position_tools
    d.moveToPosition(CoordMode.Machine, position, Z_speed_down)

    # End of cone cleaning
    set_digital_output(valve_clean_cone, DIOPinVal.PinReset)

    # Close the spindle clamp
    set_digital_output(valve_collet, DIOPinVal.PinReset)

    # Indicate to SimCNC that the new tool is in place
    d.setToolOffsetNumber(new_tool)
    d.setToolLength(new_tool, new_tool_length)
    d.setToolOffsetNumber(new_tool)

    # Y exits the carousel clamp
    position[Y] = Y_approach
    d.moveToPosition(CoordMode.Machine, position, Y_speed_final)

    # Move the Z axis to zero
    position[Z] = 0
    d.moveToPosition(CoordMode.Machine, position, Z_speed_up)

    # Small spindle start (for a capricious sensor on our spindle)
    d.executeGCode("M3 S5000")
    time.sleep(1)
    d.setSpindleState(SpindleState.OFF)
    time.sleep(2)

    # Verify if tool is in the spindle
    Read_if_tool_in(check_tool_in_spindle)
    # Verify if the clamp is closed
    Read_if_tool_in(check_clamp_status)

    # Print in the console
    print("-------------------\n End of tool change \n--------------------")

    #-----------------------------------------------------------
    # End of tool change movements
    #-----------------------------------------------------------
else:
    print(f"-------------------\n The tool {new_tool} is already in place \n--------------------")

##################################################################################################################################
# Beginning of the measurement script, based on the original from SimCNC
##################################################################################################################################

# Check at the beginning of the code whether or not the measurement should be launched (e.g., if you do not have a probe)
if do_i_have_prob == True:

    if new_tool_length == 0 or every_time_get_measure == True:  # Verify if the length of 'new_tool' in SimCNC is zero (not measured) or if the measurement must be performed every time
        print(f"The tool {new_tool} will be measured.")

        # Move in Y above the probe
        position[Y] = probeStartAbsPos['Y_probe']
        d.moveToPosition(CoordMode.Machine, position, Y_speed)

        # Descend Z rapidly; the tool should not touch the probe yet
        position[Axis.Z.value] = probeStartAbsPos['Z_probe']
        d.moveToPosition(CoordMode.Machine, position, Z_speed_down)

        # A quick blow of compressed air
        set_digital_output(valve_blower, DIOPinVal.PinSet)
        time.sleep(blowing_time)  # Blowing time defined at the beginning of the script
        set_digital_output(valve_blower, DIOPinVal.PinReset)

        # Start of the fast measurement
        position[Axis.Z.value] = zEndPosition
        probeResult = d.executeProbing(CoordMode.Machine, position, probeIndex, fastProbeVel)
        if(probeResult == False):
            sys.exit("Fast probing failed!")

        # Get the fast measurement
        fastProbeFinishPos = d.getProbingPosition(CoordMode.Machine)

        # Z up between the two measurements
        d.moveAxisIncremental(Axis.Z, goUpDist, Z_speed_up)

        # Pause between the two measurements
        time.sleep(fineProbingDelay)

        # Start of the slow measurement
        probeResult = d.executeProbing(CoordMode.Machine, position, probeIndex, slowProbeVel)
        if(probeResult == False):
            sys.exit("Slow probing failed!")

        # Get the slow measurement
        probeFinishPos = d.getProbingPosition(CoordMode.Machine)

        # Look at the difference between the two measurements
        probeDiff = abs(fastProbeFinishPos[Axis.Z.value] - probeFinishPos[Axis.Z.value])
        print("Fast Probe (axis Z): {:.4f}, Fine Probe (axis Z): {:.4f}".format(fastProbeFinishPos[Axis.Z.value], probeFinishPos[Axis.Z.value]))
        if(probeDiff > fineProbeMaxAllowedDiff and checkFineProbingDiff == True):
            errMsg = "ERROR: Difference between the two measurements too large (diff: {:.3f})".format(probeDiff)
            sys.exit(errMsg)

        # Calculate the tool length
        new_tool_length = probeFinishPos[Axis.Z.value] - refToolProbePos

        # Raise Z to zero
        position[Axis.Z.value] = 0
        d.moveToPosition(CoordMode.Machine, position, Z_speed_up)

        # Print in the console the tool offset of the new tool
        print("Tool offset ({:d}): {:.4f}".format(new_tool, new_tool_length))

        #-----------------------------------------------------------
        # End of probing script
        #-----------------------------------------------------------
    else:
        print(f"-------------------\n Tool {new_tool} already measured \n--------------------")
else:
    print("-------------------\n Tool measurement canceled, no probe installed\n--------------------")

# Export the new tool information to SimCNC
d.setToolLength(new_tool, new_tool_length)
d.setToolOffsetNumber(new_tool)
d.setSpindleToolNumber(new_tool)

# Move away from the carousel or probe to the Y position recorded at the beginning of the script
position[Y] = Y_coord
d.moveToPosition(CoordMode.Machine, position, Y_speed)

# Activate soft limits
d.ignoreAllSoftLimits(False)

# Stop the valve for the dust collector
set_digital_output(valve_dust_collector, DIOPinVal.PinReset)
# Stop the valve for the carousel door
set_digital_output(valve_door, DIOPinVal.PinReset)
