import math

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Settings  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

Ball_diameter = 2
Probe_Index = 2
Return_speed = 500

Probing_velocity = 300
Maximum_distance = 200

# Définir les angles de mesure (en degrés)
Probing_angles = [0, 120, 240]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Functions  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def Probe(Start_pos):
    print(f"  >  Probing Start at X: {Start_pos[Axis.X.value]}, Y: {Start_pos[Axis.Y.value]}")
    if not d.executeProbing(CoordMode.Machine, Start_pos, Probe_Index, Probing_velocity):
        print("  >  Probing Failed!")
        sys.exit(0)
    else:
        probing_position = d.getProbingPosition(CoordMode.Machine)
        print(f"  >  Probing Success. Position: X = {probing_position[Axis.X.value]}, Y = {probing_position[Axis.Y.value]}")
        return probing_position

def calculate_circle_center(p1, p2, p3):
    # Utilisation des équations du cercle passant par trois points
    x1, y1 = p1[Axis.X.value], p1[Axis.Y.value]
    x2, y2 = p2[Axis.X.value], p2[Axis.Y.value]
    x3, y3 = p3[Axis.X.value], p3[Axis.Y.value]

    print(f"Calculating center from points:\n  P1: X = {x1}, Y = {y1}\n  P2: X = {x2}, Y = {y2}\n  P3: X = {x3}, Y = {y3}")

    # Calcul des déterminants pour résoudre l'équation du centre
    d = 2 * ((x1 * (y2 - y3)) + (x2 * (y3 - y1)) + (x3 * (y1 - y2)))
    if d == 0:
        raise ValueError("Points are collinear, cannot determine circle center.")

    ux = (((x1**2 + y1**2) * (y2 - y3)) + ((x2**2 + y2**2) * (y3 - y1)) + ((x3**2 + y3**2) * (y1 - y2))) / d
    uy = (((x1**2 + y1**2) * (x3 - x2)) + ((x2**2 + y2**2) * (x1 - x3)) + ((x3**2 + y3**2) * (x2 - x1))) / d

    return [ux, uy]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Info  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

print("\n\n\n - - - - -  Probing configuration  - - - - ")
print("Main parameters:")
print("  -  Ball diameter  =  " + str(Ball_diameter))
print("  -  Probe Index  =  " + str(Probe_Index))
print("  -  Return speed  =  " + str(Return_speed))
print("  -  Probing velocity  =  " + str(Probing_velocity))
print("  -  Max distance      =  " + str(Maximum_distance))
print("  -  Probing angles    =  " + str(Probing_angles))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Makro   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

Starting_position = d.getPosition(CoordMode.Machine)

# Définir le rayon pour les déplacements
radius = Maximum_distance / 2

# Stocker les positions mesurées
Probing_positions = []

# Effectuer les palpages aux angles définis
for angle_deg in Probing_angles:
    angle_rad = math.radians(angle_deg)
    position = Starting_position.copy()
    position[Axis.X.value] += radius * math.cos(angle_rad)
    position[Axis.Y.value] += radius * math.sin(angle_rad)
    probing_position = Probe(position)
    Probing_positions.append(probing_position)
    d.moveToPosition(CoordMode.Machine, Starting_position, Return_speed)

# Calcul du centre
center = calculate_circle_center(*Probing_positions)

# Déplacement du palpeur au centre
print(f"Calculated center: X = {center[0]:.3f}, Y = {center[1]:.3f}")
print(f"Moving to calculated center: X = {center[0]}, Y = {center[1]}")

# Préparer la position complète
Center_position = Starting_position.copy()
Center_position[Axis.X.value] = center[0]
Center_position[Axis.Y.value] = center[1]
d.moveToPosition(CoordMode.Machine, Center_position, Return_speed)
