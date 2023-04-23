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