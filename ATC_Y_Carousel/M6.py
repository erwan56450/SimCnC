# Disclaimer: The provided code is open-source and free to use, modify, and distribute. 
# The author shall not be held responsible for any injury, damage, or loss resulting from the use of this code.
# By using this code, you agree to assume all responsibility and risk associated with the use of the code.

# Change tool script for SIMCNC & Csmio-s 
# Erwan Le Foll 24/05/2022   version 1.2   https://youtube.com/@erwan3953

# Script de changement d'outil automatique pour un chargeur d'outil avec TOURNIQUET
# ici le moteur du tourniquet est sur l'axe C en degrés (ou Lineair mm.) pour les Axes en degré comfigurer> axes> C> RotaryType (1->360) permet de prendre le chemain le plus court

# watch out! the tool sensor of this spindle needs to turn to verify that a tool is in place
# https://www.usinages.com/threads/projet-de-retrofit-complet-dune-cnc-axyz.162287/

from ConfigMachine import * #Import le fichier ConfigMachine.py qui doit ce trouver dans le meme répertoir que m6.py (#Import the ConfigMachine.py file which must be in the same directory as m6.py)
import time   # importe le temps pour la fonction time.sleep (import time for the function time.sleep)
import sys    # pour utiliser la fonction sys.exit() (to use the sys.exit() function)

#-----------------------------------------------------------
# Fonction regarde si un outil est en place , sinon stop le programe
# Copier/Coller les 2 phrases si dessous a l'endroit souhaité dans le code a partir de #Debut de la macro
# Read_if_tool_in (check_tool_in_spindel)
# Read_if_tool_in (check_clamp_status)
#-----------------------------------------------------------

def Read_if_tool_in (input_number):
    if input_number == None:  #inogre le code si l'entrée est comfigurée sur None
        return   
    elif input_number == check_tool_in_spindel:  #indique le numero de l'entrée a controler comfiguré au debut du code
        mod_IP = d.getModule(ModuleType.IP, 0) # apelle le csmio ip-s
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet: #pinset =allumé
            print("Un outil a été détecté dans la broche.") #message dans la console
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset: #pinreset = éteint
            print("Il n'y a pas d'outil dans la broche.") #message dans la console
            msg.info ("Il n'y a pas d'outil dans la broche.")
            sys.exit(1)  #arrète le programe
    elif input_number == check_clamp_status:  #2eme verification d'entrée
        mod_IP = d.getModule(ModuleType.IP, 0)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:
            print("La pince est fermé")
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet:
            print("La pince est ouvert")
            msg.info("La pince est ouvert")
            sys.exit(1)   #arrète le programe
            

            
#-----------------------------------------------------------
# Fonction regarde si l'outil a bien été libéré, "délivré" sinon stop le programe
# Copier/Coller les 2 phrases si dessous a l'endroit souhaité dans le code
# Read_if_tool_out (check_tool_in_spindel)     
# Read_if_tool_out (check_clamp_status)
#-----------------------------------------------------------


def Read_if_tool_out(input_number):
    if input_number == None: #inogre le code si l'entrée est comfigurée sur None 
        return   
    elif input_number == check_tool_in_spindel:
        mod_IP = d.getModule(ModuleType.IP, 0)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet:
            print("L'outil est reste dans la broche")
            msg.info ("L'outil est reste dans la broche")
            sys.exit(1)  #arrète le programe
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:
            print("il n'y a pas d'outil dans la broche")
    elif input_number == check_clamp_status:
        mod_IP = d.getModule(ModuleType.IP, 0)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:
            print("La pince est resté fermé")
            msg.info ("La pince est resté fermé")
            sys.exit(1) #arrète le programe
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet:
            print("La pince est ouverte.")



#-----------------------------------------------------------
# Fonction pour Activer n'importe quelle sorties numériques spécifiée.
# Copier/Coller une des phrases si dessous a l'endroit souhaité dans le code
# allumé =   set_digital_output(valve_collet, DIOPinVal.PinSet)   
# eteinte =  set_digital_output(valve_collet, DIOPinVal.PinReset)
# remplacer 'valve_collet' dans les phrase si dessus pour géré d'autres sortie, voir au debut script)
#-----------------------------------------------------------

def set_digital_output(output_number, value):
    if output_number is None:
        return
    try:
        mod_IP = d.getModule(ModuleType.IP, 0) # pour cismo ipS
        mod_IP.setDigitalIO(output_number, value)
    except NameError:
        msg.info("la sortie numerique na pas été bien definit")


############################################################
#Debut de la macro (Macro START)
############################################################

#-----------------------------------------------------------
# Intéroge le Csmio , et nome les valeurs en retour avec des noms
#--------------------------------------------------------------
#recupère le numero d'outil sur la broche et le nome hold tool
hold_tool = d.getSpindleToolNumber()  
#recupère le numero d'outil du gcode et le nome new tool
new_tool = d.getSelectedToolNumber()
#récupère la taille connu du nouvel outil
new_tool_length = d.getToolLength(new_tool)
#récupère la position machine 
position = d.getPosition(CoordMode.Machine)
# Récupérer la coordonnée Y et la sauvegarde sous le noms de Y_coord pour qu'a la fin du script Y retourne a cette endroit
Y_coord = position[Y] 
#supprimer les soft limite
d.ignoreAllSoftLimits(True)

#-----------------------------------------------------------
#regarde si il y a un outil dans la broche, Si "pas d'outil" indique outil Zero dans simcnc.
#-----------------------------------------------------------

# Déplacer l'axe Z en position zero
position[Z] = 0
d.moveToPosition(CoordMode.Machine, position, Z_speed_up)
#Petit démarage de broche (pour un capteur capritieux )
d.executeGCode( "M3 S5000" )
time.sleep(1)
d.setSpindleState( SpindleState.OFF )
time.sleep(2)

mod_IP = d.getModule(ModuleType.IP, 0)
if mod_IP.getDigitalIO(IOPortDir.InputPort, check_tool_in_spindel) == DIOPinVal.PinReset:
    d.setSpindleToolNumber("0") #nome l'outil 0 dans simcnc
    print("------------------\nPas d'outil detecté dans la fraise.\n------------------")

#recupère le numero d'outil sur la broche et le nome hold tool
hold_tool = d.getSpindleToolNumber()


#-----------------------------------------------------------
# Stop spindel
#-----------------------------------------------------------

d.setSpindleState(SpindleState.OFF) #etaint la broche 
start_time_stop_spin = time.time() #lance un chronometre (starts a timer)

# releve le colecteur de poussière si l'entré est définit
set_digital_output(valve_dust_colector, DIOPinVal.PinSet)

# ouvre la porte du tourniquet
set_digital_output(valve_dor, DIOPinVal.PinSet)

#-----------------------------------------------------------
#mouvements
#-----------------------------------------------------------

if hold_tool != new_tool and hold_tool != 0: #Si hold_tool n'est pas égale a new_tool ni zero execute les ligne suivantes
    #-----------------------------------------------------------
    #Mouvement du tourniquet sur hold_tool
    #-----------------------------------------------------------

    if hold_tool <= Tool_Count: #vérifi que l'outil n'est pas plus grand que tool_count
        hold_tool_position_C = ((C_position_last_tool - C_position_first_tool) / (Tool_Count - 1) * (hold_tool-1)) + C_position_first_tool #calcul de l'écatement etre chaques rangement.
        print(f"hold tool va etre ranger a la posistion : {hold_tool}")
    else:
        print(f"Le numéro de l'outil actuel ({hold_tool}) dépasse le nombre maximal d'outils autorisé ({Tool_Count})")
        sys.exit(1)
        

    #mouvement C en position d'outil hold_tool 
    position[C] = hold_tool_position_C
    d.moveToPosition(CoordMode.Machine, position, C_speed)

    #-----------------------------------------------------------
    #debut des mouvements portique
    #-----------------------------------------------------------

    # Déplacer l'axe Z en haut
    position[Z] = 0
    d.moveToPosition(CoordMode.Machine, position, Z_speed_up)

    # déplacement Y avant le tourniquet
    position[Y] = Y_approch
    d.moveToPosition(CoordMode.Machine, position, Y_speed)

    # calcule le temps écoulé depuis le lancement du chronometre et fait une pause si le temps comfiguré time_spindel_stop n'est pas écoulé (Calculates the elapsed time since the timer was started and pauses if the configured time_spindle_stop is not elapsed.)
    time_spent = time.time() - start_time_stop_spin
    remaining_time = time_spindle_stop - time_spent
    if remaining_time > 0: 
        time.sleep(remaining_time)

    # Decend Z a hauteur des outils
    position[Z] = Z_position_tools
    d.moveToPosition(CoordMode.Machine, position, Z_speed_down)

if hold_tool == 0:  #si hold_tool = 0, execute les lignes suivante
    
    # Déplacer l'axe Z en haut seulement si hold_tool = 0  
    position[Z] = 0
    d.moveToPosition(CoordMode.Machine, position, Z_speed_up)

if hold_tool != new_tool:  #si hold_tool n'est pas egale a hold_tool  execute les lignes suivante

    # déplacement Y  dans la pince Ou au dessus si Hold_tool = 0
    position[Y] = Y_tool_clamp
    d.moveToPosition(CoordMode.Machine, position, Y_speed_final) 

if hold_tool != new_tool and hold_tool != 0: #Si hold_tool n'est pas égale a new_tool ou zero execute les lignes suivantes

    # Libert l'outil OU ouvre la pince si outil Zero
    set_digital_output(valve_collet, DIOPinVal.PinSet)

    # indique a simcnc que le nouvelle outil Zero est en place
    d.setSpindleToolNumber('0')

    # Pause pour l'ouverture de la pince
    time.sleep (0.5)

    #vérifit que la pince est ouverte
    Read_if_tool_out (check_clamp_status)

    # Remonte Z a zero
    position[Z] = 0
    d.moveToPosition(CoordMode.Machine, position, Z_speed_up)

    # referme la pince
    set_digital_output(valve_collet, DIOPinVal.PinReset)
    time.sleep (0.5)

if hold_tool != new_tool:  #si hold_tool n'est pas egale a hold_tool execute les lignes suivante

    #Petit démarage de broche (pour un capteur capritieux sur notre broche)
    d.executeGCode( "M3 S5000" )
    time.sleep(1)
    d.setSpindleState( SpindleState.OFF )
    time.sleep(2)
    
    #verifi qu'il n'y a pas ou plus d'outils dans la broche
    Read_if_tool_out (check_tool_in_spindel)  


    #-----------------------------------------------------------
    #Mouvement du tourniquet sur new_tool
    #-----------------------------------------------------------

    

    if new_tool <= Tool_Count: #vérifi que new_tool n'est pas plus grand que tool_count
        New_tool_position_C = ((C_position_last_tool - C_position_first_tool) / (Tool_Count - 1) * (new_tool - 1)) + C_position_first_tool #calcul de l'écatement etre chaques rangement.
        print(f"récupération de l'outil : {new_tool}")
    else:
        print(f"Le numéro de l'outil new tool  ({new_tool}) dépasse le nombre maximal d'outils autorisé ({Tool_Count})")
        sys.exit(1)
        

    #mouvement C en position d'outil new_tool 
    position[C] = New_tool_position_C
    d.moveToPosition(CoordMode.Machine, position, C_speed)

    #-----------------------------------------------------------
    #mouvement pour aller chercher new tool 
    #-----------------------------------------------------------
    
    # ouvre la pince
    set_digital_output(valve_collet, DIOPinVal.PinSet)

    # descend  Z  pour un nettoyage
    position[Z] = Z_position_clean
    d.moveToPosition(CoordMode.Machine, position, Z_speed_down)

    # ouverture valve nettoyage du cone (Cleaning the cone)
    set_digital_output(valve_clean_cone, DIOPinVal.PinSet)

    # descend  Z sur new tool 
    position[Z] = Z_position_tools
    d.moveToPosition(CoordMode.Machine, position, Z_speed_down)

    # fin du nettoyage de cone
    set_digital_output(valve_clean_cone, DIOPinVal.PinReset)

    # Ferme la pince de la broche
    set_digital_output(valve_collet, DIOPinVal.PinReset)

    # indique a simcnc que le nouvelle outil est en place
    d.setToolOffsetNumber(new_tool)
    d.setToolLength (new_tool,new_tool_length)
    d.setToolOffsetNumber(new_tool)


    # Y sort de la pince du tourniquet
    position[Y] = Y_approch
    d.moveToPosition(CoordMode.Machine, position, Y_speed_final)

    # Déplacer l'axe Z en zero
    position[Z] = 0
    d.moveToPosition(CoordMode.Machine, position, Z_speed_up)

    #Petit démarage de broche (pour un capteur capritieux sur notre broche)
    d.executeGCode( "M3 S5000" )
    time.sleep(1)
    d.setSpindleState( SpindleState.OFF )
    time.sleep(2)

    #Verifit si outil dans la broche
    Read_if_tool_in (check_tool_in_spindel)
    #Verifit si la pince est fermé
    Read_if_tool_in (check_clamp_status)

    #imprime dans la console
    print("-------------------\n fin du changement d'outil \n--------------------")

    #-----------------------------------------------------------
    # Fin des mouvements de changement d'outils
    #-----------------------------------------------------------
else:
    print(f"-------------------\n L'outil {new_tool} est deja en place \n--------------------")



##################################################################################################################################
# Debut script de mesure ,basé sur l'original de simcnc (Beginning of the measurement script, based on the original from SimCNC)
##################################################################################################################################


#regarde au debut du code si oui ou non la mesure doit etre lancée (exemple :si vous n'avez pas de palpeur)
if do_i_have_prob == True: 
   
    if new_tool_length == 0 or every_time_get_measure == True:  # Vérifit si la longueur de l'outil new_tool dans simCNC est = 0 (non mesurée) ou Si la mesure doit etre effectuer a chaques fois.
        print(f"L'outil {new_tool} va etre mesuré.")

        # deplacement en Y au dessus du palpeur
        position[Y] = probeStartAbsPos['Y_probe']
        d.moveToPosition(CoordMode.Machine, position, Y_speed)

        # desente Z rapide, l'outil ne doit pas toucher le prob encore
        position[Axis.Z.value] = probeStartAbsPos['Z_probe']
        d.moveToPosition(CoordMode.Machine, position, Z_speed_down)

        # un petit coup de soufflette (a quick blow of compressed air) 
        set_digital_output(valve_blower, DIOPinVal.PinSet)
        time.sleep (blowing_time) #temps du soufflage définit au debut du script
        set_digital_output(valve_blower, DIOPinVal.PinReset)

        # début de la mesure rapide
        position[Axis.Z.value] = zEndPosition
        probeResult = d.executeProbing(CoordMode.Machine, position, probeIndex, fastProbeVel)
        if(probeResult == False):
            sys.exit("fast probing failed!")

        # recupère la mesure rapide
        fastProbeFinishPos = d.getProbingPosition(CoordMode.Machine)

        # remonté de Z entre les 2 mesures
        d.moveAxisIncremental(Axis.Z, goUpDist, Z_speed_up)

        # pause entre les deux mesures
        time.sleep(fineProbingDelay)

        # debut de la mesure lente
        probeResult = d.executeProbing(CoordMode.Machine, position, probeIndex, slowProbeVel)
        if(probeResult == False):
            sys.exit("slow probing failed!")

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
        d.moveToPosition(CoordMode.Machine, position, Z_speed_up)

        # imprime dans la console le décalage de l'outil new tool
        print("décalage d'outil({:d}) : {:.4f}".format(new_tool, new_tool_length))

        #-----------------------------------------------------------
        #fin script probing
        #-----------------------------------------------------------
    else:
        print(f"-------------------\n outil {new_tool} deja mesuré \n--------------------")     
else:
    print("-------------------\n Mesure d'outil annulée, pas de palpeur instalé\n--------------------") 




# Export les infos du nouvel outil dans simcnc    
d.setToolLength (new_tool,new_tool_length)
d.setToolOffsetNumber(new_tool)
d.setSpindleToolNumber(new_tool)

# dégagement du tourniquet ou du palpeur a la position X enregistré au debut du script
position[Y] = Y_coord
d.moveToPosition(CoordMode.Machine, position, Y_speed)

# active les soft limite
d.ignoreAllSoftLimits(False)

# stop la valve pour le cache poussière
set_digital_output(valve_dust_colector, DIOPinVal.PinReset)
#stop la valve pour la porte tourniquet
set_digital_output(valve_dor, DIOPinVal.PinReset)