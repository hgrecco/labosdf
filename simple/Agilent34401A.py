# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals, print_function, absolute_import

from matplotlib import pyplot as plt
import numpy as np

import visa

rm = visa.ResourceManager()

print(rm.list_resources())

resource_name = 'GPIB0::22::INSTR'
mult = rm.open_resource(resource_name)

mult.query('*IDN?')

dc = float(mult.query('measure:voltage:DC?'))

mult.close()

# Otras cosas que se pueden medir
# 
# MEASure
#     :VOLTage:DC? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
#     :VOLTage:DC:RATio? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
#     :VOLTage:AC? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
#     :CURRent:DC? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
#     :CURRent:AC? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
#     :RESistance? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
#     :FRESistance? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
#     :FREQuency? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
#     :PERiod? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
#     :CONTinuity?
#     :DIODe?






