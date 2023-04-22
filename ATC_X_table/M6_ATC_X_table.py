# Copier/Coller ce code Dans SimCNC> macroEditor> file> open> M6.py 
# Copy/past in SimCNC> macroEditor> file> open> M6.py

# Le fichier Configmachine.py doit etre placer dans le meme répèrtoir que celui ci M6.py




X = 0                               # donne a noms a l'axe quand getposition est utilisé
Y = 1                               
Z = 2                                
A = 3                               
B = 4
C = 5

import time                         # importe le temps pour la fonction time.sleep (import time for the function time.sleep)
import sys                          # pour utiliser la fonction sys.exit() (to use the sys.exit() function)

try:
    import ConfigMachine # Import les variable/infos du fichier ConfigMachine.py 
except ImportError:
    msg.info("File ConfigMachine.py not found. !")
    sys.exit(1) 

#-----------------------------------------------------------
# Importe le tradution du fichier multilingual.py a placer dans le meme répèretoir que M6
#-----------------------------------------------------------
try:
    from multilingual import _
except ModuleNotFoundError:
    print("The multilingual.py file cannot be found. Translations will not be available.")
    
    def _(text):
        return text




#-----------------------------------------------------------
# Fonction regarde si un outil est en place , sinon stop le programe
# Prévu pour contact NO, Inverser PinSet<>PinReset pour les contacts NC
# Read_if_tool_in (check_tool_in_spindel)
# Read_if_tool_in (check_clamp_status)
#-----------------------------------------------------------

def Read_if_tool_in (input_number):
    if input_number == None:  #inogre le code si entrée comfigurée sur None
        return   
    elif input_number == check_tool_in_spindel:
        mod_IP = d.getModule(ModuleType.IP, 0) # apelle le csmio ip-s
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet: #pinset =allumé
            print(_("A tool has been detected in the spindle."))
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset: #pinreset = etaind
            print(_("There is no tool in the spindle.."))
            sys.exit(1)  #arrète le programe
    elif input_number == check_clamp_status:
        mod_IP = d.getModule(ModuleType.IP, 0)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:
            print(_("The clamp is closed."))
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet:
            print(_("The clamp is open."))
            sys.exit(1)   #arrète le programe
            

            
#-----------------------------------------------------------
# Fonction regarde si l'outil a bien été libéré, "délivré" sinon stop le programe, 
# Prévu pour contact NO, Inverser PinSet<>PinReset pour les contacts NC
# Read_if_tool_out (check_tool_in_spindel)
# Read_if_tool_out (check_clamp_status)
#-----------------------------------------------------------


def Read_if_tool_out(input_number):
    if input_number == None: #inogre le code si l'entrée est comfigurée sur 100 
        return   
    elif input_number == check_tool_in_spindel:
        mod_IP = d.getModule(ModuleType.IP, 0)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet:
            print(_("The tool remains in the spindle."))
            sys.exit(1)  #arrète le programe
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:
            print(_("There is no tool in the spindle."))
    elif input_number == check_clamp_status:
        mod_IP = d.getModule(ModuleType.IP, 0)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:
            print(_("The clamp remained closed."))
            sys.exit(1) #arrète le programe
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet:
            print(_("The clamp is open.."))



#-----------------------------------------------------------
# Fonction pour Activer n'importe quelle sorties numériques spécifiée exemple:
# allumé=   set_digital_output(valve_collet, DIOPinVal.PinSet)   
# eteinte=  set_digital_output(valve_collet, DIOPinVal.PinReset)
# remplacer 'valve_collet' pour géré d'autres sortie, voir au debut script)
#-----------------------------------------------------------

def set_digital_output(output_number, value):
    if output_number is None:
        return
    try:
        mod_IP = d.getModule(ModuleType.IP, 0) # pour cismo ipS
        mod_IP.setDigitalIO(output_number, value)
    except NameError:
        print("The digital output has not been well defined.")



############################################################
#Debut de la macro (Macro START)
############################################################

#-----------------------------------------------------------
# Récupérer le numéro de l'outil dans la broche puis le raporte a ca place
# Get the tool number in the spindle and then return it to its place.
#-----------------------------------------------------------

#recupère le numero d'outil sur la broche et le nome hold tool (Get the tool number on the spindle and name it "hold_tool".)
hold_tool = d.getSpindleToolNumber()  
#recupère le numero d'outil du gcode et le nome new tool (Get the tool number from the gcode and name it "new tool".)
new_tool = d.getSelectedToolNumber()
#récupère la taille connu du nouvel outil (Get the known size of the new tool.)
new_tool_length = d.getToolLength(new_tool)
# Récupérer la position de la machine et la nome "position" (Retrieve the machine's position and name it "position".)
position = d.getPosition(CoordMode.Machine)
y_coord = position[Y]  # Récupérer la coordonnée Y et la nome y_coord (Retrieve the Y coordinate and name it y_coord.)

if hold_tool != new_tool: #si new_tool = hold_tool annule le changement d'outil (If new_tool equals hold_tool, cancel the tool change.)

    if 1 <= new_tool <= ToolCount:     #verifi si l'outil est compris entre 1 et tool count (Checks if the tool number is between 1 and tool count)
        print(f"------------------\n Storing tool number {hold_tool}\n------------------")  # \n est un retour a la ligne
    else:
        error_message = "The tool called in the G-code does not exist"
        print(error_message)
        msg.info(error_message, "Oups")
        sys.exit(1)  # Arrête le programme


    # Calculer la position X en fonction du numéro d'outil
    X_position_hold_tool = X_position_first_tool + ((hold_tool - 1) * X_distance_between_tools)
    print(f"------------------\n Old tool va être rangé à l'emplacement: {hold_tool}\n------------------")


    # Récupérer la position de la machine et la nome "position" (Retrieve the machine's position and name it "position".)
    position = d.getPosition(CoordMode.Machine)
    y_coord = position[Y]  # Récupérer la coordonnée Y et la nome y_coord (Retrieve the Y coordinate and name it y_coord.)

    #-----------------------------------------------------------
    # Stop spindel
    #-----------------------------------------------------------

    d.setSpindleState(SpindleState.OFF) #etaint la broche (Turn off the spindle)
    start_time_stop_spin = time.time() #lance un chronometre (starts a timer )

    #-----------------------------------------------------------
    #debut des mouvements (beginning of the movements)
    #-----------------------------------------------------------

    # Déplacer l'axe Z en haut
    position[Z] = 0
    d.moveToPosition(CoordMode.Machine, position, Z_up_speed)

    #supprimer les soft limite
    d.ignoreAllSoftLimits(True)

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

    # calcule le temps écoulé depuis le lancement du chronometre et fait une pause si le temps comfiguré time_spindel_stop n'est pas écoulé 
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
    time.sleep (blowing_time) #temps du soufflage
    set_digital_output(valve_blower, DIOPinVal.PinReset)

    # Déplacer l'axe Z approche finale lente (Moving the Z-axis in slow final approach)
    position[Z] = Z_position_tools
    d.moveToPosition(CoordMode.Machine, position, Z_down_final_speed)

    # Libert l'outil (release the tool)
    set_digital_output(valve_collet, DIOPinVal.PinSet)

    # Pause pour l'ouverture de la pince
    time.sleep (0.5)

    #-----------------------------------------------------------
    # Récupérer le numéro d'outil du g code M6 puis calcule sa position puis mouvements (Retrieve the tool number from the M6 g-code, calculate its position, and perform the corresponding movements)
    #-----------------------------------------------------------

    if 1 <= new_tool <= ToolCount:
        # Si le numéro d'outil est plus grand que ToolCount, utiliser le modulo pour déterminer la position .Permet de configurer plus d'outils que d'emplacement disponible, emexple si toulcount=10  alors loutil 11 sera placer sur l'emplacement 1 ...
        #(If the tool number is greater than ToolCount, use modulo to determine the position. This allows you to configure more tools than available locations. For example, if ToolCount=10, then tool 11 will be placed on location 1...)
        new_tool = (new_tool - 1) % ToolCount + 1   
        print(f"------------------\n Loading the new tool. {new_tool}\n------------------")
    else:
        error_message = "Tool number called too small or too large."
        print(error_message)
        msg.info(error_message, "Oups")
        sys.exit(1)  # Arrête le programme "Stop the program."

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

    #pause
    time.sleep (0.5)

    # verouille l'outil(Lock the tool)
    set_digital_output(valve_collet, DIOPinVal.PinReset)

    # remonte Le Z a zero apres la prise d'outil (raise the Z to zero after tool pickup.)
    position[Z] = 0
    d.moveToPosition(CoordMode.Machine, position, Z_up_speed)

    # verifie qu'un outil est en place (Check if a tool is in place)
    Read_if_tool_in (check_tool_in_spindel)
    Read_if_tool_in (check_clamp_status)

    # Déplacer l'axes Y en zone sur pour ne pas taper les autres outils (Move the Y axis to a safe zone to avoid hitting other tools.)
    position[Y] = Y_position_safe_zone
    d.moveToPosition(CoordMode.Machine, position, YX_speed)

    print("-------------------\n End of tool change \n--------------------")

    #-----------------------------------------------------------
    #fin des mouvements de changement d'outils (End of tool change movements)
    #-----------------------------------------------------------
else:
    print(f"-------------------\n The tool {new_tool} is already in place \n--------------------")

#-----------------------------------------------------------
# Debut script de mesure ,basé sur l'original de simcnc (Beginning of the measurement script, based on the original from SimCNC)
#-----------------------------------------------------------

if do_i_have_prob == True: #regarde au debut du code si oui ou non la mesure doit etre lancée (Check at the beginning of the code whether or not the measurement should be launched.)
   
   
   # Vérifit si la longueur de l'outil new_tool dans simCNC est 0 (non mesurée) si O execute le code de mesure
   # Verifying if the length of the new_tool in simCNC is 0 (not measured). If it is, execute the measurement code."
    if new_tool_length == 0  or  every_time_get_measure == True :  
        print(f"Tool {new_tool} Launching the measurement process .")
            
        # deplacement en XY safe zone , evite les colision avec les outils rangés
        position[X] = probeStartAbsPos['X_probe']
        position[Y] = Y_position_safe_zone
        d.moveToPosition(CoordMode.Machine, position, YX_speed)

        # deplacement Y au dessus de l'outil
        position[Y] = probeStartAbsPos['Y_probe']
        d.moveToPosition(CoordMode.Machine, position, YX_speed)

        # desente Z rapide, l'outil ne doit pas toucher le prob encore
        position[Axis.Z.value] = probeStartAbsPos['Z_probe']
        d.moveToPosition(CoordMode.Machine, position, Z_down_fast_speed)

        # un petit coup de soufflette (a quick blow of compressed air) 
        set_digital_output(valve_blower, DIOPinVal.PinSet)
        time.sleep (blowing_time) #temps du soufflage
        set_digital_output(valve_blower, DIOPinVal.PinReset)

        # début de la mesure rapide
        position[Axis.Z.value] = zEndPosition
        probeResult = d.executeProbing(CoordMode.Machine, position, probeIndex, fastProbeVel)
        if(probeResult == False):
            sys.exit(_("fast probing failed!"))

        # recupère la mesure rapide
        fastProbeFinishPos = d.getProbingPosition(CoordMode.Machine)

        # remonté de Z entre les 2 mesures
        d.moveAxisIncremental(Axis.Z, goUpDist, Z_up_speed)

        # pause entre les deux mesures
        time.sleep(fineProbingDelay)

        # debut de la mesure lente
        probeResult = d.executeProbing(CoordMode.Machine, position, probeIndex, slowProbeVel)
        if(probeResult == False):
            sys.exit(_("slow probing failed!"))

        # récupère la mesure lente
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

        # imprime dans la console le décalage de l'outil new tool
        print(_("décalage d'outil({:d}) : {:.4f}".format(new_tool, new_tool_length)))

        # retour dans la zone de soft limite 
        position[Y] = Y_position_safe_zone
        d.moveToPosition(CoordMode.Machine, position, YX_speed)

        #-----------------------------------------------------------
        #fin script probing
        #-----------------------------------------------------------
    else:
        print(_("-------------------\n Tool {new_tool} already install \n--------------------"))    
else:
    print(_("-------------------\n Tool measurement cancelled, no probe installed \n--------------------"))

#rentre dans la zone soft limite (come back in soft limit zone )
position[Y] = Y_position_safe_zone
d.moveToPosition(CoordMode.Machine, position, YX_speed)

#active les soft limite
d.ignoreAllSoftLimits(False)

# Export les infos du nouvel outil dans simcnc (Export the new tool information to SimCNC.)
d.setToolLength (new_tool,new_tool_length)
d.setToolOffsetNumber(new_tool)
d.setSpindleToolNumber(new_tool)