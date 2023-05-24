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
# Fonction regarde si un outil est en place , sinon stop le programe
# C'est contacts sont prévue pour ma fraise et probablement pas la votre
# Insérer ses 2 lignes dans le code a partir de "debut du script" pour lancer cette fonction
# Read_if_tool_in (check_tool_in_spindel)
# Read_if_tool_in (check_clamp_status)
#-----------------------------------------------------------

def Read_if_tool_in (input_number):
    if input_number == None:  #inogre le code si entrée comfigurée sur None
        return   
    elif input_number == check_tool_in_spindel:
        mod_IP = d.getModule(ModuleType.IP, 0) # apelle le csmio ip-s
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet: #pinset =allumé
            print(_("------------------\nA tool has been detected in the spindle."))
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset: #pinreset = etaind
            print(_("------------------\nThere is no tool in the spindle.."))
            sys.exit(1)  #arrète le programe
    elif input_number == check_clamp_status:
        mod_IP = d.getModule(ModuleType.IP, 0)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:
            print(_("------------------\nThe clamp is closed."))
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet:
            print(_("------------------\nThe clamp is open."))
            sys.exit(1)   #arrète le programe
            

            
#-----------------------------------------------------------
# Fonction regarde si l'outil a bien été libéré, "délivré" sinon stop le programe, 
# C'est contacts sont prévue pour ma fraise et probablement pas la votre
# Insérer ses 2 lignes dans le code a partir de "debut du script" pour lancer cette fonction
# Read_if_tool_out (check_tool_in_spindel)
# Read_if_tool_out (check_clamp_status)
#-----------------------------------------------------------


def Read_if_tool_out(input_number):
    if input_number == None: #inogre le code si l'entrée est comfigurée sur 100 
        return   
    elif input_number == check_tool_in_spindel:
        mod_IP = d.getModule(ModuleType.IP, 0)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet:
            print(_("------------------\nThe tool remains in the spindle."))
            sys.exit(1)  #arrète le programe
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:
            print(_("------------------\nThere is no tool in the spindle."))
    elif input_number == check_clamp_status:
        mod_IP = d.getModule(ModuleType.IP, 0)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:
            print(_("------------------\nThe clamp remained closed."))
            sys.exit(1) #arrète le programe
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet:
            print(_("------------------\nThe clamp is open.."))



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
        print(_("------------------\nThe digital output has not been well defined."))



############################################################
#Debut de la macro (Macro START)
############################################################

#-----------------------------------------------------------
#regarde si il y a un outil dans la broche, Si "pas d'outil" indique outil Zero dans simcnc.
#-----------------------------------------------------------

mod_IP = d.getModule(ModuleType.IP, 0)
if mod_IP.getDigitalIO(IOPortDir.InputPort, check_tool_in_spindel) == DIOPinVal.PinReset:
    d.setSpindleToolNumber("0")
    print(_("------------------\nNO TOOL IN SPINDEL.\n------------------"))

#-----------------------------------------------------------
# Intéroge le Csmio , et nome les valeurs en retour avec des noms
#--------------------------------------------------------------

# Récupérer la position de la machine et la nome "position" (Retrieve the machine's position and name it "position".)
position = d.getPosition(CoordMode.Machine)

# Récupérer la coordonnée Y et la nome y_coord (Retrieve the Y coordinate and name it y_coord.)
y_coord = position[Y]  

#récupère la taille connu du nouvel outil
ThreeD_prob_length = d.getToolLength(threeD_prob)

#supprimer les soft limite
d.ignoreAllSoftLimits(True)

#recupère le numero d'outil sur la broche et le nome hold tool (Get the tool number on the spindle and name it "hold_tool".)
hold_tool = d.getSpindleToolNumber()




if hold_tool > ToolCount and threeD_prob > ToolCount:  # Vérifie si le numéro d'outil est entre 1 et ToolCount
    msg.info(_("------------------\n Emplacement du prob ou numero hold_tool trop grand", "Oups"))
    print(_("------------------\n Emplacement du prob ou numero hold_tool trop grand"))
    sys.exit(1)  # Arrête le programme


#-----------------------------------------------------------
# Récupérer le numéro de l'outil dans la broche puis le raporte a ca place
# Get the tool number in the spindle and then return it to its place.
#-----------------------------------------------------------


#If hold_tool is not equal to zero or if the 3D probe is not already in place, execute the curent tool storage.
if hold_tool != 0 and hold_tool != threeD_prob:
    


    # Calculer la position X en fonction du numéro d'outil
    X_position_hold_tool = X_position_first_tool + ((hold_tool - 1) * X_distance_between_tools)
    print(_(f"------------------\n Old tool va être rangé à l'emplacement: {hold_tool}\n------------------"))


    # Récupérer la position de la machine et la nome "position" (Retrieve the machine's position and name it "position".)
    position = d.getPosition(CoordMode.Machine)
    y_coord = position[Y]  # Récupérer la coordonnée Y et la nome y_coord (Retrieve the Y coordinate and name it y_coord.)

    #-----------------------------------------------------------
    # Stop spindel
    #-----------------------------------------------------------

    d.setSpindleState(SpindleState.OFF) #etaint la broche (Turn off the spindle)
    start_time_stop_spin = time.time() #lance un chronometre (starts a timer )

    #-----------------------------------------------------------
    #debut des mouvements , depose de hold_tool (beginning of the movements)
    #-----------------------------------------------------------

    # Déplacer l'axe Z en haut
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
    time.sleep (blowing_time) #temps du soufflage
    set_digital_output(valve_blower, DIOPinVal.PinReset)

    # Déplacer l'axe Z approche finale lente (Moving the Z-axis in slow final approach)
    position[Z] = Z_position_tools
    d.moveToPosition(CoordMode.Machine, position, Z_down_final_speed)

    #-----------------------------------------------------------
    # Charge de Prob3D
    #-----------------------------------------------------------

if hold_tool != threeD_prob:

    # Libert l'outil ou ouvre la pince si il n'y avait pas d'outil (release the tool)
    set_digital_output(valve_collet, DIOPinVal.PinSet)

    # Nome l'outil Zero dans simcnc
    d.setToolOffsetNumber(0)

    # Pause pour l'ouverture de la pince
    time.sleep (0.5)

    # Si le debut du script a été passé a cose d'un outil Zero alors  replace Y
    position[Y] = Y_position_first_tool
    d.moveToPosition(CoordMode.Machine, position, YX_speed)

    # Calculer la position X en fonction du numéro d'outil (Calculate the X position based on the tool number)
    X_position_treeD_prob = X_position_first_tool + ((threeD_prob - 1) * X_distance_between_tools)

    # remonte Le Z a zero "Raise Z to zero."
    position[Z] = 0
    d.moveToPosition(CoordMode.Machine, position, Z_up_speed)

    #verifie qu'un outil a bien été libéré (Verify that a tool has been properly released)
    Read_if_tool_out (check_tool_in_spindel)
    Read_if_tool_out (check_clamp_status)

    # Déplacer X au dessus de new tool (Move X above new tool.)
    position[X] = X_position_treeD_prob
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
    time.sleep (0.3)

    # indique a simcnc que le nouvelle outil est en place, ses lignes de code sont la si vous stoper le programe en route
    d.setToolLength (threeD_prob,ThreeD_prob_length)
    d.setToolOffsetNumber(threeD_prob)
    d.setSpindleToolNumber(threeD_prob)

    # remonte Le Z a zero apres la prise d'outil (raise the Z to zero after tool pickup.)
    position[Z] = 0
    d.moveToPosition(CoordMode.Machine, position, Z_up_speed)

    # verifie qu'un outil est en place (Check if a tool is in place)
    Read_if_tool_in (check_tool_in_spindel)
    Read_if_tool_in (check_clamp_status)

    # Déplacer l'axes Y en zone sur pour ne pas taper les autres outils (Move the Y axis to a safe zone to avoid hitting other tools.)
    position[Y] = Y_position_safe_zone
    d.moveToPosition(CoordMode.Machine, position, YX_speed)

    print(_("-------------------\n he 3d prob in place \n--------------------"))

    #-----------------------------------------------------------
    #fin des mouvements de changement d'outils (End of tool change movements)
    #-----------------------------------------------------------
else:
    print(_("-------------------\n The 3d prob already in place \n--------------------"))



####################################################################
#Début de la mesure 3d
####################################################################

# remonte Le Z a zero 
position[Z] = 0
d.moveToPosition(CoordMode.Machine, position, Z_up_speed)


if wake_up_prob == True:
    #Petit démarage de broche pour reveiller le 3dprob (https://vers.ge/en/)
    print(_("-------------------\n WAKE UP 3D PROB \n--------------------"))
    d.executeGCode( "M3 S3000" )
    time.sleep(wake_up_time)
    d.setSpindleState( SpindleState.OFF )
    time.sleep(wake_up_time)

# Récupérer la position .Program et la nome "position_prog" (Retrieve the Program position and name it "position_prog".)
position_prog = d.getPosition(CoordMode.Program)

#moving to the Y=0 X=0 
position[Y] = 0
position[X] = 0
d.moveToPosition(CoordMode.Program, position, YX_speed)

