# -*- coding: utf-8 -*-
"""
Multimetro HP 34401
Manual (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/Agilent 34401.pdf
Manual (local): \\Srvlabos\manuales\Agilent\Agilent 34401.pdf
"""

from __future__ import division, unicode_literals, print_function, absolute_import

import visa

print(__doc__)

# Este string determina el intrumento que van a usar.
# Lo tienen que cambiar de acuerdo a lo que tengan conectado.
resource_name = 'GPIB0::22::INSTR'


rm = visa.ResourceManager()

mult = rm.open_resource(resource_name)

print(mult.query('*IDN?'))

dc = mult.query_ascii_value('MEASURE:VOLTAGE:DC?')

print(dc)

mult.close()

# otras cosas que se pueden medir
#  MEASure
#   :VOLTage:DC? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
#   :VOLTage:DC:RATio? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
#   :VOLTage:AC? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
#   :CURRent:DC? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
#   :CURRent:AC? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
#   :RESistance? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
#   :FRESistance? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
#   :FREQuency? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
#   :PERiod? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
#   :CONTinuity?
#   :DIODe?


