# Bouton pour simcnc, 
# actione la valve N9 pour déplacer le colecteur de poussière avant de faire un homing.

# Récupérer la position de la machine et la nome "position" (Retrieve the machine's position and name it "position".)


import time




mod_IP = d.getModule(ModuleType.IP, 0) # pour cismo ipS
mod_IP.setDigitalIO(9, DIOPinVal.PinSet)
time.sleep(2)
mod_IP.setDigitalIO(9, DIOPinVal.PinReset)

#execute home
d.executeHoming()