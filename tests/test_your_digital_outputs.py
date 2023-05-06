# Tester vos sorties numeriques sans vous fatiguer
# Test your digital outputs without getting tired

#######################################################################
# Définissez le numéro de sortie numérique ici . None = pas configuré
valve_collet = 13               # cone porte outils
valve_dustColect_under = 11     # déplacement du récupérateur de poussières sous la broche
valve_dustColect_out = 9       # déplacement du récupérateur de poussières  a coté de la broche
valve_clean_cone = 14           # Nettoyage du cone
valve_nozel = 12                # Soufflette
valve_dor = None                # ouverture trappe outils/tourniquet
dust_collection = None          # démarrage de l'aspiration
vacum_pump = None               # pompe a vide /table a déprésion
#######################################################################

import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

# Affiche une fenêtre de dialogue pour demander si vous voulez lancer le script ou tester une sortie numérique spécifique
root = tk.Tk()
root.withdraw()
choice = messagebox.askyesno("Question", "Voulez-vous tester toutes les sorties numériques en séquence (Oui) ou tester une sortie numérique spécifique (Non)?")
if not choice:
    specific_output = simpledialog.askinteger("Numéro de sortie", "Entrez le numéro de sortie numérique à tester:")
    if specific_output is None:
        sys.exit()





# début du script

# Dictionnaire pour associer les noms de valves à leurs numéros
valve_names = {valve_collet: "valve_collet",
               valve_dustColect_under: "valve_dustColect_under",
               valve_dustColect_out: "valve_dustColect_out",  
               valve_clean_cone: "valve_clean_cone",
               valve_nozel: "valve_nozel",
               valve_dor: "valve_dor",
               dust_collection: "dust_collection",
               vacum_pump: "vacum_pump"}

# Liste des sorties
output_list = [valve_collet, valve_dustColect_under, valve_dustColect_out, valve_clean_cone, valve_nozel, valve_dor, dust_collection, vacum_pump]  



# Modifie la sortie digital
def set_digital_output(output_number, value):
    try:
        mod_IP = d.getModule(ModuleType.IP, 0)
        mod_IP.setDigitalIO(output_number, value)
    except NameError:
        print("Variable incorect définir un chiffre ou None si non utilisé")  # message d'erreur

# Boucle pour activer et désactiver les sorties numériques
for output in output_list:
    if output is not None:
        # Active la sortie numérique spécifiée
        set_digital_output(output, DIOPinVal.PinSet)
        msg.info("Test de la sortie " + valve_names[output] + " (N° " + str(output) + ")", "Info")
        # Désactive la sortie numérique spécifiée
        set_digital_output(output, DIOPinVal.PinReset)


# Boucle pour activer et désactiver les sorties numériques
if choice:
    for output in output_list:
        if output is not None:
            # Active la sortie numérique spécifiée
            set_digital_output(output, DIOPinVal.PinSet)
            msg.info("Test de la sortie " + valve_names[output] + " (N° " + str(output) + ")", "Info")
            # Désactive la sortie numérique spécifiée
            set_digital_output(output, DIOPinVal.PinReset)
else:
    if specific_output in valve_names:
        # Active la sortie numérique spécifiée
        set_digital_output(specific_output, DIOPinVal.PinSet)
        msg.info("Test de la sortie " + valve_names[specific_output] + " (N° " + str(specific_output) + ")", "Info")
        # Désactive la sortie numérique spécifiée
        set_digital_output(specific_output, DIOPinVal.PinReset)
    else:
        msg.error("Numéro de sortie non valide. Veuillez vérifier les numéros de sortie définis.")
