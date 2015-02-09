# -*- coding: utf-8 -*-
"""
Fuente Hantek PPS2320A
manufacturer: http://www.hantek.com.cn/en/ProductDetail_32.html
Manual (local): \\Srvlabos\manuales\Agilent\Agilent 34401.pdf
"""

from __future__ import division, unicode_literals, print_function, absolute_import

import visa

print(__doc__)


# Este string determina el intrumento que van a usar.
# Lo tienen que cambiar de acuerdo a lo que tengan conectado.
resource_name = 'ASRL3::INSTR'


rm = visa.ResourceManager()

fuente = rm.open_resource(resource_name, write_termination='\n')

# query idn
print(fuente.query('a'))

# pregunta voltaje CH1
sal = fuente.query_ascii_value('rv')

print(sal)

# setea corriente CH1
fuente.write('si1000')

# setea voltaje CH1
fuente.write('su1200')

# sets voltage of CH1 12V
fuente.write('su1200')

# sets current of CH1 10A
fuente.write('si1000')

# sets voltage of CH2 1V
fuente.write('sa0100')

# sets current of CH2 0.2AV
fuente.write('sd0020')

fuente.close()


"""
Send Command Word	Perform Operation
a + line break (Hereafter, every command must take 0x0a as the line break to over, ignore the following)	Back to device model
suXXXX	CH1 preset output voltage, units V; e.g. 1200 stands for 12.00V
siXXXX 	CH1 preset output current, units A; e.g. 2500 stands for 2.500A
saXXXX	CH2 preset output voltage, units V; e.g. 1200 stands for 12.00V
sdXXXX	CH2 preset output current, units A; e.g. 2500 stands for 2.500A
O0	Output indicator light switch-off
O1	Output indicator light switch-on
O2	Parallel, series, trace, output indicator light switch-off
O3	Series, trace, output indicator switch-off; Parallel indicator light switch-on
O4	Parallel, trace, output indicator switch-off; Series indicator light switch-on
O5	Parallel, series, output indicator switch-off; Trace indicator light switch-on
O6	CH1 indicator light switch-on
O7	CH2 indicator light switch-on
O8	CH3 3.3V indicator light switch-on
O9	CH3 5V indicator light switch-on
Oa	CH3 2.5V indicator light switch-on
rv	Read the measured voltage of CH1
ra	Read the measured current of CH1
ru	Read the preset voltage of CH1
ri	Read the preset current of CH1
rh	Read the measured voltage of CH2
rj	Read the measured current of CH2
rk	Read the preset voltage of CH2
rq	Read the preset current of CH2
rm	Read the device working mode
rl	Read lock state
rp	Read CH2 state
rs	Read CH1 state
rb	Read CH3 state
	
"""
