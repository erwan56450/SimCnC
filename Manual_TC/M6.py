
# Disclaimer: The provided code is open-source and free to use, modify, and distribute. 
# The author shall not be held responsible for any injury, damage, or loss resulting from the use of this code.
# By using this code, you agree to assume all responsibility and risk associated with the use of the code.
# Be careful anyway, this is not a safe way to change a tool, because the machine  is still "enable"

# If like me you have bought a Simcnc card but your change tool rack is not ready , you will need to change the tool manually.
# Replace the M6.py in the simcnc folder by thise one.
# To use the measure button you have to configure your probing.py correctly

# where you want the spindel for the change of your tools
Y_pos_chang_tool = -1200
X_pos_chang_tool = -1000
Z_pos_chang_tool = 0

# speed of move to reach the above position
speed = 4000

# moving commande, call by Move_to_change_tool_pos() in the macro
def Move_to_change_tool_pos():
    # move Z 
    position[Z] = Z_pos_chang_tool
    d.moveToPosition(CoordMode.Machine, position, speed)

    # move to change tool place
    position[Y] = Y_pos_chang_tool
    position[X] = X_pos_chang_tool
    d.moveToPosition(CoordMode.Machine, position, speed)

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

# Set in simcnc the tool infos
d.setToolLength (new_tool,new_tool_length)
d.setToolOffsetNumber(new_tool)
d.setSpindleToolNumber(new_tool)

# Create a message box with 3 buttons and execute probing.py or d.enableMachine(False)
import tkinter as tk

def show_custom_message_box():
    global root, message_label

    root = tk.Tk()
    root.title("m6 tool change")

    # ...

    # Ajoutez ce bloc de code ici, avant le mainloop
    def on_closing():
        d.enableMachine(False)  #  désactivez la machine
        root.destroy()  # Fermez la fenêtre
    
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

def mesurer_outil():
    exec(open('probing.py').read())

def stop():
    d.enableMachine(False)

def toggle_blink():
    if message_label.cget("foreground") == "black":
        message_label.config(fg="red")
    else:
        message_label.config(fg="black")
    root.after(500, toggle_blink)  # Toggle every 500 milliseconds

def show_custom_message_box():
    global root, message_label

    root = tk.Tk()
    root.title("m6 tool change")

    custom_font = ('Helvetica', 16)  # Define a custom font 

    message_label = tk.Label(root, text="Gcode ask tool N°" + str(new_tool) + "\nManually change your tool, then make your choice below:", font=custom_font)
    message_label.pack(padx=50, pady=50)

    toggle_blink()  # Start blinking

    # Make the window always on top
    root.wm_attributes("-topmost", 1)

    
    def on_closing():
        d.enableMachine(False)  # Disable the machine if the X button is clicked
        root.destroy()  # Fermez la fenêtre

    button_frame = tk.Frame(root)
    button_frame.pack()

    continuer_button = tk.Button(button_frame, text="\u25B6 Continue ", command=root.destroy, font=custom_font)
    continuer_button.pack(side=tk.LEFT, padx=30, pady=30)

    mesurer_button = tk.Button(button_frame, text="Measure Tool", command=mesurer_outil, font=custom_font)
    mesurer_button.pack(side=tk.LEFT, padx=30, pady=30)

    stop_button = tk.Button(button_frame, text="\u25A0 STOP", command=stop, fg="white", bg="red", font=custom_font)
    stop_button.pack(side=tk.RIGHT, padx=30, pady=30)

    Go_to_change_tool_pos = tk.Button(button_frame, text="Move to Change tool location", command=Move_to_change_tool_pos, font=custom_font)
    Go_to_change_tool_pos.pack(side=tk.LEFT, padx=30, pady=30)

    # Capture l'événement de fermeture de la fenêtre
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()


########################################################
# macro start
########################################################
print ("Manual change tool Start")

#Turn off the spindle
d.setSpindleState(SpindleState.OFF) 

# if new tool length = zero, execute Move_to_change_tool_pos
if new_tool_length == 0:  
    Move_to_change_tool_pos()

#call the message box display function
show_custom_message_box()

print ("Manual change tool finish")