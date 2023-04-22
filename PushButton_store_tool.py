##################################################################################
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



X = 0                               # donne a noms a l'axe quand getposition est utilisé
Y = 1                               
Z = 2                                
A = 3                               
B = 4
C = 5

import time                         # importe le temps pour la fonction time.sleep (import time for the function time.sleep)
import sys                          # pour utiliser la fonction sys.exit() (to use the sys.exit() function)

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



import tkinter as tk
   

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




    ##################################################################################


def cancel_reset():
    root.destroy()

root = tk.Tk()
root.title("Reset Tool Length")
message = "Are you sure you want to reset all tool lengths?"
label = tk.Label(root, text=message)
label.pack(pady=20)

button_frame = tk.Frame(root)
button_frame.pack()

ok_button = tk.Button(button_frame, text="Reset All", command=reset_tool_length)
ok_button.pack(side=tk.LEFT, padx=10)

cancel_button = tk.Button(button_frame, text="Cancel", command=cancel_reset)
cancel_button.pack(side=tk.LEFT, padx=10)

root.mainloop()
