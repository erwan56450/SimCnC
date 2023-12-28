# set the corect output number here
ToolRackUnder = 10
ToolRackOut = 8


import sys
import time

#call csmio ips
mod_IP = d.getModule(ModuleType.IP, 0) 

#Call ouput  tool rack out
print("call tool  rack out")
mod_IP.setDigitalIO(ToolRackOut, DIOPinVal.PinSet)

time.sleep(2) #time for piston to expend

print("tool rack is out")
mod_IP.setDigitalIO(ToolRackOut, DIOPinVal.PinReset)