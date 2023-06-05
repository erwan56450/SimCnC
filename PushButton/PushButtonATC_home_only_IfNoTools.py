# Code to link with a home button in simcnc
# Check that there is no tool in the spindle before doing a homing.

# Open the Simcnc interface editor > Configuration > openGUIeditor > select the default button of the homing that will be replaced.
# in the GUI editor window (once the home button has been selected) at the bottom right click on "OUPUT: clicked > "ref all Axes" replace with "RUN SCRIPT" and select HomingPerso.py ")
# The script must be saved where "Run script" opened the window.

check_tool_in_spindel = 24 # Set the corect number of spindel tool sensor

import time

# On this machine the spindle must turn a few turns for the sensor to work correctly (delet this 4 line if no need)
d.executeGCode( "M3 S5000" )
time.sleep(0.5)
d.setSpindleState( SpindleState.OFF )
time.sleep(3)
# end start spindel


if check_tool_in_spindel is not None: # Vérifie si l'entrée n'est pas configurée sur None
    mod_IP = d.getModule(ModuleType.IP, 0) # Appelle le module CSMIO IP-S
    if mod_IP.getDigitalIO(IOPortDir.InputPort, check_tool_in_spindel) == DIOPinVal.PinSet: # PinSet = allumé
        msg.info("Retirez l'outil dans la broche avant le homing", "Info")# Affiche un message dans la console
        sys.exit(1) # Arrête le programme
    elif mod_IP.getDigitalIO(IOPortDir.InputPort, check_tool_in_spindel) == DIOPinVal.PinReset: # PinReset = éteint
        print("Lancement du homing") # Affiche un message dans la console passe au homing

#execute home
d.executeHoming()