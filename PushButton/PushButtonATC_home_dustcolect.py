# I use this code on the 'reference all axise' in sim cnc, 

# first it release my dust shoe
# sec execute homming

import time


mod_IP = d.getModule(ModuleType.IP, 0) # pour cismo ipS
mod_IP.setDigitalIO(9, DIOPinVal.PinSet)
time.sleep(2)
mod_IP.setDigitalIO(9, DIOPinVal.PinReset)

#execute home
d.executeHoming()