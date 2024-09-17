# I'm not using this code any more & I made some minor updates
# Put all speeds very slow for testing; be ready to E-stop!!!!!

# Disclaimer: The provided code is open-source and free to use, modify, and distribute.
# The author shall not be held responsible for any injury, damage, or loss resulting from the use of this code.
# By using this code, you agree to assume all responsibility and risk associated with the use of the code.

# Python code to automatically change the tool on an ATC router and measure it if its value in the tool table is 0

# Change tool script for SIMCNC & Csmio-s
# Erwan Le Foll 23/04/2022    https://youtube.com/@erwan3953

# The homing in this code is done at the top right of your table with home values Y0, X0, Z0.
# The working area is therefore in negative values. (This can be modified)

from ConfigMachine import *  # Import the ConfigMachine.py file, which must be in the same directory as m6.py
import time   # Import time for the function time.sleep
import sys    # For using the function sys.exit()

#-----------------------------------------------------------
# Function checks if a tool is in place; otherwise stops the program
# Copy/Paste the two sentences below to the desired location in the code starting from #Start of the macro

# Read_if_tool_in(check_tool_in_spindle)
# Read_if_tool_in(check_clamp_status)
#-----------------------------------------------------------

def Read_if_tool_in(input_number):
    if input_number is None:  # Ignore the code if the input is configured as None
        return
    elif input_number == check_tool_in_spindle:  # Indicates the number of the input to control configured at the beginning of the code
        mod_IP = d.getModule(ModuleType.IP, 0)  # Call the CSMIO IP-S module
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet:  # PinSet = On
            print("Sensor: Tool detected")  # Message in the console
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:  # PinReset = Off
            print("There is no tool in the spindle.")  # Message in the console
            msg.info("There is no tool in the spindle.")
            sys.exit(1)  # Stop the program
    elif input_number == check_clamp_status:  # Second input check
        mod_IP = d.getModule(ModuleType.IP, 0)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:
            print("Sensor: Clamp closed")
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet:
            print("Clamp open")
            msg.info("Clamp open")
            sys.exit(1)   # Stop the program

#-----------------------------------------------------------
# Function checks if the tool has been properly released; otherwise stops the program
# Copy/Paste the two sentences below to the desired location in the code

# Read_if_tool_out(check_tool_in_spindle)
# Read_if_tool_out(check_clamp_status)
#-----------------------------------------------------------

def Read_if_tool_out(input_number):
    if input_number is None:  # Ignore the code if the input is configured as None
        return
    elif input_number == check_tool_in_spindle:
        mod_IP = d.getModule(ModuleType.IP, 0)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet:
            print("The tool remains in the spindle")
            msg.info("The tool remains in the spindle")
            sys.exit(1)  # Stop the program
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:
            print("Sensor: The tool has been successfully released")
    elif input_number == check_clamp_status:
        mod_IP = d.getModule(ModuleType.IP, 0)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:
            print("The clamp sensor indicates that the clamp has remained closed.")
            msg.info("The clamp sensor indicates that the clamp has remained closed.")
            sys.exit(1)  # Stop the program
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet:
            print("Sensor: Clamp Open")

#-----------------------------------------------------------
# Function to activate any specified digital outputs example:
# on = set_digital_output(valve_collet, DIOPinVal.PinSet)
# off = set_digital_output(valve_collet, DIOPinVal.PinReset)
# Replace 'valve_collet' to handle other outputs; see ConfigMachine.py
#-----------------------------------------------------------

def set_digital_output(output_number, value):
    if output_number is None:  # If ConfigMachine.py returns None, the function is ignored
        return
    try:
        mod_IP = d.getModule(ModuleType.IP, 0)  # For CSMIO IP-S
        mod_IP.setDigitalIO(output_number, value)
    except NameError:
        print("------------------\nThe digital output has not been well defined.")

############################################################
# Start of the macro
############################################################

#-----------------------------------------------------------
# Check if there is a tool in the spindle. If "no tool," indicates tool zero in SimCNC.
#-----------------------------------------------------------

mod_IP = d.getModule(ModuleType.IP, 0)
if mod_IP.getDigitalIO(IOPortDir.InputPort, check_tool_in_spindle) == DIOPinVal.PinReset:
    d.setSpindleToolNumber("0")
    print("------------------\n NO TOOL IN SPINDLE.\n------------------")

#-----------------------------------------------------------
# Ask the CSMIO and name the returned values.
#-----------------------------------------------------------

# Get the tool number on the spindle and name it "hold_tool."
hold_tool = d.getSpindleToolNumber()

# Get the tool number from the G-code and name it "new_tool."
new_tool = d.getSelectedToolNumber()

# Get the known size in SimCNC of the new tool.
new_tool_length = d.getToolLength(new_tool)

# Get the machine's position and name it "position."
position = d.getPosition(CoordMode.Machine)

# Get the Y coordinate and name it y_coord.
y_coord = position[Y]

# Remove soft limits.
d.ignoreAllSoftLimits(True)

#-----------------------------------------------------------
# Prevent G-code from calling Probe 3D
#-----------------------------------------------------------

if threeD_prob is not None and new_tool == threeD_prob:
    print("The tool called in the G-code cannot be the 3D probe")
    msg.info("The tool called in the G-code cannot be the 3D probe")
    sys.exit(1)  # Stop the program

#-----------------------------------------------------------
# Get the tool number in the spindle and then return it to its place.
#-----------------------------------------------------------

# Evacuate the dust collector
set_digital_output(valve_dustCollect_out, DIOPinVal.PinSet)
time.sleep(2)
set_digital_output(valve_dustCollect_out, DIOPinVal.PinReset)

# If new_tool equals hold_tool or zero, skip procedure of storing hold_tool
if hold_tool != new_tool and hold_tool != 0:

    if hold_tool <= ToolCount:  # Checks if the tool number is between 1 and ToolCount
        print(f"------------------\n Storing tool number {hold_tool}\n------------------")
    else:
        msg.info("------------------\nThe tool called in the G-code does not exist")
        sys.exit(1)  # Stop the program

    # Calculate the X position based on the tool number
    X_position_hold_tool = X_position_first_tool + ((hold_tool - 1) * X_distance_between_tools)
    print(f"------------------\n Old tool will be stored at the location: {hold_tool}\n------------------")

    #-----------------------------------------------------------
    # Stop spindle
    #-----------------------------------------------------------

    d.setSpindleState(SpindleState.OFF)  # Turn off the spindle
    start_time_stop_spin = time.time()  # Start a timer

    #-----------------------------------------------------------
    # Begin movements to store hold_tool
    #-----------------------------------------------------------

    # Move Z axis up
    position[Z] = 0
    d.moveToPosition(CoordMode.Machine, position, Z_up_speed)

    # Check where the machine is and then shift Y if necessary
    if y_coord > Y_position_safe_zone:
        # Move towards the safe zone on the Y-axis
        position[Y] = Y_position_safe_zone
        d.moveToPosition(CoordMode.Machine, position, YX_speed)

    # Move in X and Y to a safe zone to avoid touching the tools
    position[X] = X_position_hold_tool
    position[Y] = Y_position_safe_zone
    d.moveToPosition(CoordMode.Machine, position, YX_speed)

    # Move the Y axis to the final location
    position[Y] = Y_position_first_tool
    d.moveToPosition(CoordMode.Machine, position, YX_speed)

    # Calculate the elapsed time since the timer was started and pause if the configured time_spindle_stop is not elapsed
    time_spent = time.time() - start_time_stop_spin
    remaining_time = time_spindle_stop - time_spent
    if remaining_time > 0:
        print(f"------------------\n {remaining_time} before next move, spindle still turning!!!\n------------------")
        time.sleep(remaining_time)

    # Move Z axis fast approach
    position[Z] = Z_position_approach
    d.moveToPosition(CoordMode.Machine, position, Z_down_fast_speed)

    # A quick blow of compressed air
    set_digital_output(valve_blower, DIOPinVal.PinSet)
    time.sleep(blowing_time)  # See timing in ConfigMachine.py
    set_digital_output(valve_blower, DIOPinVal.PinReset)

    # Move Z axis slow final approach
    position[Z] = Z_position_tools
    d.moveToPosition(CoordMode.Machine, position, Z_down_final_speed)

#-----------------------------------------------------------
# Retrieve the tool number from the M6 G-code, calculate its position, and perform the corresponding movements
#-----------------------------------------------------------

if hold_tool != new_tool:  # Ignore the code if hold_tool == new_tool

    if new_tool <= ToolCount:
        # Check that the new tool does not exceed ToolCount
        new_tool = (new_tool - 1) % ToolCount + 1
        print(f"------------------\n Loading the new tool: {new_tool}\n------------------")
    else:
        msg.info("Tool number called is too large.")
        sys.exit(1)  # Stop the program

    # Release the tool or open the clamp if there was no tool
    set_digital_output(valve_collet, DIOPinVal.PinSet)

    # Name the tool zero in SimCNC; in case of emergency stop, it is important that SimCNC knows there is no tool
    d.setToolOffsetNumber(0)

    # Pause for clamp opening
    time.sleep(0.5)

    # If the start of the script was skipped because of a zero tool, then replace Y
    # Otherwise, do not move because you are already at this location
    position[Y] = Y_position_first_tool
    d.moveToPosition(CoordMode.Machine, position, YX_speed)

    # Calculate the X position based on the tool number
    X_position_new_tool = X_position_first_tool + ((new_tool - 1) * X_distance_between_tools)

    # Raise Z to zero
    position[Z] = 0
    d.moveToPosition(CoordMode.Machine, position, Z_up_speed)

    # Verify that a tool has been properly released
    Read_if_tool_out(check_tool_in_spindle)
    Read_if_tool_out(check_clamp_status)

    # Move X above new tool
    position[X] = X_position_new_tool
    d.moveToPosition(CoordMode.Machine, position, YX_speed)

    # Move Z-axis in fast approach
    position[Z] = Z_position_approach
    d.moveToPosition(CoordMode.Machine, position, Z_down_fast_speed)

    # Clean the cone
    set_digital_output(valve_clean_cone, DIOPinVal.PinSet)

    # Move Z axis to final slow approach
    position[Z] = Z_position_tools
    d.moveToPosition(CoordMode.Machine, position, Z_down_final_speed)

    # Finish cleaning the cone
    set_digital_output(valve_clean_cone, DIOPinVal.PinReset)

    # Lock the tool
    set_digital_output(valve_collet, DIOPinVal.PinReset)

    # Pause
    time.sleep(0.5)

    # Indicate to SimCNC that the new tool is in place
    d.setToolLength(new_tool, new_tool_length)
    d.setToolOffsetNumber(new_tool)
    d.setSpindleToolNumber(new_tool)

    # Raise Z to zero after picking up the tool
    position[Z] = 0
    d.moveToPosition(CoordMode.Machine, position, Z_up_speed)

    # Check if a tool is in place
    Read_if_tool_in(check_tool_in_spindle)
    Read_if_tool_in(check_clamp_status)

    # Move the Y axis to a safe zone to avoid hitting other tools
    position[Y] = Y_position_safe_zone
    d.moveToPosition(CoordMode.Machine, position, YX_speed)

    print("-------------------\n End of tool change \n--------------------")

    #-----------------------------------------------------------
    # End of tool change movements
    #-----------------------------------------------------------
else:
    print(f"-------------------\n The tool {new_tool} is already in place \n--------------------")

#-----------------------------------------------------------
# Begin measurement script, based on the original from SimCNC
#-----------------------------------------------------------

if do_i_have_prob == True:  # Check at the beginning of the code whether or not the measurement should be launched

    # Verify if the length of the new_tool in SimCNC is 0 (not measured). If it is, execute the measurement code
    if new_tool_length == 0 or every_time_get_measure == True:
        print(f"Tool {new_tool} Launching the measurement process.")

        # Move in XY safe zone to avoid collisions with stored tools
        position[X] = probeStartAbsPos['X_probe']
        position[Y] = Y_position_safe_zone
        d.moveToPosition(CoordMode.Machine, position, YX_speed)

        # Move Y above the probe
        position[Y] = probeStartAbsPos['Y_probe']
        d.moveToPosition(CoordMode.Machine, position, YX_speed)

        # Descend Z rapidly; the tool should not touch the probe yet
        position[Axis.Z.value] = probeStartAbsPos['Z_probe']
        d.moveToPosition(CoordMode.Machine, position, Z_down_fast_speed)

        # A quick blow of compressed air
        set_digital_output(valve_blower, DIOPinVal.PinSet)
        time.sleep(blowing_time)  # Blowing time
        set_digital_output(valve_blower, DIOPinVal.PinReset)

        # Start of the fast probing
        position[Axis.Z.value] = zEndPosition
        probeResult = d.executeProbing(CoordMode.Machine, position, probeIndex, fastProbeVel)
        if(probeResult == False):
            sys.exit("Fast probing failed!")

        # Save the result of the fast probe
        fastProbeFinishPos = d.getProbingPosition(CoordMode.Machine)

        # Z up between the two measurements
        d.moveAxisIncremental(Axis.Z, goUpDist, Z_up_speed)

        # Pause between the two measurements
        time.sleep(fineProbingDelay)

        # Start of the slow probing
        probeResult = d.executeProbing(CoordMode.Machine, position, probeIndex, slowProbeVel)
        if(probeResult == False):
            sys.exit("Slow probing failed!")

        # Save the result of the slow probe
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
        d.moveToPosition(CoordMode.Machine, position, Z_up_speed)

        # Print in the console the tool offset of the new tool
        print("Tool offset ({:d}): {:.4f}".format(new_tool, new_tool_length))

        # Return to the soft limit zone
        position[Y] = Y_position_safe_zone
        d.moveToPosition(CoordMode.Machine, position, YX_speed)

        #-----------------------------------------------------------
        # End of probing script
        #-----------------------------------------------------------
    else:
        print(f"-------------------\n Tool {new_tool} already measured \n--------------------")
else:
    print("-------------------\n Tool measurement cancelled, no probe installed \n--------------------")

# Return to the soft limit zone
position[Y] = Y_position_safe_zone
d.moveToPosition(CoordMode.Machine, position, YX_speed)

# Dust shoe back in place
set_digital_output(valve_dustCollect_under, DIOPinVal.PinSet)
time.sleep(2)
set_digital_output(valve_dustCollect_under, DIOPinVal.PinReset)

# Activate soft limits
d.ignoreAllSoftLimits(False)

# Export the new tool information to SimCNC
d.setToolLength(new_tool, new_tool_length)
d.setToolOffsetNumber(new_tool)
d.setSpindleToolNumber(new_tool)
