# -*- coding: utf-8 -*-
"""
Osciloscopio Tektronix TDS1002B')
Manual U (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/RigolDS1000_user.pdf
Manual P (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/RigolDS1000_prog.pdf
Manual U (local): \\Srvlabos\manuales\Rigol\RigolDS1000_user.pdf
Manual P (local): \\Srvlabos\manuales\Rigol\RigolDS1000_prog.pdf
"""

from __future__ import division, unicode_literals, print_function, absolute_import

from matplotlib import pyplot as plt
import numpy as np

import visa

print(__doc__)

# Este string determina el intrumento que van a usar.
# Lo tienen que cambiar de acuerdo a lo que tengan conectado.
resource_name = 'USB0::0x1AB1::0x0588::DS1K00005888::INSTR'

rm = visa.ResourceManager()

osci = rm.open_resource(resource_name)

# Pide identificacion
print(osci.query('*IDN?'))

# Escala de voltaje
voltscale = float(osci.query(":CHAN1:SCAL?"))
 
# Offset de voltaje
voltoffset = float(osci.query(":CHAN1:OFFS?"))

# Escala de tiempo
timescale = float(osci.query(":TIM:SCAL?"))
# Sample rate
sample_rate = float(osci.query(":ACQ:SAMP?"))


# Offset de tiempo
timeoffset = float(osci.query(":TIM:OFFS?"))


# Cambia a modo RAW (lee todo los puntos)
osci.write(':WAV:POIN:MODE RAW')

# Frena la adquisicion
osci.write(':STOP')

# Adquiere los datos del canal 1 y los devuelve en un array de numpy
data = osci.query_binary_values(':WAV:DATA? CHAN1', datatype='B', container=np.array)

divisions = 12 * 6
tiempo = timeoffset - np.arange(len(data)) / (1. / 2. * sample_rate)


# Convierte los datos de Unidades digitales a Volts
data = (240 - data) * voltscale / 25 - (voltoffset + voltscale * 4.6)
 
plt.plot(tiempo, data)
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')


# Si vas a repetir la adquisicion muchas veces sin cambiar la escala
# es util definir una funcion que mida y haga las cuentas
def definir_medir(inst):
    # Escala de voltaje
    voltscale = float(inst.query(":CHAN1:SCAL?"))

    # Offset de voltaje
    voltoffset = float(inst.query(":CHAN1:OFFS?"))

    # Escala de tiempo
    timescale = float(inst.query(":TIM:SCAL?"))

    # Offset de tiempo
    timeoffset = float(inst.query(":TIM:OFFS?"))

    # creamos una function auxiliar
    def _medir():
        # Adquiere los datos del canal 1 y los devuelve en un array de numpy
        data = inst.query_binary_values(':WAV:DATA? CHAN1', datatype='B', container=np.array)

        divisions = 12 * 6
        tiempo = timeoffset - np.arange(len(data)) / (1. / 2. * sample_rate)

        # Convierte los datos de Unidades digitales a Volts
        data = (240 - data) * voltscale / 25 - (voltoffset + voltscale * 4.6)
        return tiempo, data
    
    # Devolvemos la funcion auxiliar que "sabe" la escala
    return _medir


import time

medir = definir_medir(osci)
for n in range(10):
    tiempo, data = medir()
    plt.figure()
    plt.plot(tiempo, data)
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Voltaje [V]')
    time.sleep(.1)


osci.close()




