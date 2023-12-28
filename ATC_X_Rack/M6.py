# Disclaimer: The provided code is open-source and free to use, modify, and distribute. 
# The author shall not be held responsible for any injury, damage, or loss resulting from the use of this code.
# By using this code, you agree to assume all responsibility and risk associated with the use of the code.

# Code python pour changer d'outil sur fraise ATC automatiqueement et le mesurer si sa valeur dans la table d'outils est = 0
# (Python code to automatically change the tool on an ATC router and measure it if its value in the tool table is = 0 )

# Change tool script for SIMCNC & Csmio-s 
# Erwan Le Foll 25/11/2023    https://youtube.com/@erwan3953

# Le Homming de ce code ce fait en haut a droit de votre table au valeur home=Y0,X0,Z0. La zone de travail est donc en valeurs negatives.(peux ce modifier)
# (The homing in this code is done in the top right of your table with home values = Y0, X0, Z0. The working area is therefore in negative values. (can be modified)

from ConfigMachine import * #Import le fichier ConfigMachine.py qui doit ce trouver dans le meme répertoir que m6.py (#Import the ConfigMachine.py file which must be in the same directory as m6.py)
import time   # importe le temps pour la fonction time.sleep (import time for the function time.sleep)
import sys    # pour utiliser la fonction sys.exit() (to use the sys.exit() function)


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
            print("problem, There is no tool in the spindle.") #message dans la console
            msg.info ("problem,There is no tool in the spindle.")
            sys.exit(1)  #arrète le programe (stop the program)
    elif input_number == check_clamp_status:  #2eme verification d'entrée
        mod_IP = d.getModule(ModuleType.IP, 0)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:
            print("sensor: Clamp closed")
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinSet:
            print("problem, Clamp is open")
            msg.info("problem, Clamp is open")
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
            print("Problem, The tool remains in the spindle")
            msg.info ("Problem, The tool remains in the spindle")
            sys.exit(1)  #arrète le programe (stop the program)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:
            print("sensor: The tool has been successfully released")
    elif input_number == check_clamp_status:
        mod_IP = d.getModule(ModuleType.IP, 0)
        if mod_IP.getDigitalIO(IOPortDir.InputPort, input_number) == DIOPinVal.PinReset:
            print("Problem,The clamp sensor indicates that the clamp has remained closed.")
            msg.info ("Problem,The clamp sensor indicates that the clamp has remained closed.")
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
        print("------------------\nThe digital output has not been well defined.")

        
#-----------------------------------------------------------
# Function to activate air tool rack UNDER from spindel (use " tool_rack_under() " in your code)
#-----------------------------------------------------------

def tool_rack_under():
    #Call ouput tool rack under
    print("call tool rack under")
    mod_IP.setDigitalIO(ToolRackUnder, DIOPinVal.PinSet)

    time.sleep(2)#time for piston to expend




#-----------------------------------------------------------
# Function to activate air tool rack OUT from spindel
#-----------------------------------------------------------

def tool_rack_out():

    #close the air out Valve of tool rack
    mod_IP.setDigitalIO(ToolRackUnder, DIOPinVal.PinReset)
    time.sleep(0.2)

    #Call ouput  tool rack out
    print("Start removing the tool holder")
    mod_IP.setDigitalIO(ToolRackOut, DIOPinVal.PinSet)

    time.sleep(2) #time for piston to expend

    print("tool rack is out")
    mod_IP.setDigitalIO(ToolRackOut, DIOPinVal.PinReset) #stop output 

############################################################
#Debut de la macro (Macro START)
############################################################

#-----------------------------------------------------------
# Check if there is a tool in the spindle, If "no tool" indicates  tool zero in simcnc.
#-----------------------------------------------------------

mod_IP = d.getModule(ModuleType.IP, 0)
if mod_IP.getDigitalIO(IOPortDir.InputPort, check_tool_in_spindel) == DIOPinVal.PinReset:
    d.setSpindleToolNumber("0")
    print("------------------\n NO TOOL IN SPINDEL.\n------------------")

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

# Get the Y coordinate and name save it as y_coord.
y_coord = position[Y]  


#-----------------------------------------------------------
# Prevent gcode from calling Prob3D
#-----------------------------------------------------------

if threeD_prob is not None and new_tool == threeD_prob:
    print("The tool called in the gcode cannot be the prob3D")
    msg.info("The tool called in the gcode cannot be the prob3D, if no prob3D see configeMachine.py")
    sys.exit(1)  # stop the program
    

#-----------------------------------------------------------
# Stop spindel
#-----------------------------------------------------------

d.setSpindleState(SpindleState.OFF) #Turn off the spindle
start_time_stop_spin = time.time() #starts a timer from stop spindel 

#-----------------------------------------------------------
# Tool rack under spindel
#-----------------------------------------------------------

# Move Z axis up
position[Z] = 0
d.moveToPosition(CoordMode.Machine, position, Z_up_speed)

# checking if Tool rack not gone to hit  the spindel, 
if y_coord > Y_position_safe_zone:
    
    # Making a movement towards the safe zone on the Y-axis
    position[Y] = Y_position_safe_zone
    d.moveToPosition(CoordMode.Machine, position, YX_speed)

# call fonction to move tool rack
tool_rack_under()

#-----------------------------------------------------------
# Get the tool number in the spindle and then return it to its place.
#-----------------------------------------------------------

# If new_tool equals hold_tool or Zero, Skip procedure of storing hold tool
if hold_tool != new_tool and hold_tool != 0: 

    if  hold_tool <= ToolCount:     #Checks if the tool number is between 1 and tool count)
        print(f"------------------\n Storing tool number {hold_tool}\n------------------")
    else:
        msg.inf("------------------\nThe tool called in the G-code does not exist", "Oups")
        sys.exit(1)  # stop code


    # Calculate position X based on tool number
    X_position_hold_tool = X_position_first_tool + ((hold_tool - 1) * X_distance_between_tools)
    print(f"------------------\n Old tool will be stored at the location: {hold_tool}\n------------------")



    #-----------------------------------------------------------
    #beginning of the movements,drop hold_tool
    #-----------------------------------------------------------

    # moving in X and Y in a safe zone to avoid touching the tools
    position[X] = X_position_hold_tool 
    position[Y] = Y_position_safe_zone
    d.moveToPosition(CoordMode.Machine, position, YX_speed)

    # Move Final Z
    position[Z] = Z_position_tools
    d.moveToPosition(CoordMode.Machine, position, Z_down_fast_speed)

    # Calculates the elapsed time since the timer was started and pauses if the configured time_spindle_stop is not elapsed. 
    time_spent = time.time() - start_time_stop_spin
    remaining_time = time_spindle_stop - time_spent
    if remaining_time > 0:
        remaining_time = round(remaining_time, 1) #arrondi a 1 decimale
        print(f"------------------\n {remaining_time}Secondes before next move, spindle still turning!!!\n------------------")
        time.sleep(remaining_time)


    # Move the Y axis to the final location
    position[Y] = Y_position_first_tool
    d.moveToPosition(CoordMode.Machine, position, ZY_final_speed)

    # tool in place ready to be relase

#-----------------------------------------------------------
# LOADING NEW TOOL
#-----------------------------------------------------------

if hold_tool != new_tool: # skip code if holdtool = newtool

    if  new_tool <= ToolCount:
        # Check that the new tool does not exceed toolcount
        new_tool = (new_tool - 1) % ToolCount + 1   
        print(f"------------------\n Loading the new tool. {new_tool}\n------------------")
    else:
        msg.inf("Tool number called to large.", "Oups")
        sys.exit(1)  # Arrête le programme "Stop the program."

    # relaes the tool or opens the clamp if there was no tool)
    set_digital_output(valve_collet, DIOPinVal.PinSet)

    # Pause pour l'ouverture de la pince (Pause for clamp opening)
    time.sleep (0.5)

    # If the start of the script was skipped because of a Zero tool then replace Y
    # sinon pas de mouvement car vous ete deja a cette emplacement
    position[Y] = Y_position_first_tool
    d.moveToPosition(CoordMode.Machine, position, YX_speed)

    # Calculate the X position based on the tool number
    X_position_new_tool = X_position_first_tool + ((new_tool - 1) * X_distance_between_tools)

    # Name the tool Zero in simcnc, In case of emergency stop it is important that simcnc knows that there is no more tool
    d.setToolOffsetNumber(0)

    # Move Z axis up
    position[Z] = 0
    d.moveToPosition(CoordMode.Machine, position, Z_up_speed)

    # Verify that a tool has been properly released
    Read_if_tool_out (check_tool_in_spindel)
    Read_if_tool_out (check_clamp_status)

    # Move X above new tool.)
    position[X] = X_position_new_tool
    d.moveToPosition(CoordMode.Machine, position, YX_speed)

    # Move Z-axis in fast approach.
    position[Z] = Z_position_approach
    d.moveToPosition(CoordMode.Machine, position, Z_down_fast_speed)

    # Cleaning the cone)
    set_digital_output(valve_clean_cone, DIOPinVal.PinSet)

    # Déplacer l'axe Z aproche final lente (Move Z axis to final slow approach.
    position[Z] = Z_position_tools
    d.moveToPosition(CoordMode.Machine, position, ZY_final_speed)

    # Cleaning of the tool taper finished.
    set_digital_output(valve_clean_cone, DIOPinVal.PinReset)

    # Lock the tool
    set_digital_output(valve_collet, DIOPinVal.PinReset)

    #pause
    time.sleep (0.5)

    # Check if a tool is in place)
    Read_if_tool_in (check_tool_in_spindel)
    Read_if_tool_in (check_clamp_status)

    # tells simcnc that the new tool is in place (why here againe? in case of emergecy stop)
    d.setToolLength (new_tool,new_tool_length)
    d.setToolOffsetNumber(new_tool)
    d.setSpindleToolNumber(new_tool)

    # Move the Y axis to a safe zone to avoid hitting other tools.
    position[Y] = Y_position_safe_zone
    d.moveToPosition(CoordMode.Machine, position, ZY_final_speed)
    
    # Raise the Z to zero after tool pickup.
    position[Z] = 0
    d.moveToPosition(CoordMode.Machine, position, Z_up_speed)

    print("-------------------\n End of tool change \n--------------------")

    #-----------------------------------------------------------
    # End of tool change movements
    #-----------------------------------------------------------
else:
    print(f"-------------------\n The tool {new_tool} is already in place \n--------------------")

#-----------------------------------------------------------
# Beginning of the measurement script, based on the original from SimCNC
#-----------------------------------------------------------

if do_i_have_prob == True: # Check at the beginning of the code whether or not the measurement should be launched.
   
   
      # Verifying if the length of the new_tool in simCNC is 0 (not measured). If it is, execute the measurement code."
    if new_tool_length == 0  or  every_time_get_measure == True :  
        print(f"Tool {new_tool} Launching the measurement process .")
            
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

        #  fast prob)
        position[Axis.Z.value] = zEndPosition
        probeResult = d.executeProbing(CoordMode.Machine, position, probeIndex, fastProbeVel)
        if(probeResult == False):
            sys.exi("fast probing failed!")

        #  save the result fast prob)
        fastProbeFinishPos = d.getProbingPosition(CoordMode.Machine)

        #  Z up for 2 mesur)
        d.moveAxisIncremental(Axis.Z, goUpDist, Z_up_speed)

        # pause entre les deux mesures
        time.sleep(fineProbingDelay)

        #  slow prob)
        probeResult = d.executeProbing(CoordMode.Machine, position, probeIndex, slowProbeVel)
        if(probeResult == False):
            sys.exi("slow probing failed!")

        # récupère la mesure lente (save the slow prob)
        probeFinishPos = d.getProbingPosition(CoordMode.Machine)

        # regararde la différence entre les deux mesures (Look at the difference between the two measurements)
        probeDiff = abs(fastProbeFinishPos[Axis.Z.value] - probeFinishPos[Axis.Z.value])
        print("Fast Probe (axe Z): {:.4f}, Fine Probe (axe Z): {:.4f}".format(fastProbeFinishPos[Axis.Z.value], probeFinishPos[Axis.Z.value]))
        if(probeDiff > fineProbeMaxAllowedDiff and checkFineProbingDiff == True):
            errMsg = "ERROR: dif entre les deux mesures trop grande (diff: {:.3f})".format(probeDiff)
            sys.exit( errMsg)

        #  Calculate  tool length)
        new_tool_length = probeFinishPos[Axis.Z.value] - refToolProbePos

        # remonté du Z a O  
        position[Axis.Z.value] = 0
        d.moveToPosition(CoordMode.Machine, position, Z_up_speed)

        #  print in chat the result
        print("décalage d'outil({:d}) : {:.4f}".format(new_tool, new_tool_length))

        #-----------------------------------------------------------
        # fin script probing
        #-----------------------------------------------------------
    else:
        print(f"-------------------\n Tool {new_tool} already measured \n--------------------")    
else:
    print("-------------------\n Tool measurement cancelled, no probe installed \n--------------------")


# call back the air tool rack
tool_rack_out()

#  Export the new tool information to SimCNC. 
d.setToolLength (new_tool,new_tool_length)
d.setToolOffsetNumber(new_tool)
d.setSpindleToolNumber(new_tool)