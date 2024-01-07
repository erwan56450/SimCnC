# Disclaimer: The provided code is open-source and free to use, modify, and distribute. 
# The author shall not be held responsible for any injury, damage, or loss resulting from the use of this code.
# By using this code, you agree to assume all responsibility and risk associated with the use of the code.

# Python code to automatically change the tool on an ATC router and measure it if its value in the tool table is = 0 

# Change tool script for SIMCNC & Csmio-s 
# Erwan Le Foll 26/11/2023   https://youtube.com/@erwan3953

# In my configuration, the homing is done at X0Y0Z0 at the top right of the machine, the 23 tools are on the X axis in the Y+ area
# The working area is in Y- which allows the tools to be protected by the SoftLimit Zone

#-----------------------------------------------------------
# Machine informations
#-----------------------------------------------------------


# infos
ToolCount = 23                    # Nombre max. d'outils sur la table premier outil =1 (Maximum number of tools on the table, first tool=1)

# vitesses (speed)
ZY_final_speed = 1000              # slow final approach speed of Y or Z)
Z_down_fast_speed = 2000           # vitesse de Z d'aproche rapide (fast approach speed of Z)
Z_up_speed = 4000                 # viteese de lever du Z (speed to lift Z)
YX_speed = 20000                    # Vitesse de l'axe Y et X (speed of Y and X axis)

# positions
Y_position_first_tool = -14        # Y position where the first tool is stored.
Y_position_safe_zone = -100        # Y zone where tools can move on the X axis without touching each other tools stored
X_position_first_tool = -206    # X position of the first tool
Z_position_tools = -153.3          # Z location where the tool is stored
Z_position_approach = -135         # Z location where it is necessary to start slowing down and trigger the air conne cleaner
X_distance_between_tools = -76     # distance between each tool holders ( minus = seconde tool on left)

# input/output csmio number (instead a number, with " Bone " and it will be ignore)
check_tool_in_spindel = 24          # Digital input number managing the tool detection sensor.
check_clamp_status = 25             # Digital input number managing the cone clamp open sensor.
valve_collet = 13                   # Digital output number managing the valve for tool change.
valve_clean_cone = 14               # Digital output number managing the valve for tool holder cone cleaning.
valve_dustColect_out = 9            # Remove dust shoe
valve_dustColect_under = 11         # put the dust shoe ready to suck
valve_blower = None                 #12  # Digital output number managing the valve for the blower

# time
blowing_time = 0.5                  # Time in seconds of the blower at the tool drop or measurement.
time_spindle_stop = 15              # WARNING If to short you can destroy your spindel Clamp. Time in seconds for the stop of your spindel with the >>>HEAVIEST<<< tool.

# tool rack
ToolRackUnder = 10
ToolRackOut = 8

#-----------------------------------------------------------
# probing infos
#-----------------------------------------------------------

do_i_have_prob = True               #  True = tool measurement enabled. False = tool measurement disabled
every_time_get_measure = False      # True = measure every time, False = measure only if tool table is at zero
probeStartAbsPos = {'X_probe': -92, 'Y_probe': -36.5, 'Z_probe': -30} #  Placement coordinates above the probe [X_probe, Y_probe, Z_probe] Your longest tool must pass with this Z!
probeIndex = 0                      # corresponds to the input you configured in the simcnc settings
zEndPosition = -210                 # The Z-axis will not go down any further!)
refToolProbePos = -143.67           # Height at which your reference tool touches the probe (if your reference tool touches at Z-100mm and you indicate - 100mm here, then it will be referenced to 0mm))
fastProbeVel = 900                  # Speed of the first, fast measurement (units/min)
slowProbeVel = 250                  # Speed of the second, slow measurement (units/min)
goUpDist = 6                        # Z-axis up travel in mm between the two measurements
fineProbingDelay = 0.2              # Time in seconds between the two measurements
checkFineProbingDiff = False        # Do not change)
fineProbeMaxAllowedDiff = 0.1       # tolerance between the two table prob measurements
moveX = True                        # Ne pas changer (Do not change)
moveY = True                        # Ne pas changer (Do not change)

#-----------------------------------------------------------
# WORK IN PROGRESS 
# 3d prob infos (infos si dessous utilisé par le fichier 3d_prob.py)
#-----------------------------------------------------------

threeD_prob = 1                     # numero de l'emplacement prob-3d, si PAS de prob3D indiquer "None" 
threeD_probeIndex = 2               # correspond a l'entrée que vous avez configuré dans les settings de simcnc (0,1,2 ou 3 possible)
wake_up_prob = True                 # fait tourner le prob pour l'allumer
wake_up_speed = 3000                # RPM, My spindel dosen't start under.
time_spindel_stop_prob = 5          # Time to stop the spindel withe the prob a RPM on ligne above
threeD_fastProbeVel = 700           # vitesse de la premiere mesure, rapide (units/min) (Speed of the first, fast measurement (units/min))
threeD_slowProbeVel = 250           # vitesse du deuxieme mesure, lente (units/min) (Speed of the second, slow measurement (units/min))
threeD_retract = 5                  # retract between 2 mesures
threeD_prob_ball_diameter = 2       # size of the 3d prob bal diameter

#-----------------------------------------------------------
# Assigns a name to each axis when using getposition.
# "d.getPosition(CoordMode.Machine)" returns a machine position which, if the machine is at zero, will be: 0.0.0.0.0.0
# These lines of code are used to name each digit returned in the format X.Y.Z.A.B.C, where the first zero at position 0 is named X, the second zero at position 1 is named Y, etc.
# If your tool changer/holder is on the Y-axis instead of X-axis like mine, you can either replace all the X's in the code m6.py with Y's, or here, name X=1 and Y=0 (a trick I haven't tested).
#-----------------------------------------------------------

X = 0
Y = 1
Z = 2
A = 3
C = 5