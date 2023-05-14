
# set the corect output number here
OutputToControl = 0

# link this script to a push button in simcnc
# you must copy/past this file where simcnc open the windows when you clique "ouput clicked> run script "


import sys


#call csmio ips
mod_IP = d.getModule(ModuleType.IP, 0) 

if mod_IP.getDigitalIO(IOPortDir.OutputPort, OutputToControl) == DIOPinVal.PinReset:
    print("Aspiration ON")
    mod_IP.setDigitalIO(OutputToControl, DIOPinVal.PinSet)
    sys.exit()

if mod_IP.getDigitalIO(IOPortDir.OutputPort, OutputToControl) == DIOPinVal.PinSet:
    print("Aspiration OFF")
    mod_IP.setDigitalIO(OutputToControl, DIOPinVal.PinReset)
    sys.exit()








