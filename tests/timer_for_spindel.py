import tkinter as tk
print("start")  # message d'erreur
initial_time_in_seconds = 3  # Configuration initiale en secondes

class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Window")

        # Obtenir les dimensions de l'écran
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculer la position pour centrer la fenêtre
        x_position = (screen_width - 200) // 2
        y_position = (screen_height - 200) // 2  # Ajustement pour accommoder le bouton "Skip"

        # Positionner et redimensionner la fenêtre
        self.root.geometry(f"200x200+{x_position}+{y_position}")

        # Forcer la fenêtre à rester au premier plan
        self.root.wm_attributes("-topmost", 1)

        # Ajout d'une étiquette pour le texte "Spindle Warm Up"
        warm_up_label = tk.Label(self.root, text="Spindle Warm Up", font=("Helvetica", 14))
        warm_up_label.pack()

        # Ajout d'une étiquette pour afficher le compte à rebours avec une police de taille 30
        self.countdown_label = tk.Label(self.root, text="", font=("Helvetica", 30), padx=10, pady=10)
        self.countdown_label.pack()

        # Bouton "Skip" pour arrêter le compteur et fermer la fenêtre
        skip_button = tk.Button(self.root, text="Skip", command=self.skipCountdownAndClose)
        skip_button.pack()

        # Démarrage automatique du compte à rebours
        self.startCountdown(seconds=initial_time_in_seconds)

    def updateCountdown(self):
        if self.seconds_left > 0:
            mins, secs = divmod(self.seconds_left, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            self.countdown_label.config(text=timer)
            self.seconds_left -= 1
            self.root.after(1000, self.updateCountdown)  # Mise à jour toutes les 1000 millisecondes (1 seconde)
        else:
            self.countdown_label.config(text="Countdown finished")
            self.root.after(100, self.closeWindow)  # Fermer la fenêtre après 2 secondes

    def startCountdown(self, minutes=None, seconds=None):
        if minutes is not None:
            self.seconds_left = minutes * 60
        elif seconds is not None:
            self.seconds_left = seconds
        else:
            raise ValueError("You must provide either 'minutes' or 'seconds' argument.")
        self.updateCountdown()

    def skipCountdownAndClose(self):
        # Mettez à jour l'étiquette pour indiquer que le compteur a été ignoré
        self.countdown_label.config(text="Countdown skipped")
        # Arrêtez la mise à jour du compteur
        self.seconds_left = 0
        # Fermez la fenêtre après 2 secondes
        self.root.after(100, self.closeWindow)

    def closeWindow(self):
        # Fermer la fenêtre
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownApp(root)
    root.mainloop()

print("end")  
