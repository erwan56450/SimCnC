import math
# - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Settings  - - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 												

Ball_diameter = 2
Probe_Index = 2
Return_speed = 6000

Probing_velocity = 500															
Maximum_distance = 200	

# - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Functions  - - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 	

def Probe_Xp(Start_pos):															
	Maximum_position = Start_pos.copy()																	
	Maximum_position[Axis.X.value] +=  Maximum_distance		
								
	print("  >  Probing Start")																						
	if(d.executeProbing( CoordMode.Machine, Maximum_position, Probe_Index, Probing_velocity ) == False):
		print("  >  Probing Failed !")
		sys.exit(0)																			
	else:																													
		print("  >  Probing Success")																	
		return d.getProbingPosition( CoordMode.Machine )


def Probe_Xn(Start_pos):															
	Maximum_position = Start_pos.copy()																	
	Maximum_position[Axis.X.value] -=  Maximum_distance		
																
	print("  >  Probing Start")																						
	if(d.executeProbing( CoordMode.Machine, Maximum_position, Probe_Index, Probing_velocity ) == False):
		print("  >  Probing Failed !")
		sys.exit(0)																			
	else:																													
		print("  >  Probing Success")																			
		return d.getProbingPosition( CoordMode.Machine )


def Probe_Yp(Start_pos):															
	Maximum_position = Start_pos.copy()																	
	Maximum_position[Axis.Y.value] +=  Maximum_distance		
															
	print("  >  Probing Start")																						
	if(d.executeProbing( CoordMode.Machine, Maximum_position, Probe_Index, Probing_velocity ) == False):
		print("  >  Probing Failed !")
		sys.exit(0)																			
	else:																													
		print("  >  Probing Success")																			
		return d.getProbingPosition( CoordMode.Machine )


def Probe_Yn(Start_pos):															
	Maximum_position = Start_pos.copy()																	
	Maximum_position[Axis.Y.value] -=  Maximum_distance		
														
	print("  >  Probing Start")																						
	if(d.executeProbing( CoordMode.Machine, Maximum_position, Probe_Index, Probing_velocity ) == False):
		print("  >  Probing Failed !")
		sys.exit(0)																			
	else:																													
		print("  >  Probing Success")																			
		return d.getProbingPosition( CoordMode.Machine )


# - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Info  - - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 							

print("\n\n\n - - - - -  Probing  configuration  - - - - ")
print("Main parameters : ")
print("  -  Ball diameter  =  " + str(Ball_diameter))
print("  -  Probe Index  =  " + str(Probe_Index))
print("  -  Return speed  =  " + str(Return_speed))
print("  -  Probing velocity  =  " + str(Probing_velocity))
print("  -  Max distance      =  " + str(Maximum_distance))

# - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Makro   - - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 	

Starting_position = d.getPosition( CoordMode.Machine )


# Y++
Postion_Y1 = Probe_Yp(Starting_position)
d.moveToPosition( CoordMode.Machine, Starting_position,  Return_speed)


Starting_position[Axis.X.value] += 40
d.moveToPosition( CoordMode.Machine, Starting_position,  Return_speed)

# Y++
Postion_Y2 = Probe_Yp(Starting_position)
d.moveToPosition( CoordMode.Machine, Starting_position,  Return_speed)

Starting_position[Axis.X.value] -= 40
d.moveToPosition( CoordMode.Machine, Starting_position,  Return_speed)



X = (Postion_Y2[Axis.X.value] - Postion_Y1[Axis.X.value])
Y = (Postion_Y2[Axis.Y.value] - Postion_Y1[Axis.Y.value])

print(math.degrees(math.atan2(Y, X)))

