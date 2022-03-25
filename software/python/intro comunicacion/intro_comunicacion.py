import visa
import numpy as np
import time
import matplotlib.pyplot as plt

# inicializo comunicacion con equipos
rm = visa.ResourceManager()
#lista de dispositivos conectados, para ver las id de los equipos
rm.list_resources()

#inicializo generador de funciones
fungen = rm.open_resource('USB0::0x0699::0x0346::C034198::INSTR')
#le pregunto su identidad
fungen.query('*IDN?')
#le pregunto la freq
fungen.query('FREQ?')
#le seteo la freq
fungen.write('FREQ 2000')
fungen.query('FREQ?')
#le pregunto la amplitud
fungen.query('VOLT?')
#le seteo la amplitud
fungen.write('VOLT 2')
fungen.query('VOLT?')
#le pregunto si la salida esta habilitada
fungen.query('OUTPut1:STATe?')
#habilito la salida
fungen.write('OUTPut1:STATe 1')
fungen.query('OUTPut1:STATe?')
#le pregunto la impedancia de carga seteada
fungen.query('OUTPUT1:IMPEDANCE?')



#inicializo el osciloscopio
osci = rm.open_resource('USB0::0x0699::0x0363::C102223::INSTR')
#le pregunto su identidad
osci.query('*IDN?')
#le pregunto la conf del canal (1|2)
osci.query('CH1?')
#le pregunto la conf horizontal
osci.query('HOR?')
#le pregunto la punta de osciloscopio seteada
osci.query('CH2:PRObe?')


#Seteo de canal
channel=1
scale = 5
osci.write("CH{0}:SCA {1}".format(channel, scale))
osci.query("CH{0}:SCA?".format(channel))
"""escalas Voltaje (V) ojo estas listas no son completas
2e-3
5e-3
10e-3
20e-3
50e-3
100e-3
5e-2
10e-2
"""

zero = 0
osci.write("CH{0}:POS {1}".format(channel, zero))
osci.query("CH{0}:POS?".format(channel))

channel=2
scale = 2e-1
osci.write("CH{0}:SCA {1}".format(channel, scale))
osci.write("CH{0}:POS {1}".format(channel, zero))

#seteo escala horizontal
scale = 200e-6
osci.write("HOR:SCA {0}".format(scale))
osci.write("HOR:POS {0}".format(zero))	
osci.query("HOR?")
"""
escalas temporales (s)

10e-9
25e-9
50e-9
100e-9
250e-9
500e-9
1e-6
2e-6
5e-6
10e-6
25e-6
50e-6

"""


#le pido los valores de la pantalla (0:255)
data = osci.query_binary_values('CURV?', datatype='B',container=np.array)
plt.plot(data)

#le pido los parametros de la pantalla
xze, xin, yze, ymu, yoff = osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';') 
xze
xin
#voltaje = (data - yoff) * ymu + yze 
#tiempo = xze + np.arange(len(data)) * xin



# Conexion usando clases
from instrumental import AFG3021B
from instrumental import TDS1002B

#osciloscopio
osci = TDS1002B('USB0::0x0699::0x0363::C102223::INSTR')
osci.get_time()
osci.set_time(scale = 1e-3)
osci.set_channel(1,scale = 2)
tiempo, data = osci.read_data(channel = 1)
plt.plot(tiempo,data)
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')

#generador de funciones
fungen = AFG3021B(name = 'USB0::0x0699::0x0346::C034198::INSTR')
fungen.getFrequency()

#barrido de frecuencia
for freq in range(1000,5000,1000):
    print(freq)
    fungen.setFrequency(freq)
    time.sleep(0.1)
    tiempo, data = osci.read_data(channel = 1)
    plt.plot(tiempo,data)
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Voltaje [V]')