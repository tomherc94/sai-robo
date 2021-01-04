"""
from pyfirmata import Arduino,util
from pyfirmata import SERVO
import time

placa = Arduino("/dev/ttyUSB0")
placa.digital[9].mode = SERVO

def liberacao():
    placa.digital[8].write(1)
    placa.digital[9].write(180)
    print("Liberado!")

    time.sleep(1) 
    #placa.delay(1)
    
    placa.digital[8].write(0)
    placa.digital[9].write(0)
    print("Travado!")
    pass
"""