# -*- coding: utf-8 -*-
"""
Generador de funciones Tektronix AFG 3021B
Manual U (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/TektronixAFG3000.pdf
Manual P (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/TektronixAFG3000_p.pdf
Manual U (local): \\Srvlabos\manuales\Tektronix\AFG3012B (M Usuario).pdf
Manual P (local): \\Srvlabos\manuales\Tektronix\AFG3012B (Prog Manual).pdf
"""

from __future__ import division, unicode_literals, print_function, absolute_import

import time

import numpy as np
import visa

print(__doc__)

# Este string determina el intrumento que van a usar.
# Lo tienen que cambiar de acuerdo a lo que tengan conectado.
resource_name = 'USB0::0x0699::0x0346::C033250::INSTR'

rm = visa.ResourceManager()

# Abre la sesion VISA de comunicacion
fungen = rm.open_resource(resource_name)

print(fungen.query('*IDN?'))

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





