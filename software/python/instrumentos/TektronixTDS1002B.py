# -*- coding: utf-8 -*-
"""
Osciloscopio Tektronix TDS1002B
Manual U (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/TDS1002 Manual.pdf
Manual P (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/TDS 100-1000-2000_prog.pdf
Manual U (local): \\Srvlabos\manuales\Tektronix\TDS1002 Manual.pdf
Manual P (local): \\Srvlabos\manuales\Tektronix\TDS 200-1000-2000_prog.pdf
"""

from __future__ import division, unicode_literals, print_function, absolute_import

import time

from matplotlib import pyplot as plt
import numpy as np
import visa

print(__doc__)

# Este string determina el intrumento que van a usar.
# Lo tienen que cambiar de acuerdo a lo que tengan conectado.
resource_name = 'USB0::0x0699::0x0363::C065089::INSTR'


rm = visa.ResourceManager()

osci = rm.open_resource(resource_name)

osci.query('*IDN?')

# Le pido algunos parametros de la pantalla, para poder escalear adecuadamente
xze, xin, yze, ymu, yoff = osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';')

# Modo de transmision: Binario
osci.write('DAT:ENC RPB')
osci.write('DAT:WID 1')

# Adquiere los datos del canal 1 y los devuelve en un array de numpy
data = osci.query_binary_values('CURV?', datatype='B', container=np.array)

tiempo = xze + np.arange(len(data)) * xin

plt.plot(tiempo, data)
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')


# Si vas a repetir la adquisicion muchas veces sin cambiar la escala
# es util definir una funcion que mida y haga las cuentas
def definir_medir(inst):
    xze, xin, yze, ymu, yoff = inst.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';')

    # creamos una function auxiliar
    def _medir():
        # Adquiere los datos del canal 1 y los devuelve en un array de numpy
        data = inst.query_binary_values('CURV?', datatype='B', container=np.array)

        tiempo = xze + np.arange(len(data)) * xin
        return tiempo, data
    
    # Devolvemos la funcion auxiliar que "sabe" la escala
    return _medir


medir = definir_medir(osci)
for n in range(10):
    tiempo, data = medir()
    plt.figure()
    plt.plot(tiempo, data)
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Voltaje [V]')
    time.sleep(.1)

osci.close()



