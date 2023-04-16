# Tester vos sorties numeriques sans vous fatiguer
# Test your digital outputs without getting tired

#######################################################################
# Définissez le numéro de sortie numérique ici None = pas configuré
valve_collet = 13           # cone porte outils
valve_dust_colector = None  # déplacement du récupérateur de poussières
valve_clean_cone = 15       # Nettoyage du cone
valve_nozel = 12            # Soufflette
valve_dor = None            # ouverture trappe outils/tourniquet
dust_collection = None      # démarrage de l'aspiration
vacum_pump = None           # pompe/table a vide
#######################################################################

# début du script

# Dictionnaire pour associer les noms de valves à leurs numéros
valve_names = {valve_collet: "valve_collet",
               valve_dust_colector: "valve_dust_colector",
               valve_clean_cone: "valve_clean_cone",
               valve_nozel: "valve_nozel",
               valve_dor: "valve_dor",
               dust_collection: "dust_collection",
               vacum_pump: "vacum_pump"}

# Liste des sorties
output_list = [valve_collet, valve_dust_colector, valve_clean_cone, valve_nozel, valve_dor, dust_collection, vacum_pump]


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