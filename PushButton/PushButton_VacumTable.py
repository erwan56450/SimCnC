
# set the corect output number here
ToolRackUnder = 9
ToolRackOut = 8

# link this script to a push button in simcnc
# you must copy/past this file where simcnc open the windows when you clique "ouput clicked> run script "


import sys


#call csmio ips
mod_IP = d.getModule(ModuleType.IP, 0) 

if mod_IP.getDigitalIO(IOPortDir.OutputPort, ToolRackUnder) == DIOPinVal.PinReset:
    print("tool rack out")
    mod_IP.setDigitalIO(ToolRackUnder, DIOPinVal.PinSet)
    sys.exit()

if mod_IP.getDigitalIO(IOPortDir.OutputPort, ToolRackUnder) == DIOPinVal.PinSet:
    print("tool rack under")
    mod_IP.setDigitalIO(ToolRackUnder, DIOPinVal.PinReset)
    sys.exit()








