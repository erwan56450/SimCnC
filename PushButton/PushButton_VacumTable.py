OutputToControl = 0
#3 table aspirante
#0 aspiration

import sys

mod_IP = d.getModule(ModuleType.IP, 0)

if mod_IP.getDigitalIO(IOPortDir.OutputPort, OutputToControl) == DIOPinVal.PinReset:
    print("Aspiration ON")
    mod_IP.setDigitalIO(OutputToControl, DIOPinVal.PinSet)
    sys.exit()

if mod_IP.getDigitalIO(IOPortDir.OutputPort, OutputToControl) == DIOPinVal.PinSet:
    print("Aspiration OFF")
    mod_IP.setDigitalIO(OutputToControl, DIOPinVal.PinReset)
    sys.exit()








