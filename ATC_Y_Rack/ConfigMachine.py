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
ToolCount = 5                      #  Maximum number of tools on the table, first tool=1

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

# input/output csmio number (instead a number, with " Bone " and it will be ignore)
check_tool_in_spindel = 24          # Digital input number managing the tool detection sensor
check_clamp_status = 25             # Digital input number managing the cone clamp open sensor
valve_collet = 13                   # Digital output number managing the valve for tool change
valve_clean_cone = 14               # Digital output number managing the valve for tool holder cone cleaning
valve_dustColect_out = None         # Remove dust shoe
valve_dustColect_under = None       # put the dust shoe ready to suck
valve_blower = None                 # Digital output number managing the valve for the blower

# time
blowing_time = 0.5                  # Time in seconds of the blower at the tool drop or measurement
time_spindle_stop = 15              # WARNING If to short you will destroy your spindel. Time in seconds for the stop of your spindel with the heaviest tool

#-----------------------------------------------------------
# Infos sur le Contacteur de palpage (probing infos)
#-----------------------------------------------------------

do_i_have_prob = True               # True = tool measurement enabled. False = tool measurement disabled
every_time_get_measure = True       # True = measure every time, False = measure only if tool table is at zero
probeStartAbsPos = {'X_probe': 10, 'Y_probe': 90, 'Z_probe': -80} #Placement coordinates above the probe [X_probe, Y_probe, Z_probe] Your longest tool must pass with this Z!
probeIndex = 0                      # settings->Modules->IO Signals  : 0,1,2 or 3  (corresponds to the input you configured in the simcnc settings)
zEndPosition = -190                 # The Z-axis will not go down any further!
refToolProbePos = -143.67           # Height at which your reference tool touches the probe (if your reference tool touches at Z-100mm and you indicate - 100mm here, then it will be referenced to 0mm)
fastProbeVel = 700                  # Speed of the first, fast measurement (units/min)
slowProbeVel = 250                  # Speed of the second, slow measurement (units/min)
goUpDist = 6                        # Z-axis up travel in mm between the two measurements
fineProbingDelay = 0.2              # Time in seconds between the two measurements)
checkFineProbingDiff = False        # Do not change
fineProbeMaxAllowedDiff = 0.1       # tolerance between the two measurements
moveX = True                        # Do not change
moveY = True                        # Do not change


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

email:
Erwan@fridu.net