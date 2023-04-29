# Disclaimer: The provided code is open-source and free to use, modify, and distribute. 
# The author shall not be held responsible for any injury, damage, or loss resulting from the use of this code.
# By using this code, you agree to assume all responsibility and risk associated with the use of the code.

# Code python pour changer d'outil sur fraise ATC automatiqueement et le mesurer si sa valeur dans la table d'outils est = 0
# (Python code to automatically change the tool on an ATC router and measure it if its value in the tool table is = 0 )

# Change tool script for SIMCNC & Csmio-s 
# Erwan Le Foll 23/04/2022    https://youtube.com/@erwan3953

# Le Homming de ce code ce fait en haut a droit de votre table au valeur home=Y0,X0,Z0. La zone de travail est donc en valeurs negatives.(peux ce modifier)
# (The homing in this code is done in the top right of your table with home values = Y0, X0, Z0. The working area is therefore in negative values. (can be modified)

#-----------------------------------------------------------
# INfos sur la machine (Machine informations)
#-----------------------------------------------------------

# vitesses (speed)
Z_down_final_speed = 2000           # Vitesse de Z d'aproche finale lente (slow final approach speed of Z)
Z_down_fast_speed = 5000            # vitesse de Z d'aproche rapide (fast approach speed of Z)
Z_up_speed = 10000                  # viteese de lever du Z (speed to lift Z)
YX_speed = 50000                    # Vitesse de l'axe Y et X (speed of Y and X axis)

#positions
Y_position_first_tool = -60         # position Y du trou (Y position of the hole)
Y_position_safe_zone = -210         # zone ou les outils peuvent circuler sur l'axe X sans toucher les autres porte outils (zone where tools can move on the X axis without touching each other)
X_position_first_tool = -296        # position du premier outil (position of the first tool)
Z_position_tools = -206.5             # emplacement Z ou l'outil est libéré (location where the tool is released)
Z_position_approach = -170          # emplacement Z ou il faut commencer a ralentir et declanche valve_clean_cone ou valve_blower  (location where it is necessary to start slowing down and trigger the air conne cleaner)
X_distance_between_tools = -150     # distance entre les support d'outils sur la table (distance between tool holders)

# numeros d'entrée/sorties 
ToolCount = 11                      # Nombre max. d'outils sur la table premier outil =1 (Maximum number of tools on the table, first tool=1)
check_tool_in_spindel = 24          # Numéro de l'entrée numérique qui gère le détecteur d'outil inséré, None=desactivé (Digital input number managing the tool detection sensor)
check_clamp_status = 25             # Numéro de l'entrée numérique qui gère le détecteur d'ouverture de la griffe du conne , None=desactivé (Digital input number managing the cone clamp open sensor)
valve_collet = 13                   # Numéro de la sortie numérique qui gère la valve pour le changement d'outil (Digital output number managing the valve for tool change)
valve_clean_cone = 15               # Numéro de la sortie numérique qui gère la valve pour le nettoyage du cone du porte outil (Digital output number managing the valve for tool holder cone cleaning)
valve_blower = 12                   # Numéro de la sortie numérique qui gère la valve de la soufflette (Digital output number managing the valve for the blower)
blowing_time = 0.5                  # temps en seconde du coup de soufflette a la dépose d'un outil ou a la mesure (Time in seconds of the blower at the tool drop or measurement).
time_spindle_stop = 8               # temps en seconde  de l'arrete de votre broche avec l'outil le plus lourd (time in seconds for the stop of your spindel with the heaviest tool)

#-----------------------------------------------------------
# Infos sur le Contacteur de palpage (probing infos)
#-----------------------------------------------------------

do_i_have_prob = True               # True = mesure d'outil activée. False = mesure d'outil desactivée ( True = tool measurement enabled. False = tool measurement disabled)
every_time_get_measure = True       # True = mesure a tous les coups, False = mesure que si la table d'outil est a zero (True = measure every time, False = measure only if tool table is at zero)
probeStartAbsPos = {'X_probe': -108, 'Y_probe': -60, 'Z_probe': -80} # Coordonnées de placement au dessus du prob [X_probe, Y_probe, Z_probe] votre outil le plus long doit passer avec ce Z! (Placement coordinates above the probe [X_probe, Y_probe, Z_probe] Your longest tool must pass with this Z!)
probeIndex = 0                      # correspond a l'entrée que vous avez configuré dans les settings de simcnc (settings->Modules->IO Signals  : 0,1,2 ou 3 possible) (corresponds to the input you configured in the simcnc settings)
zEndPosition = -190                 # l'axe z ne descendra pas plus loint! (The Z-axis will not go down any further!)
refToolProbePos = -143.67           # Hauteur a la quelle votre outil de reférénce touche le prob, (si votre outil de référence touche a Z-100mm et que vous indiquez - 100mm ici, alors le décalage enregistré sera de 0mm) (Height at which your reference tool touches the probe (if your reference tool touches at Z-100mm and you indicate - 100mm here, then it will be referenced to 0mm))
fastProbeVel = 700                  # Vitesse de la premiere mesure, rapide (units/min) (Speed of the first, fast measurement (units/min))
slowProbeVel = 250                  # Vitesse du deuxieme mesure, lente (units/min) (Speed of the second, slow measurement (units/min))
goUpDist = 6                        # Remontée en mm de Z entre les deux mesures (Z-axis up travel in mm between the two measurements)
fineProbingDelay = 0.2              # Temps en secondes entre les deux mesures (Time in seconds between the two measurements)
checkFineProbingDiff = False        # Ne pas changer (Do not change)
fineProbeMaxAllowedDiff = 0.1       # Tolerence entre les deux mesures (tolerance between the two measurements)
moveX = True                        # Ne pas changer (Do not change)
moveY = True                        # Ne pas changer (Do not change)

X = 0  # donne un noms a l'axe quand getposition est utilisé
Y = 1  # Plus loint dans le code j'apelle get posision qui me renvoie une posision machine qui si la machine est a zero sera: 0.0.0.0.0.0                             
Z = 2  # ses lignes servent a nommer c'est chifres, le premier zero qui est en position 0 est nomé X le 2eme qui est en position 1 est nomé Y ex..                              
A = 3                               
B = 4
C = 5

import time   # importe le temps pour la fonction time.sleep (import time for the function time.sleep)
import sys    # pour utiliser la fonction sys.exit() (to use the sys.exit() function)

#-----------------------------------------------------------
# Importe le tradution du fichier multilingual.py a placer dans le meme répèretoir que M6
#-----------------------------------------------------------
try:
    from multilingual import _
except ModuleNotFoundError:
    print("The multilingual.py file cannot be found. Traduction pas disponible.")
    
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
#regarde si il y a un outil dans la broche, Si "non" nome l'outil en place dans Simcnc "Zero".
#-----------------------------------------------------------

mod_IP = d.getModule(ModuleType.IP, 0)
if mod_IP.getDigitalIO(IOPortDir.InputPort, check_tool_in_spindel) == DIOPinVal.PinReset:
    d.setSpindleToolNumber("0")
    print(_("------------------\nNO TOOL IN SPINDEL.\n------------------"))
#-----------------------------------------------------------
# Intéroge le Csmio , et nome les valeurs en retour avec des noms
#--------------------------------------------------------------

#recupère le numero d'outil sur la broche et le nome hold tool (Get the tool number on the spindle and name it "hold_tool".)
hold_tool = d.getSpindleToolNumber()  
#recupère le numero d'outil du gcode et le nome new tool (Get the tool number from the gcode and name it "new tool".)
new_tool = d.getSelectedToolNumber()
#récupère la taille connu du nouvel outil (Get the known size of the new tool.)
new_tool_length = d.getToolLength(new_tool)
# Récupérer la position de la machine et la nome "position" (Retrieve the machine's position and name it "position".)
position = d.getPosition(CoordMode.Machine)
y_coord = position[Y]  # Récupérer la coordonnée Y et la nome y_coord (Retrieve the Y coordinate and name it y_coord.)

#-----------------------------------------------------------
# Récupérer le numéro de l'outil dans la broche puis le raporte a ca place
# Get the tool number in the spindle and then return it to its place.
#-----------------------------------------------------------

if hold_tool != new_tool and hold_tool != 0: #si new_tool = hold_tool annule le changement d'outil (If new_tool equals hold_tool, cancel the tool change.)

    if  new_tool <= ToolCount:     #verifi si l'outil est compris entre 1 et tool count (Checks if the tool number is between 1 and tool count)
        print(_(f"------------------\n Storing tool number {hold_tool}\n------------------"))  # \n est un retour a la ligne
    else:
        msg.info(_("------------------\nThe tool called in the G-code does not exist", "Oups"))
        sys.exit(1)  # Arrête le programme


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



    #-----------------------------------------------------------
    # Récupérer le numéro d'outil du g code M6 puis calcule sa position puis mouvements (Retrieve the tool number from the M6 g-code, calculate its position, and perform the corresponding movements)
    #-----------------------------------------------------------
if hold_tool != new_tool:

    if  new_tool <= ToolCount:
        # Si le numéro d'outil est plus grand que ToolCount, utiliser le modulo pour déterminer la position .Permet de configurer plus d'outils que d'emplacement disponible, emexple si toulcount=10  alors loutil 11 sera placer sur l'emplacement 1 ...
        #(If the tool number is greater than ToolCount, use modulo to determine the position. This allows you to configure more tools than available locations. For example, if ToolCount=10, then tool 11 will be placed on location 1...)
        new_tool = (new_tool - 1) % ToolCount + 1   
        print(_(f"------------------\n Loading the new tool. {new_tool}\n------------------"))
    else:
        msg.info(_("Tool number called to large.", "Oups"))
        sys.exit(1)  # Arrête le programme "Stop the program."

    # Libert l'outil ou ouvre la pince si il n'y avait pas d'outil (release the tool)
    set_digital_output(valve_collet, DIOPinVal.PinSet)

    # indique a simcnc que plus d'outil en place avec l'outil Zero.
    d.setToolOffsetNumber(0)

    # Pause pour l'ouverture de la pince
    time.sleep (0.5)

    # Si le debut du script a été passé a cose d'un outil Zero alors  replace Y
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

    #pause
    time.sleep (0.5)

    # verouille l'outil(Lock the tool)
    set_digital_output(valve_collet, DIOPinVal.PinReset)

    # indique a simcnc que le nouvelle outil est en place
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