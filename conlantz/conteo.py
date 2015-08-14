# -*- coding: utf-8 -*-

import numpy as np
from scipy import signal

import visa

from tds1002b import TDS1002B

# Listo los VISA resources disponibles
rm = visa.ResourceManager()
print(rm.list_resources())

#: VISA Resources Reemplazar por el que tengas
resource_name = 'USB0::0x0699::0x0363::C065089::INSTR'

#: Numero de pantallas a tomar
repeticiones = 20

#: Indica si deber
plotear = False

#: Cuanta de eventos por pantalla
eventos = []

#: Altura de picos
amplitudes = []

# Abro la sesion con el osciloscopio
with TDS1002B(resource_name) as osc:

    # Levanto n pantallas y en cada una registro el número de máximos
    for i in range(repeticiones):

        tiempo, voltaje = osc.acquire_curve()

        # Busco máximos
        peakind = signal.find_peaks_cwt(voltaje, np.arange(0.1,1), min_snr=50)

        eventos.append(np.size(peakind))

        amplitudes.extend((voltaje[j] for j in peakind) )


#%% Histogramas
if plotear:
    import matplotlib.pyplot as plt

    tiempo, voltaje = osc.acquire_curve()
    plt.plot(tiempo, voltaje, '.')
    plt.show()

    # Para hacer un histograma de eventos:
    plt.hist(eventos)
    plt.show()

    # Para hacer un histograma de amplitudes (para sacar la tensión umbral, por ejemplo)

    plt.hist(amplitudes)
    plt.show()
