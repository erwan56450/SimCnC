import tkinter as tk
print("start")  # Error message
initial_time_in_seconds = 10  # Initial configuration in seconds

class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Window")

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate position to center the window
        x_position = (screen_width - 200) // 2
        y_position = (screen_height - 200) // 2  # Adjustment to accommodate the "Skip" button

        # Position and resize the window
        self.root.geometry(f"200x200+{x_position}+{y_position}")

        # Force the window to stay on top
        self.root.wm_attributes("-topmost", 1)

        # Add a label for the text "Spindle Warm Up"
        warm_up_label = tk.Label(self.root, text="Spindle Warm Up", font=("Helvetica", 14))
        warm_up_label.pack()

        # Add a label to display the countdown with a font size of 30
        self.countdown_label = tk.Label(self.root, text="", font=("Helvetica", 30), padx=10, pady=10)
        self.countdown_label.pack()

        # "Skip" button to stop the countdown and close the window
        skip_button = tk.Button(self.root, text="Skip", command=self.skipCountdownAndClose)
        skip_button.pack()

        # Automatically start the countdown
        self.startCountdown(seconds=initial_time_in_seconds)

    def updateCountdown(self):
        if self.seconds_left > 0:
            mins, secs = divmod(self.seconds_left, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            self.countdown_label.config(text=timer)
            self.seconds_left -= 1
            self.root.after(1000, self.updateCountdown)  # Update every 1000 milliseconds (1 second)
        else:
            self.root.after(100, self.closeWindow)  # Close the window after 0.1 seconds

    def startCountdown(self, minutes=None, seconds=None):
        if minutes is not None:
            self.seconds_left = minutes * 60
        elif seconds is not None:
            self.seconds_left = seconds
        else:
            raise ValueError("You must provide either 'minutes' or 'seconds' argument.")
        self.updateCountdown()

    def skipCountdownAndClose(self):
        # Stop updating the countdown
        self.seconds_left = 0
        # Close the window after 0.1 seconds
        self.root.after(100, self.closeWindow)

    def closeWindow(self):
        # Close the window
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownApp(root)
    root.mainloop()

print("end")
