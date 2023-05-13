valve_dustColect_out = 9

import time



def set_digital_output(output_number, value):
    if output_number is None:
        return
    try:
        mod_IP = d.getModule(ModuleType.IP, 0) # pour cismo ipS
        mod_IP.setDigitalIO(output_number, value)
    except NameError:
        print(_("------------------\nThe digital output has not been well defined."))

        

# evacue le récupérateur de poussières
set_digital_output(valve_dustColect_out, DIOPinVal.PinSet)   
time.sleep(2)
set_digital_output(valve_dustColect_out, DIOPinVal.PinReset)






