# -*- coding: utf-8 -*-
"""
Protek 506

 El multimetro Protek 506 se comunica con la compu a travis de un puerto
 serie (DB9). El multimetro devuelve la lectura que muestra en pantalla
 cada vez que desde el puerto serie recibe algo (puede ser un caracter
 en blanco). En este ejemplo esta seteado para leer temperatura con una
 termocupla, por lo que el string que devuelve el multimetro es
 'TEMP 33,2'. De ahi el programa extrae el valor de temperatura y lo
 guarda en una variable

Manual (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/Agilent 34401.pdf
Manual (local): \\Srvlabos\manuales\Agilent\Agilent 34401.pdf
"""

import time

import visa

print(__doc__)

# Este string determina el intrumento que van a usar.
# Lo tienen que cambiar de acuerdo a lo que tengan conectado.
resource_name = 'ASRL1::INSTR'

rm = visa.ResourceManager()


mult = rm.open_resource(resource_name,
                        baudrate=1200, data_bits=7, stop_bits=visa.constants.StopBits.two,
                        parity=visa.constants.Parity.none,
                        write_termination='\n')

mediciones = []

for n in range(5):
    result = mult.query('')
    mediciones.append((time.time(), float(result[4:])))

print(mediciones)

mult.close()
