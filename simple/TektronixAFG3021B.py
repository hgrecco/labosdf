# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals, print_function, absolute_import

import time

from matplotlib import pyplot as plt
import numpy as np

import visa

rm = visa.ResourceManager()

print(rm.list_resources())

resource_name = 'USB0::0x0699::0x0346::C034165::INSTR'
fungen = rm.open_resource(resource_name)

fungen.query('*IDN?')

# Rampa logaritmica de frequencias 
# Los dos primeros numeros (1 y 3) indican los exponentes de los limites(10^1 y 10^3)
# El siguiente el numero de pasos
for freq in np.logspace(1, 3, 20):
    fungen.write('FREQ %f' % freq)
    time.sleep(0.1)

# Rampa lineal de amplitudes
# Los dos primeros numeros (0 y 1) indican los limites.
# El siguiente el numero de pasos
for amplitude in np.linspace(0, 1, 10):
    fungen.write('VOLT %f' % amplitude)
    time.sleep(0.1)
    
    
# Rampa lineal de offset
# Los dos primeros numeros (0 y 1) indican los limites.
# El siguiente el numero de pasos
for offset in np.linspace(0, 1, 10):
    fungen.write('VOLT:OFFS %f' % offset)
    time.sleep(0.1)

fungen.close()





