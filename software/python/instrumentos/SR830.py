# -*- coding: utf-8 -*-
"""
LOCKIN Tektronix SR830
Manual (web): http://www.thinksrs.com/downloads/PDFs/Manuals/SR830m.pdf
Manual (local): \\Srvlabos\manuales\Standford\SR830m.pdf
"""

from __future__ import division, unicode_literals, print_function, absolute_import

import visa

print(__doc__)

# Este string determina el intrumento que van a usar.
# Lo tienen que cambiar de acuerdo a lo que tengan conectado.
resource_name = 'GPIB0::8::INSTR'


rm = visa.ResourceManager()

lockin = rm.open_resource(resource_name)

# Pide indentificacion
print(lockin.query('*IDN?'))

# Lee las salidas una a la vez
# X=1, Y=2, R=3, T=4
x = lockin.query_ascii_values('OUTP ?1')
y = lockin.query_ascii_values('OUTP ?2')
r = lockin.query_ascii_values('OUTP ?3')
t = lockin.query_ascii_values('OUTP ?4')

print(x, y, r, t)

# O bien todas juntas
xyrt = lockin.query_ascii_values('SNAP ? 1,2,3,4')

print(xyrt)

# Cambia el voltaje en la salida auxiliar
# El primer numero es la salida y el segundo es el voltaje
lockin.write('AUXV 0, 4.32')


lockin.close()
