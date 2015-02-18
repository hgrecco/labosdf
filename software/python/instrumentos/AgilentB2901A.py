# -*- coding: utf-8 -*-
"""
Fuente Agilent B2901A
manufacturer: http://www.hantek.com.cn/en/ProductDetail_32.html
Manual Usuario (local): \\Srvlabos\manuales\HP-Agilent\B2901A\B2910-90010.pdf
"""

from __future__ import division, unicode_literals, print_function, absolute_import

import visa

print(__doc__)


# Este string determina el intrumento que van a usar.
# Lo tienen que cambiar de acuerdo a lo que tengan conectado.
resource_name = 'USB0::0x0957::0x8B18::MY51140178::INSTR'

rm = visa.ResourceManager()

inst = rm.open_resource(resource_name, write_termination='\n')

# query idn
print(inst.query('*IDN?'))

# Ultimos valores medidos de 
# Voltage, corriente, resistencia, tiempo, status, source ouput setting
print(inst.query_ascii_values(':READ:SCALar?'))


inst.close()


