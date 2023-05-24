# Disclaimer: The provided code is open-source and free to use, modify, and distribute. 
# The author shall not be held responsible for any injury, damage, or loss resulting from the use of this code.
# By using this code, you agree to assume all responsibility and risk associated with the use of the code.

# Code python pour changer d'outil sur fraise ATC automatiqueement et le mesurer si sa valeur dans la table d'outils est = 0
# (Python code to automatically change the tool on an ATC router and measure it if its value in the tool table is = 0 )

# Change tool script for SIMCNC & Csmio-s 
# Erwan Le Foll 23/04/2022    https://youtube.com/@erwan3953

# Le Homming de ce code ce fait en haut a droit de votre table au valeur home=Y0,X0,Z0. La zone de travail est donc en valeurs negatives.(peux ce modifier)
# (The homing in this code is done in the top right of your table with home values = Y0, X0, Z0. The working area is therefore in negative values. (can be modified)

from ConfigMachine import * #Import le fichier ConfigMachine.py qui doit ce trouver dans le meme répertoir que m6.py (#Import the ConfigMachine.py file which must be in the same directory as m6.py)
import time   # importe le temps pour la fonction time.sleep (import time for the function time.sleep)
import sys    # pour utiliser la fonction sys.exit() (to use the sys.exit() function)

#-----------------------------------------------------------
# WORK IN PROGRESS
# Importe le tradution du fichier multilingual.py a placer dans le meme répèretoir que M6
#-----------------------------------------------------------
try:
    from multilingual import _
except ModuleNotFoundError:
    print("The multilingual.py file cannot be found. WORK IN PROGRESS.")
    
    def _(text):
        return text
#-----------------------------------------------------------
# Function checks if a tool is in place, otherwise stops the program
# Copy/Paste the two sentences below to the desired location in the code starting from #Start of the macro

# Read_if_tool_in (check_tool_in_spindel)
# Read_if_tool_in (check_clamp_status)
#-----------------------------------------------------------

def Read_if_tool_in (input_number):
    if input_number == None:  #inogre le code si l'entrée est comfigurée sur None
        return   
    elif input_number == check_tool_in_spindel:  #indique le numero de l'entrée a controler comfiguré au debut du code
        mod_IP = d.getModule(ModuleType.IP, 0) # apelle le csmio ip-s
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet: #pinset =allumé
            print("sensor: tool detected") #message dans la console
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset: #pinreset = éteint
            print("There is no tool in the spindle.") #message dans la console
            msg.info ("There is no tool in the spindle.")
            sys.exit(1)  #arrète le programe (stop the program)
    elif input_number == check_clamp_status:  #2eme verification d'entrée
        mod_IP = d.getModule(ModuleType.IP, 0)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:
            print("sensor: Clamp closed")
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet:
            print("Clamp open")
            msg.info("Clamp open")
            sys.exit(1)   #arrète le programe (stop the program)


#-----------------------------------------------------------
# Function checks if the tool has been properly released, otherwise stops the program
# Copy/Paste the two sentences below to the desired location in the code
#
# Read_if_tool_out (check_tool_in_spindel)     
# Read_if_tool_out (check_clamp_status)
#-----------------------------------------------------------


def Read_if_tool_out(input_number):
    if input_number == None: #inogre le code si l'entrée est comfigurée sur None 
        return   
    elif input_number == check_tool_in_spindel:
        mod_IP = d.getModule(ModuleType.IP, 0)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet:
            print("The tool remains in the spindle")
            msg.info ("The tool remains in the spindle")
            sys.exit(1)  #arrète le programe (stop the program)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:
            print("sensor: The tool has been successfully released")
    elif input_number == check_clamp_status:
        mod_IP = d.getModule(ModuleType.IP, 0)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:
            print("The clamp sensor indicates that the clamp has remained closed.")
            msg.info ("The clamp sensor indicates that the clamp has remained closed.")
            sys.exit(1) #arrète le programe (stop the program)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet:
            print("sensor: Clamp Open")

#-----------------------------------------------------------
# Function to activate any specified digital outputs example:
# on=           set_digital_output(valve_collet, DIOPinVal.PinSet)
# off =         set_digital_output(valve_collet, DIOPinVal.PinReset)
# here replace 'valve_collet' to handle other outputs, see configumachine.py)
#-----------------------------------------------------------

def set_digital_output(output_number, value):
    if output_number is None: #if comfigemachine.py return No number but "None", the Function is ignored
        return
    try:
        mod_IP = d.getModule(ModuleType.IP, 0) # pour cismo ipS
        mod_IP.setDigitalIO(output_number, value)
    except NameError:
        print(_("------------------\nThe digital output has not been well defined."))



############################################################
#Debut de la macro (Macro START)
############################################################

#-----------------------------------------------------------
# Check if there is a tool in the spindle, If "no tool" indicates  tool zero in simcnc.
#-----------------------------------------------------------

mod_IP = d.getModule(ModuleType.IP, 0)
if mod_IP.getDigitalIO(IOPortDir.InputPort, check_tool_in_spindel) == DIOPinVal.PinReset:
    d.setSpindleToolNumber("0")
    print(_("------------------\n NO TOOL IN SPINDEL.\n------------------"))

#-----------------------------------------------------------
# Ask the Csmio , and name the returned values with names.
#--------------------------------------------------------------

# Get the tool number on the spindle and name it "hold_tool".
hold_tool = d.getSpindleToolNumber()

# Get the tool number from the gcode and name it "new tool".
new_tool = d.getSelectedToolNumber()

# Get the known size in simcnc of the new tool.
new_tool_length = d.getToolLength(new_tool)

# Get the machine's position and name it "position".
position = d.getPosition(CoordMode.Machine)
# Get the Y coordinate and name it y_coord.
y_coord = position[Y]  

# Remove soft limit.
d.ignoreAllSoftLimits(True)

#-----------------------------------------------------------
# Prevent gcode from calling Prob3D
#-----------------------------------------------------------

if threeD_prob is not None and new_tool == threeD_prob:
    print("The tool called in the gcode cannot be the prob3D")
    msg.info("The tool called in the gcode cannot be the prob3D" "g-code num err")
    sys.exit(1)  # Arrête le programme (stop the program)
    
#-----------------------------------------------------------
# Get the tool number in the spindle and then return it to its place.
#-----------------------------------------------------------

# evacue le récupérateur de poussières (# evacuates the dust collector)
set_digital_output(valve_dustColect_out, DIOPinVal.PinSet)   
time.sleep(2)
set_digital_output(valve_dustColect_out, DIOPinVal.PinReset)

# If new_tool equals hold_tool or Zero, Skip procedure of storing hold tool
if hold_tool != new_tool and hold_tool != 0: 

    if  hold_tool <= ToolCount:     #Checks if the tool number is between 1 and tool count)
        print(_(f"------------------\n Storing tool number {hold_tool}\n------------------"))  
    else:
        msg.info(_("------------------\nThe tool called in the G-code does not exist", "Oups"))
        sys.exit(1)  # Arrête le programme (stop code)


    # Calculer la position X en fonction du numéro d'outil (Calculate position X based on tool number)
    X_position_hold_tool = X_position_first_tool + ((hold_tool - 1) * X_distance_between_tools)
    print(_(f"------------------\n Old tool will be stored at the location: {hold_tool}\n------------------"))

    #-----------------------------------------------------------
    # Stop spindel
    #-----------------------------------------------------------

    d.setSpindleState(SpindleState.OFF) #etaint la broche (Turn off the spindle)
    start_time_stop_spin = time.time() #lance un chronometre (starts a timer )

    #-----------------------------------------------------------
    #debut des mouvements , déposer l'outil hold_tool (beginning of the movements,drop hold_tool)
    #-----------------------------------------------------------

    # Déplacer l'axe Z en haut (Move Z axis up)
    position[Z] = 0
    d.moveToPosition(CoordMode.Machine, position, Z_up_speed)

    # vérifier où est la machine puis décalage Y si besoin (checking where the machine is and then shifting Y if necessary)
    if y_coord > Y_position_safe_zone:
        # Faire un déplacement vers la zone sûre sur l'axe Y (Making a movement towards the safe zone on the Y-axis)
        position[Y] = Y_position_safe_zone
        d.moveToPosition(CoordMode.Machine, position, YX_speed)

    # deplacement en X et Y en zone sur pour ne pas touche les outils (moving in X and Y in a safe zone to avoid touching the tools)
    position[X] = X_position_hold_tool 
    position[Y] = Y_position_safe_zone
    d.moveToPosition(CoordMode.Machine, position, YX_speed)

    # Déplacer l'axes Y à l'emplacement final (Move the Y axis to the final location)
    position[Y] = Y_position_first_tool
    d.moveToPosition(CoordMode.Machine, position, YX_speed)

    # calcule le temps écoulé depuis le lancement du chronometre et fait une pause si le temps comfiguré time_spindel_stop n'est pas encore écoulé 
    # (Calculates the elapsed time since the timer was started and pauses if the configured time_spindle_stop is not elapsed.)
    time_spent = time.time() - start_time_stop_spin
    remaining_time = time_spindle_stop - time_spent
    if remaining_time > 0: 
        time.sleep(remaining_time)

    # Déplacer l'axe Z approche rapide  (Move the Z axis fast approach)
    position[Z] = Z_position_approach
    d.moveToPosition(CoordMode.Machine, position, Z_down_fast_speed)

    # Un petit coup de soufflette (a quick blow of compressed air)
    set_digital_output(valve_blower, DIOPinVal.PinSet)
    time.sleep (blowing_time) #see timing in configemachine.py
    set_digital_output(valve_blower, DIOPinVal.PinReset)

    # Déplacer l'axe Z approche finale lente (Moving the Z-axis in slow final approach)
    position[Z] = Z_position_tools
    d.moveToPosition(CoordMode.Machine, position, Z_down_final_speed)


#-----------------------------------------------------------
# Récupérer le numéro d'outil du g code M6 puis calcule sa position puis mouvements (Retrieve the tool number from the M6 g-code, calculate its position, and perform the corresponding movements)
#-----------------------------------------------------------

if hold_tool != new_tool: #ignore le code si holdtool= newtool (skip code if holdtool= newtool)

    if  new_tool <= ToolCount:
        # Vérifie que le nouvelle outil ne dépasse pas toolcount (Check that the new tool does not exceed toolcount)
        new_tool = (new_tool - 1) % ToolCount + 1   
        print(_(f"------------------\n Loading the new tool. {new_tool}\n------------------"))
    else:
        msg.info(_("Tool number called to large.", "Oups"))
        sys.exit(1)  # Arrête le programme "Stop the program."

    # Libert l'outil ou ouvre la pince si il n'y avait pas d'outil (relaes the tool or opens the clamp if there was no tool)
    set_digital_output(valve_collet, DIOPinVal.PinSet)

    # Nomme l'outil Zero dans simcnc, En cas d'arret d'urgence il est important que simcnc sache qu'il n'y a plus d'outil
    # Name the tool Zero in simcnc, In case of emergency stop it is important that simcnc knows that there is no more tool
    d.setToolOffsetNumber(0)

    # Pause pour l'ouverture de la pince (Pause for clamp opening)
    time.sleep (0.5)

    # Si le debut du script a été passé a cause d'un outil Zero alors  replace Y ( If the start of the script was skipped because of a Zero tool then replace Y)
    position[Y] = Y_position_first_tool
    d.moveToPosition(CoordMode.Machine, position, YX_speed)

    # Calculer la position X en fonction du numéro d'outil (Calculate the X position based on the tool number)
    X_position_new_tool = X_position_first_tool + ((new_tool - 1) * X_distance_between_tools)

    # remonte Le Z a zero "Raise Z to zero."
    position[Z] = 0
    d.moveToPosition(CoordMode.Machine, position, Z_up_speed)

    #verifie qu'un outil a bien été libéré (Verify that a tool has been properly released)
    Read_if_tool_out (check_tool_in_spindel)
    Read_if_tool_out (check_clamp_status)

    # Déplacer X au dessus de new tool (Move X above new tool.)
    position[X] = X_position_new_tool
    d.moveToPosition(CoordMode.Machine, position, YX_speed)

    # Déplacer l'axe Z aproche rapide (Move Z-axis in fast approach.)
    position[Z] = Z_position_approach
    d.moveToPosition(CoordMode.Machine, position, Z_down_fast_speed)

    # nettoyage du cone (Cleaning the cone)
    set_digital_output(valve_clean_cone, DIOPinVal.PinSet)

    # Déplacer l'axe Z aproche final lente (Move Z axis to final slow approach.)
    position[Z] = Z_position_tools
    d.moveToPosition(CoordMode.Machine, position, Z_down_final_speed)

    # fin nettoyage du cone(Cleaning of the tool taper finished.)
    set_digital_output(valve_clean_cone, DIOPinVal.PinReset)

    # verouille l'outil(Lock the tool)
    set_digital_output(valve_collet, DIOPinVal.PinReset)

    #pause
    time.sleep (0.5)

    # indique a simcnc que le nouvelle outil est en place ,(tells simcnc that the new tool is in place)
    d.setToolLength (new_tool,new_tool_length)
    d.setToolOffsetNumber(new_tool)
    d.setSpindleToolNumber(new_tool)

    # remonte Le Z a zero apres la prise d'outil (raise the Z to zero after tool pickup.)
    position[Z] = 0
    d.moveToPosition(CoordMode.Machine, position, Z_up_speed)

    # verifie qu'un outil est en place (Check if a tool is in place)
    Read_if_tool_in (check_tool_in_spindel)
    Read_if_tool_in (check_clamp_status)

    # Déplacer l'axes Y en zone sur pour ne pas taper les autres outils (Move the Y axis to a safe zone to avoid hitting other tools.)
    position[Y] = Y_position_safe_zone
    d.moveToPosition(CoordMode.Machine, position, YX_speed)

    print(_("-------------------\n End of tool change \n--------------------"))

    #-----------------------------------------------------------
    #fin des mouvements de changement d'outils (End of tool change movements)
    #-----------------------------------------------------------
else:
    print(_(f"-------------------\n The tool {new_tool} is already in place \n--------------------"))

#-----------------------------------------------------------
# Debut script de mesure ,basé sur l'original de simcnc (Beginning of the measurement script, based on the original from SimCNC)
#-----------------------------------------------------------

if do_i_have_prob == True: #regarde au debut du code si oui ou non la mesure doit etre lancée (Check at the beginning of the code whether or not the measurement should be launched.)
   
   
   # Vérifit si la longueur de l'outil new_tool dans simCNC est 0 (non mesurée) si O execute le code de mesure
   # Verifying if the length of the new_tool in simCNC is 0 (not measured). If it is, execute the measurement code."
    if new_tool_length == 0  or  every_time_get_measure == True :  
        print(_(f"Tool {new_tool} Launching the measurement process ."))
            
        # deplacement en XY safe zone , evite les colision avec les outils rangés
        position[X] = probeStartAbsPos['X_probe']
        position[Y] = Y_position_safe_zone
        d.moveToPosition(CoordMode.Machine, position, YX_speed)

        # deplacement Y au dessus du prob
        position[Y] = probeStartAbsPos['Y_probe']
        d.moveToPosition(CoordMode.Machine, position, YX_speed)

        # desente Z rapide, l'outil ne doit pas toucher le prob encore
        position[Axis.Z.value] = probeStartAbsPos['Z_probe']
        d.moveToPosition(CoordMode.Machine, position, Z_down_fast_speed)

        # un petit coup de soufflette (a quick blow of compressed air) 
        set_digital_output(valve_blower, DIOPinVal.PinSet)
        time.sleep (blowing_time) #temps du soufflage
        set_digital_output(valve_blower, DIOPinVal.PinReset)

        # début de la mesure rapide  (fast prob)
        position[Axis.Z.value] = zEndPosition
        probeResult = d.executeProbing(CoordMode.Machine, position, probeIndex, fastProbeVel)
        if(probeResult == False):
            sys.exit(_("fast probing failed!"))

        # recupère la mesure rapide (save the result fast prob)
        fastProbeFinishPos = d.getProbingPosition(CoordMode.Machine)

        # remonté de Z entre les 2 mesures (Z up for 2 mesur)
        d.moveAxisIncremental(Axis.Z, goUpDist, Z_up_speed)

        # pause entre les deux mesures
        time.sleep(fineProbingDelay)

        # debut de la mesure lente (slow prob)
        probeResult = d.executeProbing(CoordMode.Machine, position, probeIndex, slowProbeVel)
        if(probeResult == False):
            sys.exit(_("slow probing failed!"))

        # récupère la mesure lente (save the slow prob)
        probeFinishPos = d.getProbingPosition(CoordMode.Machine)

        # regararde la différence entre les deux mesures (Look at the difference between the two measurements)
        probeDiff = abs(fastProbeFinishPos[Axis.Z.value] - probeFinishPos[Axis.Z.value])
        print("Fast Probe (axe Z): {:.4f}, Fine Probe (axe Z): {:.4f}".format(fastProbeFinishPos[Axis.Z.value], probeFinishPos[Axis.Z.value]))
        if(probeDiff > fineProbeMaxAllowedDiff and checkFineProbingDiff == True):
            errMsg = "ERROR: dif entre les deux mesures trop grande (diff: {:.3f})".format(probeDiff)
            sys.exit( errMsg)

        # calcule le décalage de l'outil (calculate  tool length)
        new_tool_length = probeFinishPos[Axis.Z.value] - refToolProbePos

        # remonté du Z a O  
        position[Axis.Z.value] = 0
        d.moveToPosition(CoordMode.Machine, position, Z_up_speed)

        # imprime dans la console le décalage de l'outil new tool  (print in chat the result)
        print(_("décalage d'outil({:d}) : {:.4f}".format(new_tool, new_tool_length)))

        # retour dans la zone de soft limite  (back in y safe zone)
        position[Y] = Y_position_safe_zone
        d.moveToPosition(CoordMode.Machine, position, YX_speed)

        #-----------------------------------------------------------
        #fin script probing
        #-----------------------------------------------------------
    else:
        (_(f"-------------------\n Tool {new_tool} already mesured \n--------------------"))     
else:
    print(_("-------------------\n Tool measurement cancelled, no probe installed \n--------------------"))

#rentre dans la zone soft limite (come back in soft limit zone )
position[Y] = Y_position_safe_zone
d.moveToPosition(CoordMode.Machine, position, YX_speed)

#Dust shoe back in place
set_digital_output(valve_dustColect_under, DIOPinVal.PinSet)   
time.sleep(2)
set_digital_output(valve_dustColect_under, DIOPinVal.PinReset)

# Activate soft limits
d.ignoreAllSoftLimits(False)

# Export les infos du nouvel outil dans simcnc (Export the new tool information to SimCNC.)
d.setToolLength (new_tool,new_tool_length)
d.setToolOffsetNumber(new_tool)
d.setSpindleToolNumber(new_tool)