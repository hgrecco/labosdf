

# Donde empezar:

# Lo mas fácil para usar Python científico es utilizar
# la distribución Anaconda (que incluye muchos paquetes).
# http://continuum.io/downloads#py34

# Tutorial generico: http://www.diveintopython3.net/
# Documentacion de Python: https://docs.python.org/3/
# Tutorial científico: https://scipy-lectures.github.io/

# Paquetes:
# - Rutinas numéricas: http://www.numpy.org/
#                      http://www.scipy.org/
# - Graficos: http://matplotlib.org/
# - Manejo de Unidades: http://pint.readthedocs.org/
# - Control de instrumentos: http://pyvisa.readthedocs.org/
#                           http://lantz.readthedocs.org/


# Llenar una lista de valores en un loop
xs = []
ys = []
for n in range(5, 10):
    xs.append(n)
    ys.append(n * n)

print('El largo de la lista es:')
print(len(xs))
print(xs)


# Transformar una lista en un array de NumPy
import numpy as np

xs = np.asarray(xs)
ys = np.asarray(ys)

print('El tamaño del array es')
print(xs.shape)


# Generar una vector equiespaciado
xs = np.linspace(1, 10, n=100)

# Generar un vector con ceros igual a otro para despues llenarlo (es mas eficiente)
ys = np.zeros_like(xs)

for n, x in enumerate(xs):
    ys[n] = x * x

# Poner todo en un array bidimensional
tabla = np.concatenate((xs, ys), axis=0)

# Guardar y leer datos en un csv (comma separated values)
np.savetxt('datos.csv', tabla, delimiter=',')
tabla_de_csv = np.loadtxt('datos.csv')

# Guardar y leer datos en un mat (archivo de matlab)
from scipy import io
# Como el archivo mat admite muchas tablas en el mismo archivo
# creo un diccionario que vincule un nombre (string) con el dato a grabarse
io.savemat('datos.mat', {'mitabla': tabla})
contenido_mat = io.loadmat('datos.mat')
print(contenido_mat)
tabla_mat = contenido_mat['mitabla']

# Guardar y leer datos en un npz (archivo de python)
# Como el archivo npz admite muchas tablas en el mismo archivo
# paso los datos p
np.savez('datos.npz', mitabla=tabla)
contenido_npz = io.loadmat('datos.mat')
print(contenido_mat)
tabla_npz = contenido_npz['mitabla']

# Plotear
import matplotlib.pyplot as plt
plt.plot(xs, ys)

# Con puntos
plt.scatter(xs, ys, '.')


# Generar un string unico para el nombre del archivo
for n in range(10):
    print('archivo%03d.txt' % n)

# Generar un string unico por fecha y hora
from datetime import datetime
print(datetime.now().isoformat())
# O un poco menos detallado
print(datetime.now().strftime('%Y%m%d_%H%M%S'))

# Pedir un dato al operador
s = input('Dame un numero: ')
# Convertir string en numero
valor = float(s)

# Esperar 2 segundos
import time
time.sleep(2)


# Finalmente para calcular el valor medio de un vector igual que para muchas otras cosas
# http://lmgtfy.com/?q=python+numpy+mean+value
