# -*- coding: utf-8 -*-
"""
Para mas informacion, ejecutar el siguiente comando en el sistema operativo:

    python -m visa info

Para una consola de instrumentacion, ejecutar el siguiente comando en el sistema operativo:

    python -m visa shell
"""
from __future__ import division, unicode_literals, print_function, absolute_import

print(__doc__)

try:
    import visa
except ImportError:
    print('PyVISA no esta instalado, ejecuta el siguiente comando en el sistema operativo\n\n'
          '     pip install -U pyvisa\n\n')
    import sys
    sys.exit(1)

rm = visa.ResourceManager()

print('Los instrumentatos/puertos detectados son:\n')
for name in rm.list_resources():
    print(repr(name))