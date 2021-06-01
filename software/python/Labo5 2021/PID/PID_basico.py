# -*- coding: utf-8 -*-
"""
Created on Wed May  5 01:56:43 2021
@author: damian
Comandos implementados en la placa:
V###.### ó v###.###:    establece la tensión de salida del controlador.
                        valor usado por el controlador para fijar la modulación por ancho de pulso: PWM = 0,5 (1+Vsalida/Vmaxima).
R####### ó R#######:    fija la resolución del encoder.
                        solo se usa para transformar los puloss a grados pero no esta implementado.
M###.### ó m###.###:    establece la máxima tesion soportada por el motor.
                        valor usado por el controlador para fijar la modulación por ancho de pulso: PWM = 0,5 (1+Vsalida/Vmaxima).
X ó x:                  reinicia la placa.
"""
import serial
import time
import numpy as np
import matplotlib.pyplot as plt

#%% Iniciar controlador serie
ser = serial.Serial(port='COM6', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=0.005, xonxoff=0, rtscts=0)
ser.close() 
ser.open()

#reset controlador
ser.write(bytes('X','utf-8')) 
time.sleep(0.01)
ser.flushInput()

#escribo voltaje, pregunto posicion y velocidad
str = 'V0\n\r'
ser.write(bytes(str,'utf-8'))
time.sleep(0.002)
s = ser.readline(25)
print(s)

#%% Defino funciones de comunicacion con el controlador

def setVoltageGetData(puerto,voltaje):
    puerto.flushInput()
    str = 'V%f\n\r' % (voltaje)
    puerto.write(bytes(str,'utf-8'))
    time.sleep(0.002)
    s = puerto.readline(25)
    pos = float(s[0:9])
    vel = float(s[10:23])  
    return pos,vel

def resetControlador(puerto):
    puerto.write(bytes('X','utf-8')) 
    time.sleep(0.01)
    puerto.flushInput()

def voltajeCorregido(voltaje):
    voltpos = 2
    voltneg = 2 
    maxvolt = 12
    if(voltaje > 0 ):        
        voltaje *= maxvolt/(maxvolt+voltpos)
        voltaje += voltpos
    else:        
        voltaje *= maxvolt/(maxvolt+voltneg)
        voltaje -= voltneg
    return voltaje

#%% Respuesta a un pulso de voltaje

#reseteo el controlador    
resetControlador(ser)
time.sleep(0.2)

#inicializo variables
voltajes = np.concatenate((0*np.ones(10) ,5*np.ones(50), 0*np.ones(140)))
N = len(voltajes)
posiciones = np.zeros(N)
posiciones[:] = np.nan
velocidades=np.zeros(N)
velocidades[:] = np.nan
tiempos=np.zeros(N)
tiempos[:] =np.nan

#loop poniendo voltaje y midiendo posicion y velocidad
toc = time.time()
for i in range(N):    
    pos,vel = setVoltageGetData(ser,voltajes[i]) 
    posiciones[i] = pos
    velocidades[i] = vel
    tiempos[i] = time.time()-toc

#plot de la salida
plt.close('all')
fig, axs = plt.subplots(3, sharex=True)
axs[0].plot(tiempos, voltajes,'.-')
axs[0].set(ylabel = 'Voltaje')
axs[1].plot(tiempos, posiciones,'.-')
axs[1].set(ylabel = 'Posición')
v2 = np.diff(posiciones) / np.diff(tiempos) /256
axs[2].plot(tiempos[:-1], v2,'.-')
axs[2].plot(tiempos, velocidades,'.-')
axs[2].set(ylabel = 'Velocidad')
plt.legend(('Medida por la PC','Pedida por la placa'))
plt.xlabel('Tiempo [s]')


