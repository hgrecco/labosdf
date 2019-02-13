# -*- coding: utf-8 -*-
#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc
import os
import scipy.optimize as opt
import scipy.stats as stats
import pathlib

from instrumentos import Osciloscopio


# Abajo de todo hay ejemplos de como usar algunas funciones

def adquirir_y_graficar(osci):
    """
    Adquiere una pantalla de osciloscopio y grafica los datos

    :param osci: objeto de tipo Osciloscopio
    """
    tiempo, data = osci.get_ventana(1)
    plt.figure()
    plt.plot(tiempo, data)

    return tiempo, data


def adquirir_y_guardar(osci, path, filename):
    """
    Adquiere una pantalla de osciloscopio y guarda los datos en formato csv.

    :param osci: objeto de tipo osciloscopio
    :param path: string con la ruta donde guardar los datos.
    :param filename: string con el nombre que va a tener el archivo.
    """
    os.chdir(path)
    tiempo, data = osci.get_ventana(1)
    np.savetxt(filename, np.vstack((tiempo, data)).T, delimiter=',')  # Guarda los datos crudos, separados por ","

    return tiempo, data


def adquirir_guardar_multiples(osci, path, n):
    """
    Adquiere n pantallas y las guarda como csv.

    :param osci: objeto de tipo osciloscopio
    :param path: string con la ruta donde guardar los datos.
    :param n: numero de pantallas a adquirir
    """
    for i in range(n):
        filename = "medicion_{0}.csv".format(n)
        adquirir_y_guardar(osci, path, filename)


def adquirir_cuentas_eventos(osci, path, n, thres=-5e-3):
    """
    Adquiere n pantallas y guarda solo los eventos (valores de tension detectados como minimos) y cuentas (cantidad
    de minimos por pantalla)

    :param osci: objeto de tipo instrumentos.Osciloscopio
    :param path: string con la ruta donde guardar los datos.
    :param n: numero de mediciones a realizar.
    :param thresh: umbral de tension. Tensiones mayores a este valor (del PMT, que observa tensiones negativas) son
    **ruido**
    """

    os.chdir(path)

    cuentas = list()
    eventos = list()

    for i in range(n):
        filename = "medicion_{0}.csv".format(n)
        tiempo, data = adquirir_y_guardar(osci, path, filename)

        minimos = (np.diff(np.sign(np.diff(data))) > 0).nonzero()[0] + 1
        # Elimino tensiones positivas, recodar que la señal del PMT es negativa
        for m in minimos:
            if data[m] < thres:
                eventos.append(data[m])
        cuentas.append(data[data[minimos, 1] < thres].shape[0])  # Calculo la cantidad de minimos que hubo en una medicion

    np.savetxt("eventos.csv", eventos, delimiter=',')
    np.savetxt("cuentas.csv", cuentas, delimiter=',')


def generar_cuentas_eventos(mediciones_path, thres=-5e-3):
    """
    Abre todos los archivos .csv de la carpeta mediciones_path. Luego calcula minimos para cada csv y guarda en una
    nueva tabla de datos la cantidad de minimos por medicion.

    :param mediciones_path: Carpeta donde estan guardadas las mediciones en crudo, en formato csv.
    :param thres: Umbral para la deteccion de minimos
    :return:
    """
    mediciones_path = pathlib.Path(mediciones_path)
    mediciones = list(mediciones_path.glob('*.csv'))

    cuentas = list()
    eventos = list()
    for med in mediciones:
        data = np.loadtxt(med, delimiter=',')
        minimos = (np.diff(np.sign(np.diff(data[:,1]))) > 0).nonzero()[0] + 1
        cuentas.append(data[data[minimos,1] < thres].shape[0]) # Calculo la cantidad de minimos que hubo en una medicion

        for m in minimos:
            if data[m] < thres:
                eventos.append(data[m])
    # Crear carpeta ./histograma/ y guardar
    histograma_path = mediciones_path / "histograma"
    histograma_path.mkdir(exist_ok=True)

    np.savetxt(histograma_path / "cuentas.csv", cuentas, fmt='%i', delimiter=',')
    np.savetxt(histograma_path / "eventos.csv", eventos, fmt='%i', delimiter=',')

    return cuentas, eventos


def correlacion(dataPath):
    data = np.loadtxt(dataPath, delimiter=',')
    data = data[:]

    autocorre = np.correlate(data[:,1], data[:,1], mode="same")
    
    plt.plot(data[:,0], data[:,1])
    plt.figure()
    plt.plot(autocorre)
    plt.xlabel("t[s]")
    plt.ylabel('Amp[V]')
    plt.show()


def histograma(path):
    
    ### Datos ###
    os.chdir(path)      
    rawData = np.loadtxt('cuentas.csv', delimiter=',') # carga cuentas.csv. Guardar con savetxt
    data = rawData[rawData < 20] # Aca podés eliminar cuentas muy altas, producto de malas mediciones
    data.sort()
    ###
    ### Histograma ###
    hist, bins = np.histogram(data,bins = np.arange(np.max(data)), density = True)
    bins = bins[:-1]
    ###
    ### Ajuste ###
    ### Fuciones de ayuda ###
    poissonPDF = lambda j, lambd: (lambd**j) * np.exp(-lambd) / scipy.misc.factorial(j)
    bePDF = lambda j, lambd: np.power(lambd, j) / np.power(1+lambd,1+j)
    ###
    pPoisson, pconv = opt.curve_fit(poissonPDF, bins, hist, p0 = 3)
    pBE, pconv = opt.curve_fit(bePDF, bins, hist, p0 = 3)
    with open('p-valor','w+') as f:
        f.write("Poisson p-value: {}\n".format(stats.chisquare(hist,poissonPDF(bins,pPoisson),ddof = 1)[1]))
        f.write("BE p-value: {}".format(stats.chisquare(hist,bePDF(bins,pBE),ddof = 1)[1]))
    ######
    
    ### Ploteo ###
    width = 24 / 2.54 #24cm de ancho
    figSize = (width * (1+np.sqrt(5)) / 2, width) #relación aurea
    
    #Figura 1    
    plt.figure(figsize=figSize)
    plt.plot(poissonPDF(bins,pPoisson), 'r^', label='Poisson', markersize = 10) #azul
    plt.plot(bePDF(bins,pBE), 'go', label = 'BE', markersize = 10) #verde
    plt.bar(bins,hist, width = 0.1,label='Datos')    
    #Configuración
    plt.grid()
    ### Ejes ###
    plt.axis('tight')
    plt.xlim((-1,10))
    plt.ylim((0,0.25))
    plt.xlabel('Numero de eventos',fontsize=22)
    plt.ylabel('Frecuencias relativas',fontsize=22)
    plt.tick_params(labelsize = 20)
    ###
    ### Texto a agregar ###
    text = 'Poisson\n'
    text += r'$<n> = {0:.2f}$'.format(pPoisson[0])
    text += '\n'
    text += r'$\chi^2_{{ \nu = {0} }} = {1:.3f}$'.format(hist.size, poissonChisq)
    text += '\n\n'
    text += 'BE\n'
    text += r'$<n> = {0:.2f}$'.format(pBE[0])
    text += '\n'
    text += r'$\chi^2_{{ \nu = {0} }} = {1:.2f}$'.format(hist.size, beChisq)
    plt.text(0.7,0.3, text, transform = plt.gca().transAxes, fontsize = fontSize)
    ######
    plt.legend(loc=0,fontsize=20)
    plt.savefig('histograma.png', bbox_inches = 'tight')
    
    #Figura 2
    plt.figure(2,figsize=figSize)
    plt.plot(np.log(poissonPDF(bins,pPoisson)), 'r^', label='Log(Poisson)', markersize = 10) #azul
    plt.plot(np.log(bePDF(bins,pBE)), 'go', label = 'Log(BE)', markersize = 10) #verde
    plt.plot(bins,np.log(hist),'bd',label='Log(Datos)', markersize = 10)    
    #### Configuración ####
    plt.grid()
    ### Ejes ###
    plt.axis('tight')
    plt.xlim((-1,10))
    plt.ylim((-5,-1))
    plt.xlabel('Numero de eventos',fontsize=22)
    plt.ylabel('Log(Frecuencias relativas)',fontsize=22)
    plt.tick_params(labelsize = 20)
    ###
    plt.legend(loc=0,fontsize=20)
    ########
    plt.savefig('log_histograma.png', bbox_inches = 'tight')

if __name__ == "__main__":
    # Ejemplo de la utilizacion de estas funciones:

    osci = Osciloscopio('USB0::0x0699::0x0363::C065087::INSTR')
    path = r"D:\Alumnos\Grupo N\Conteo"
    N = 10

    # Adquirimos con los valores por defecto:
    adquirir_datos(osci, path, N)

    # Y ahora adquirimos cambiando algunos parametros y calculando eventos y cuentas:
    path = r"D:\Alumnos\Grupo N\Conteo\Escala nueva"
    adquirir_datos(osci, path, N, escala_temporal=200E-6, escala_tension=30E-3, guardar_eventos=True)