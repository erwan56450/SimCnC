# work in progresse DOn't USE 
# work in progresse DOn't USE 
# work in progresse DOn't USE 
# work in progresse DOn't USE 
# work in progresse DOn't USE 

# Disclaimer: The provided code is open-source and free to use, modify, and distribute. 
# The author shall not be held responsible for any injury, damage, or loss resulting from the use of this code.
# By using this code, you agree to assume all responsibility and risk associated with the use of the code.

# If like me you have bought a Simcnc card but your change tool rack is not ready , you will need to change the tool manually.
# Replace the M6.py in the simcnc folder by thise one.

# where you want the spindel for the change of tools
Y_pos_chang_tool = -1400
X_pos_chang_tool = -1000
Z_pos_chang_tool = 0

# speed 
speed = 2000

# other
mesure_the_tool = True      #if probing.py is configure you can mesure the tool after clique OK 

# name axis when d.getposition respond
X = 0
Y = 1
Z = 2


# Get the tool number from the gcode and name it "new tool".
new_tool = d.getSelectedToolNumber()

# Get the known size in simcnc of the new tool name it "new_tool_length"
new_tool_length = d.getToolLength(new_tool)

# Get the machine's position and name it "position".
position = d.getPosition(CoordMode.Machine)

# Import the library for message boxes
import tkinter as tk
from tkinter import messagebox

# Create a message box with custom-sized buttons and window
def show_message_box():
    root = tk.Tk()  # Create a temporary root window
    root.withdraw()  # Hide the root window

    # Adjust the size of the buttons and window
    root.option_add('*TButton*padding', 10)  # Adjust button padding
    root.option_add('*TButton*font', ('Helvetica', 12))  # Adjust button font size
    root.option_add('*Dialog.msg.font', ('Helvetica', 14))  # Adjust message font size

    result = messagebox.askquestion(
        "Info",
        "gcode ask tool = " + str(new_tool) + "\nContinue without measuring?",
        icon='info',
        type=messagebox.YESNO
    )

    if result == 'no':  # If the "Measure tool" button is clicked
        exec(open('probing.py').read())

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

#call the message box display function
show_message_box()

# Export the new tool information to SimCNC.
d.setToolLength (new_tool,new_tool_length)
d.setToolOffsetNumber(new_tool)
d.setSpindleToolNumber(new_tool)

print ("Manuel change tool finish")