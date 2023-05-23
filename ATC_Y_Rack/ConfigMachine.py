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

# infos
ToolCount = 5                      # Nombre max. d'outils sur la table premier outil =1 (Maximum number of tools on the table, first tool=1)

# vitesses (speed)
Z_down_final_speed = 1000           # slow final approach speed of Z
Z_down_fast_speed = 1500            # fast approach speed of Z
Z_up_speed = 2000                   # speed to lift up Z
YX_speed = 3000                     # speed of Y and X axis

# positions
Y_position_first_tool = 90          # Y position of the hole
X_position_safe_zone = 80           # zone where tools can move on the Y axis without touching each other 
X_position_first_tool = 90          # position of the first tool
Z_position_tools = -110             # location where the tool is released
Z_position_approach = -80           # location where it is necessary to start slowing down and trigger the air conne cleaner
X_distance_between_tools = -100     # distance between each tool holders

# numeros d'entrée/sorties  (put None =not use)
check_tool_in_spindel = 24          # Digital input number managing the tool detection sensor
check_clamp_status = 25             # Digital input number managing the cone clamp open sensor
valve_collet = 13                   # Digital output number managing the valve for tool change
valve_clean_cone = 14               # Digital output number managing the valve for tool holder cone cleaning
valve_dustColect_out = None         # Remove dust shoe
valve_dustColect_under = None       # put the dust shoe ready to suck
valve_blower = None                 # Digital output number managing the valve for the blower

# time
blowing_time = 0.5                  # Time in seconds of the blower at the tool drop or measurement
time_spindle_stop = 8               # time in seconds for the stop of your spindel with the heaviest tool

#-----------------------------------------------------------
# Infos sur le Contacteur de palpage (probing infos)
#-----------------------------------------------------------

do_i_have_prob = True               # True = mesure d'outil activée. False = mesure d'outil desactivée ( True = tool measurement enabled. False = tool measurement disabled)
every_time_get_measure = True       # True = mesure a tous les coups, False = mesure que si la table d'outil est a zero (True = measure every time, False = measure only if tool table is at zero)
probeStartAbsPos = {'X_probe': 10, 'Y_probe': 90, 'Z_probe': -80} # Coordonnées de placement au dessus du prob [X_probe, Y_probe, Z_probe] votre outil le plus long doit passer avec ce Z! (Placement coordinates above the probe [X_probe, Y_probe, Z_probe] Your longest tool must pass with this Z!)
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


#-----------------------------------------------------------
# Donne un noms a l'axe quand getposition est utilisé.
# "d.getPosition(CoordMode.Machine)"  renvoie une posision machine qui si la machine est a zero sera: 0.0.0.0.0.0                             
# Ses lignes de code servent a nommer chaque chiffre retrounés de la sorte X.Y.Z.A.B.C, ici le premier zero qui est en position 0 est nomé X le 2eme qui est en position 1 est nomé Y ex..                              
# Si votre ligne/chargeur d'outils est sur Y et non X comme moi, alors vous pouvez soit remplacer tous les X dans le code m6.py par des Y, soit ici nomer X=1 Y=0 (astuce que je n'ai pas testé)
#-----------------------------------------------------------

X = 0
Y = 1
Z = 2
A = 3
C = 5