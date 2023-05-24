
import sys
import time
from ConfigMachine import *


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


#recupère le numero d'outil sur la broche et le nome hold tool (Get the tool number on the spindle and name it "hold_tool".)
current_tool = d.getSpindleToolNumber()  

# Récupérer la position de la machine et la nome "position" (Retrieve the machine's position and name it "position".)
position = d.getPosition(CoordMode.Machine)

#supprimer les soft limite
d.ignoreAllSoftLimits(True)

#-----------------------------------------------------------
#regarde si il y a un outil dans la broche, Si "non" indique dans Simcnc outil "Zero".
#-----------------------------------------------------------

mod_IP = d.getModule(ModuleType.IP, 0)

if mod_IP.getDigitalIO(IOPortDir.InputPort, check_tool_in_spindel) == DIOPinVal.PinReset:
    d.setSpindleToolNumber("0")
    print(_("------------------\nNO TOOL IN SPINDEL.\n------------------"))
    msg.info("NO TOOL IN SPINDEL", "Info")  #error message
    sys.exit(1) # stop the programe

#-----------------------------------------------------------
#Start moving
#-----------------------------------------------------------

print(_(f"------------------\n Tool {current_tool} Launching the measurement process .\n------------------"))
    
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

# start speed mesurement
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

# Export les infos du nouvel outil dans simcnc (Export the new tool information to SimCNC.)
d.setToolLength (current_tool,new_tool_length)
d.setToolOffsetNumber(current_tool)
d.setSpindleToolNumber(current_tool)

# remonté du Z a O
position[Axis.Z.value] = 0
d.moveToPosition(CoordMode.Machine, position, Z_up_speed)

# imprime dans la console le décalage de l'outil new tool
print(_("décalage d'outil({:d}) : {:.4f}".format(current_tool, new_tool_length)))

# retour dans la zone de soft limite 
position[Y] = Y_position_safe_zone
d.moveToPosition(CoordMode.Machine, position, YX_speed)

#-----------------------------------------------------------
#fin script probing
#-----------------------------------------------------------


#active les soft limite
d.ignoreAllSoftLimits(False)


