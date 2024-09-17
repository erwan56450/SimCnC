
# - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Settings  - - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 												

Ball_diameter = 2
Probe_Index = 2
Return_speed = 6000

Probing_velocity = 2000															
Maximum_distance = 200	 #attention si vous indiquer une valeur trop grand une erreure peux survenir si vous approcher les soft limit de la machine

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

# X++
Postion_Xp = Probe_Xp(Starting_position)
d.moveToPosition( CoordMode.Machine, Starting_position,  Return_speed)

# X--
Postion_Xn = Probe_Xn(Starting_position)
Starting_position[Axis.X.value] = ( Postion_Xp[Axis.X.value] + Postion_Xn[Axis.X.value] ) / 2				
d.moveToPosition( CoordMode.Machine, Starting_position,  Return_speed)		

# Y++
Postion_Yp = Probe_Yp(Starting_position)
d.moveToPosition( CoordMode.Machine, Starting_position,  Return_speed)

# Y--
Postion_Yn = Probe_Yn(Starting_position)
Starting_position[Axis.Y.value] = ( Postion_Yp[Axis.Y.value] + Postion_Yn[Axis.Y.value] ) / 2
d.moveToPosition( CoordMode.Machine, Starting_position,  Return_speed)


Probing_velocity = 500
print("  -  Probing velocity  =  " + str(Probing_velocity)) 

# X++
Starting_position[Axis.X.value] = Postion_Xp[Axis.X.value] - Ball_diameter / 2
d.moveToPosition( CoordMode.Machine, Starting_position, Return_speed)
Postion_Xp = Probe_Xp(Starting_position)

# X--
Starting_position[Axis.X.value] = Postion_Xn[Axis.X.value] + Ball_diameter / 2
d.moveToPosition( CoordMode.Machine, Starting_position, Return_speed)
Postion_Xn = Probe_Xn(Starting_position)

Starting_position[Axis.X.value] = ( Postion_Xp[Axis.X.value] + Postion_Xn[Axis.X.value] ) / 2		
d.moveToPosition( CoordMode.Machine, Starting_position,  Return_speed)

# Y++
Starting_position[Axis.Y.value] = Postion_Yp[Axis.Y.value] - Ball_diameter / 2
d.moveToPosition( CoordMode.Machine, Starting_position, Return_speed)
Postion_Yp = Probe_Yp(Starting_position)

# Y--
Starting_position[Axis.Y.value] = Postion_Yn[Axis.Y.value] + Ball_diameter / 2
d.moveToPosition( CoordMode.Machine, Starting_position, Return_speed)
Postion_Yn = Probe_Yn(Starting_position)


Starting_position[Axis.Y.value] = ( Postion_Yp[Axis.Y.value] + Postion_Yn[Axis.Y.value] ) / 2
d.moveToPosition( CoordMode.Machine, Starting_position,  Return_speed)


print("Średnica po X" + str(Postion_Xp[Axis.X.value] - Postion_Xn[Axis.X.value] + Ball_diameter))
print("Srednica po Y" + str(Postion_Yp[Axis.Y.value] - Postion_Yn[Axis.Y.value] + Ball_diameter))




	




	



	






