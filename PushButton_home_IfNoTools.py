# Code a lier avec un bouton home dans simcnc 
# Verifit qu'il n'y a pas d'outil dans la broche avant de faire un homing.
# tester le code dans la console script
# Ouvrir l'editeur d'interface Simcnc > Configuration > openGUIeditor > selectionner le bouton par defaut du homing qui va etre rempalcer.
# dans le fenetre GUI editor (une fois le bouton home selectioné) en bas a droite cliquer sur "OUPUT: clicked > "ref all Axes"  remplacer par "RUN SCRIPT" et selectioner HomingPerso.py ")
# Le script doit etre sauvegardé la ou "Run script" a ouvert la fenetre.

check_tool_in_spindel = 24 # Numero de l'entrée a vérifier si "off" avant le homing # None =ignoré

import time

d.executeGCode( "M3 S5000" )
time.sleep(1)
d.setSpindleState( SpindleState.OFF )
time.sleep(0.5)

if check_tool_in_spindel is not None: # Vérifie si l'entrée n'est pas configurée sur None
    mod_IP = d.getModule(ModuleType.IP, 0) # Appelle le module CSMIO IP-S
    if mod_IP.getDigitalIO(IOPortDir.InputPort, check_tool_in_spindel) == DIOPinVal.PinSet: # PinSet = allumé
        msg.info("Retirez l'outil dans la broche avant le homing", "Info")# Affiche un message dans la console
        sys.exit(1) # Arrête le programme
    elif mod_IP.getDigitalIO(IOPortDir.InputPort, check_tool_in_spindel) == DIOPinVal.PinReset: # PinReset = éteint
        print("Lancement du homing") # Affiche un message dans la console passe au homing

#execute home
d.executeHoming()