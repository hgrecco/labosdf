#code copied from:
#https://github.com/jrr1984/thorlabs_step_motors_ZST213B/blob/master/spectrometer/ccs200m.ipynb

#code requirements:
#0) Runs on python 3.6.3 (does not work on python 3.7)
#1) install through setup.py https://github.com/mabuchilab/Instrumental
#2) needs pyvisa, cffi (messy installation perhaps depending on OS)
# juanreto@gmail.com


import visa
rm = visa.ResourceManager()
rm.list_resources()

from instrumental import instrument,list_instruments
from instrumental.drivers.spectrometers.thorlabs_ccs import CCS


paramsets = list_instruments()
paramsets


ccs = instrument(paramsets[0])
ccs

ccs.get_device_info()

ccs.get_integration_time()

ccs.set_integration_time(integration_time='0.01 seconds', stop_scan=True)

ccs.stop_scan()

ccs.stop_and_clear()

ccs.reset()

ccs.start_single_scan()

ccs.is_data_ready()

ccs.take_data(integration_time=None, num_avg=1, use_background=False)

import matplotlib.pyplot as plt
#%matplotlib inline
plt.plot(x,y)
