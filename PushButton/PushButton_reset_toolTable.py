# see how to add this to simcnc here https://youtu.be/OfvQqaUnNeQ

# Code to link to a new button in SimCNC to reset tool compensation from 1 to 100
# Used if you are using one of my ATC codes with the "every_time_get_measure = false" option
# because if the tool has already been measured, it will not be measured again.
# So, every time you replace the end mill, you can click on this button.


import tkinter as tk

def reset_tool_length():
    for tool_table in range(1, 100): #reset les tailles d'outils de 1 a 100
        n_tool = tool_table
        current_tool_length = d.getToolLength(n_tool)

        if current_tool_length != 0:
            d.setToolLength(n_tool, 0)
            print(f"The measurement of tool {n_tool} has been reset.")
        
    print(" All tool measurements have been reset.")
    root.destroy()

def cancel_reset():
    root.destroy()

root = tk.Tk()
root.title("Reset Tool Length")
message = "Are you sure you want to reset all tool lengths?"
label = tk.Label(root, text=message)
label.pack(pady=20)

button_frame = tk.Frame(root)
button_frame.pack()

ok_button = tk.Button(button_frame, text="Reset All", command=reset_tool_length)
ok_button.pack(side=tk.LEFT, padx=10)

cancel_button = tk.Button(button_frame, text="Cancel", command=cancel_reset)
cancel_button.pack(side=tk.LEFT, padx=10)

root.mainloop()
