# Disclaimer: The provided code is open-source and free to use, modify, and distribute. 
# The author shall not be held responsible for any injury, damage, or loss resulting from the use of this code.
# By using this code, you agree to assume all responsibility and risk associated with the use of the code.
# This code was created to test and validate the movement of the tool charger and its calculation; it serves no other purpose.

# Tool change script for SIMCNC & Csmio-s 
# Created by Erwan Le Foll on 24/04/2022      https://youtube.com/@erwan3953

C_speed = 1000  # Speed of the motor movement
C_position_first_tool = 44  # Position of motor C when the tool is in the carousel at tool position 1
C_position_last_tool = 355  # Position of motor C when the tool is in the carousel at the last tool position
Tool_count = 8  # Maximum number of tools in the carousel
C = 5  # Number of the motor to actuate (motor C)

hold_tool = d.getSpindleToolNumber()  # Retrieves the number of the current tool
position = d.getPosition(CoordMode.Machine)  # Retrieves the machine's current position

if 1 <= hold_tool <= Tool_count:  # Checks that the tool number is within the valid range
    # Calculates the position of the tool in motor C based on its number
    hold_tool_position_C = ((C_position_last_tool - C_position_first_tool) / (Tool_count - 1) * (hold_tool - 1)) + C_position_first_tool
else:
    print(f"The current tool number ({hold_tool}) exceeds the maximum allowed number of tools ({Tool_count})")

print(f"The position of the current tool is: {hold_tool_position_C}")

# Moves motor C to the position corresponding to the current tool
position[C] = hold_tool_position_C
d.moveToPosition(CoordMode.Machine, position, C_speed)
