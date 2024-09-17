from tkinter import *
import time
# - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Settings  - - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
Ball_diameter = 2.00  													
Sensor_hysteresis_Xp = 0								
Sensor_hysteresis_Xn = 0								
Sensor_hysteresis_Yp = 0						
Sensor_hysteresis_Yn = 0					
Sensor_hysteresis_Zn = 0										
Probe_Index = 2
Return_speed = 1000

# - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Functions - - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def info():
	print("\n\n\n - - - - -  Probing  configuration  - - - - ")
	print("Main parameters : ")
	print("  -  Ball diameter       =  " + str(Ball_diameter))
	print("  -  Probing velocity  =  " + str(P_v.get()))
	print("  -  Max distance      =  " + str(M_d.get()))
	print("")
	print("Sensor hysteresis : ")
	print("  -  X axis, positive direction  =  " + str(Sensor_hysteresis_Xp))
	print("  -  X axis, positive negative  =  " + str(Sensor_hysteresis_Xn))
	print("  -  Y axis, positive direction  =  " + str(Sensor_hysteresis_Yp))
	print("  -  Y axis, positive negative  =  " + str(Sensor_hysteresis_Yn))
	print("")


def Probe_Xp():
	info()
	print(" - - - - - - -  Probe X  plus  - - - - - - - -")																						
	Probing_velocity = float(P_v.get())														
	Maximum_distance = float(M_d.get())																		
	Starting_position = d.getPosition( CoordMode.Machine )																	
	Maximum_position = Starting_position.copy()																	
	Maximum_position[Axis.X.value] +=  Maximum_distance																						

	print("  >  Probing Start")																																													
	if(d.executeProbing( CoordMode.Machine, Maximum_position, Probe_Index, Probing_velocity ) == False):																						
		print("  >  Probing Failed !")																			
		B_probing_Xp.configure(bg = "red")
		B_GoToZero_X.configure(bg = "red")
	else:																													
		print("  >  Probing Success")																			
		B_probing_Xp.configure(bg = "#f0f0f0")
		B_GoToZero_X.configure(bg = "green")
		Probe_activation_position = d.getProbingPosition( CoordMode.Machine )																			
		Probe_stop_position = d.getPosition( CoordMode.Machine )																	
		Current_axis_position = -(Ball_diameter / 2) + Sensor_hysteresis_Xp + (Probe_stop_position[Axis.X.value] -  Probe_activation_position[Axis.X.value]) 										
		d.setAxisProgPosition( Axis.X, Current_axis_position )																			

	d.moveToPosition( CoordMode.Machine, Starting_position,  Return_speed)
	print("\n - - - - - - - -  Probe End  - - - - - - - - -\n")


def Probe_Xn():
	info()
	print(" - - - - - - -  Probe X  minus  - - - - - - - -")																						
	Probing_velocity = float(P_v.get()) 																
	Maximum_distance = float(M_d.get())																		
	Starting_position = d.getPosition( CoordMode.Machine )																		
	Maximum_position = Starting_position.copy()																	
	Maximum_position[Axis.X.value] -=  Maximum_distance																						

	print("  >  Probing Start")																						
	if(d.executeProbing( CoordMode.Machine, Maximum_position, Probe_Index, Probing_velocity ) == False):
		print("  >  Probing Failed !")																			
		B_probing_Xn.configure(bg = "red")
		B_GoToZero_X.configure(bg = "red")
	else:																													
		print("  >  Probing Success")																			
		B_probing_Xn.configure(bg = "#f0f0f0")
		B_GoToZero_X.configure(bg = "green")
		Probe_activation_position = d.getProbingPosition( CoordMode.Machine )
		Probe_stop_position = d.getPosition( CoordMode.Machine )																		
		Current_axis_position = (Ball_diameter / 2) - Sensor_hysteresis_Xn + (Probe_stop_position[Axis.X.value] -  Probe_activation_position[Axis.X.value]) 										
		d.setAxisProgPosition( Axis.X, Current_axis_position )			
																
	d.moveToPosition( CoordMode.Machine, Starting_position,  Return_speed)
	print("\n - - - - - - - -  Probe End  - - - - - - - - -\n")


def Probe_Yp():
	info()
	print(" - - - - - - -  Probe Y  plus  - - - - - - - -")																						
	Probing_velocity = float(P_v.get())																
	Maximum_distance = float(M_d.get())																		
	Starting_position = d.getPosition( CoordMode.Machine )																	
	Maximum_position = Starting_position.copy()																	
	Maximum_position[Axis.Y.value] +=  Maximum_distance																						

	print("  >  Probing Start")																																													
	if(d.executeProbing( CoordMode.Machine, Maximum_position, Probe_Index, Probing_velocity ) == False):																							
		print("  >  Probing Failed !")																			
		B_probing_Yp.configure(bg = "red")
		B_GoToZero_Y.configure(bg = "red")
	else:																													
		print("  >  Probing Success")																			
		B_probing_Yp.configure(bg = "#f0f0f0")
		B_GoToZero_Y.configure(bg = "green")
		Probe_activation_position = d.getProbingPosition( CoordMode.Machine )																			
		Probe_stop_position = d.getPosition( CoordMode.Machine )																		
		Current_axis_position = -(Ball_diameter / 2) + Sensor_hysteresis_Yp + (Probe_stop_position[Axis.Y.value] -  Probe_activation_position[Axis.Y.value]) 										
		d.setAxisProgPosition( Axis.Y, Current_axis_position )														

	d.moveToPosition( CoordMode.Machine, Starting_position,  Return_speed)
	print("\n - - - - - - - -  Probe End  - - - - - - - - -\n")


def Probe_Yn():
	info()
	print(" - - - - - - -  Probe X  plus  - - - - - - - -")																						
	Probing_velocity = float(P_v.get())																
	Maximum_distance = float(M_d.get())																		
	Starting_position = d.getPosition( CoordMode.Machine )																	
	Maximum_position = Starting_position.copy()																	
	Maximum_position[Axis.Y.value] -=  Maximum_distance																						

	print("  >  Probing Start")																																													
	if(d.executeProbing( CoordMode.Machine, Maximum_position, Probe_Index, Probing_velocity ) == False):																							
		print("  >  Probing Failed !")																			
		B_probing_Yn.configure(bg = "red")
		B_GoToZero_Y.configure(bg = "red")
	else:																													
		print("  >  Probing Success")																			
		B_probing_Yn.configure(bg = "#f0f0f0")
		B_GoToZero_Y.configure(bg = "green")
		Probe_activation_position = d.getProbingPosition( CoordMode.Machine )																			
		Probe_stop_position = d.getPosition( CoordMode.Machine )																	
		Current_axis_position = (Ball_diameter / 2) - Sensor_hysteresis_Yn + (Probe_stop_position[Axis.Y.value] -  Probe_activation_position[Axis.Y.value]) 										
		d.setAxisProgPosition( Axis.Y, Current_axis_position )																		

	d.moveToPosition( CoordMode.Machine, Starting_position,  Return_speed)
	print("\n - - - - - - - -  Probe End  - - - - - - - - -\n")
	

def Probe_Zn():
	info()
	print(" - - - - - - -  Probe Z  minus  - - - - - - - -")																						
	Probing_velocity = float(P_v.get())				
	Maximum_distance = float(M_d.get())																		
	Starting_position = d.getPosition( CoordMode.Machine )																
	Maximum_position = Starting_position.copy()																	
	Maximum_position[Axis.Z.value] -=  Maximum_distance																						

	print("  >  Probing Start")																																													
	if(d.executeProbing( CoordMode.Machine, Maximum_position, Probe_Index, Probing_velocity ) == False):																							
		print("  >  Probing Failed !")																			
		B_probing_Zn.configure(bg = "red")
	else:																													
		print("  >  Probing Success")																			
		B_probing_Zn.configure(bg = "#f0f0f0")
		Probe_activation_position = d.getProbingPosition( CoordMode.Machine)																		
		Probe_stop_position = d.getPosition( CoordMode.Machine )												
		Current_axis_position = Sensor_hysteresis_Zn + (Probe_stop_position[Axis.Z.value] -  Probe_activation_position[Axis.Z.value]) 										
		d.setAxisProgPosition( Axis.Z, Current_axis_position )																		

	d.moveToPosition( CoordMode.Machine, Starting_position,  Return_speed)
	print("\n - - - - - - - -  Probe End  - - - - - - - - -\n")


def GoTo_X0():
	MsgBox = messagebox.askquestion ('Warning !!!','Have you done probing for the X axis?',icon = 'question')
	if MsgBox == 'yes':
		print(" - - - - - - - - -  GoTo_X0 - - - - - - - - - -")
		
		Position_M = d.getPosition( CoordMode.Machine )	
		Position_M[Axis.Z.value] = 0 
		d.moveToPosition( CoordMode.Machine, Position_M,  Return_speed)
		
		time.sleep(0.5)

		Position_P = d.getPosition( CoordMode.Program )	
		Position_P[Axis.X.value] = 0 
		d.moveToPosition( CoordMode.Program, Position_P,  Return_speed)


def GoTo_Y0():
	MsgBox = messagebox.askquestion ('Warning !!!','Have you done probing for the Y axis?',icon = 'question')
	if MsgBox == 'yes':
		print(" - - - - - - - - -  GoTo_Y0 - - - - - - - - - -")

		Position_M = d.getPosition( CoordMode.Machine )	
		Position_M[Axis.Z.value] = 0 
		d.moveToPosition( CoordMode.Machine, Position_M,  Return_speed)
		
		time.sleep(0.5)

		Position_P = d.getPosition( CoordMode.Program )	
		Position_P[Axis.Y.value] = 0 
		d.moveToPosition( CoordMode.Program, Position_P,  Return_speed)



# - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Main Window - - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

window = Tk()																																			
window.geometry("240x360")																												
window.title( "Probing 3D" )																													
window.attributes("-topmost", True)

L3 = Label(window, text="Probing velocity", font= ("Times New Roman",12))										
L3.place(x=20, y=30, height=20, width=100)																						

P_v = Entry(window)																											
P_v.place(x=135, y=30 ,height=20, width=30)																
P_v.insert(0,"200")																												

L4 = Label(window, text="unit/min", font= ("Times New Roman",12))													
L4.place(x=170, y=30, height=20, width=50)																						


L5 = Label(window, text="Max distance    ", font= ("Times New Roman",12))
L5.place(x=20, y=55, height=20, width=100)

M_d = Entry(window)
M_d.place(x=135, y=55 ,height=20, width=30)
M_d.insert(0,"20")

L6 = Label(window, text="unit      ", font= ("Times New Roman",12))
L6.place(x=170, y=55, height=20, width=50)


B_probing_Xp = Button(window, text='X+', font= ("Times New Roman",14), command = Probe_Xp)				
B_probing_Xp.place(x=150, y=180, height=40, width=40)																			

B_probing_Xn = Button(window, text='X- ', font= ("Times New Roman",14), command = Probe_Xn)
B_probing_Xn.place(x=50, y=180, height=40, width=40)

B_probing_Yp = Button(window, text='Y+', font= ("Times New Roman",14), command = Probe_Yp)
B_probing_Yp.place(x=100, y=130, height=40, width=40)

B_probing_Yn = Button(window, text='Y- ', font= ("Times New Roman",14), command = Probe_Yn)
B_probing_Yn.place(x=100, y=230, height=40, width=40)

B_probing_Zn = Button(window, text='Z- ', font= ("Times New Roman",14), command = Probe_Zn)
B_probing_Zn.place(x= 100, y=180, height=40, width=40)				

B_GoToZero_X = Button(window, text='GoTo X0', font= ("Times New Roman",14), command = GoTo_X0 )		
B_GoToZero_X.place(x=10, y=300, height=40, width=100)		

B_GoToZero_Y = Button(window, text='GoTo Y0 ', font= ("Times New Roman",14), command = GoTo_Y0 )		
B_GoToZero_Y.place(x=120, y=300, height=40, width=100)	

mainloop( )