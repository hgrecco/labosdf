# -*- coding: utf-8 -*-
"""
Este programa muestra como controlar el motor por pasos:
Tiene 3 partes:
    - Codigo de para llamar a la libreria NI-DAQmx (bajo nivel)
    - Clase que abstrae el funcionamiento del motor por pasos
    - Ejemplo de uso
"""

import time


# ---- Codigo de para llamar a la libreria NI-DAQmx ----
# Esta seccion existe hasta que exista una buena libreria para Python 3
# que use DAQmx.

# Es de mas bajo nivel y no es necesario entenderla para saber que hace
# el programa.

import ctypes
try:
    nidaq = ctypes.windll.nicaiu
except:
    raise Exception("No se pudo abrir la libreria DAQmx")


def CHK(err, msg=''):
    """Recibe la respuesta de la DAQ y si es un error,
    busca el texto que lo describe.
    """
    if err < 0:
        buf_size = 100
        buf = ctypes.create_string_buffer(b'\000' * buf_size)
        nidaq.DAQmxGetErrorString(err,ctypes.byref(buf),buf_size)
        m = 'nidaq call failed with error %d: %s' % (err, repr(buf.value))
        if msg:
            msg = m + '\n' + msg
        raise RuntimeError(m)


class DigitalOutput:

    def __init__(self, device):
        self.task = ctypes.c_uint32(0)

        # Usando una tarea existente
        # int32 DAQmxLoadTask (const char taskName[], TaskHandle *taskHandle);
        # out = nidaq.DAQmxLoadTask(b"MotorTask", ctypes.byref(self.task))
        # if out < 0:
        #    raise Exception("No se pudo encontrar una tarea llamada MotorTask.\n"
        #                    "Usando el NI-MAX Measurement and Automation crea"
        #                    "un task con 4 digital outputs (Error %s. Ver NIDAQmx.h)" % out)

        # int32 DAQmxCreateTask (const char taskName[], TaskHandle *taskHandle);
        CHK(nidaq.DAQmxCreateTask(b"", ctypes.byref(self.task)))


        if isinstance(device, int):
            device = "Dev%d/port0/line0:3" % device

        # int32 DAQmxCreateDOChan (TaskHandle taskHandle, const char lines[],
        #                          const char nameToAssignToLines[], int32 lineGrouping);
        CHK(nidaq.DAQmxCreateDOChan(self.task, bytes(device, "utf-8"), b"", 1),
            "Es posible que la placa de adquisición no este conectada o el numero de dispositivo "
            "sea incorrecto. Verificalo con el NI-MAX Measurement and Automation.")

        CHK(nidaq.DAQmxStartTask(self.task))

    def set(self, valores):
        DAQmx_Val_GroupByChannel = 0
        FourIntegers = ctypes.c_uint8 * 4
        data = FourIntegers(*valores)

        # Sintaxis de la funcion en la libreria.
        # int32 DAQmxWriteDigitalLines(TaskHandle taskHandle, int32 numSampsPerChan, bool32 autoStart, float64 timeout
        #                              bool32 dataLayout, 
        #                              uInt8 writeArray[], int32 *sampsPerChanWritten, bool32 *reserved);
        CHK(nidaq.DAQmxWriteDigitalLines(self.task, ctypes.c_int32(1), ctypes.c_uint32(1), ctypes.c_double(10.0), 
                                         DAQmx_Val_GroupByChannel,
                                         data, None, None))
        
    def __del__(self):
        CHK(nidaq.DAQmxStopTask(self.task))
        CHK(nidaq.DAQmxClearTask(self.task))


### --- Clase que abstrae el funcionamiento del motor por pasos ----

# El objeto motor lleva la cuenta de los pasos dados.
# Esto permite mover a posiciones absolutas una vez definida
# la posicion actual. Si se borra el objeto motor entre una
# medicion y la siguiente hay que volver a definir la posicion
# actual.

# Ademas para un dado motor paso a paso no queremos crear mas de una
# instancia del objeto Motor porque:
# - usarian el mismo recurso (DAQ)
# - cada uno llevaria una cuenta independiente de los pasos dados.

# Al utilizar spyder, el "workspace" tiene memoria de los objetos
# creados.

# La forma usual seria crear un registro de los objetos creados
# y devolver el objeto existente en un modulo que se importa.
# Pero es comun usando Spyder poner todo en un solo archivo.
# lo que sigue es una forma evitar crear muchos objetos motor
# y no es relevante para entender la adquisicion.
try:
    _MOTOR_INSTANCES
except NameError:
    _MOTOR_INSTANCES = {}


class Motor:

    # Secuencia del motor a utilizar. Puede cambiar para otro tipo de motor.
    SECUENCIA = ((True, True, True, True),
                 (True, False, True, False),
                 (True, False, False, True),
                 (False, True, False, True),
                 (False, True, True, False))
                 
    # Tiempo de espera en segundos despues de dar el paso.
    ESPERA = .1

    def __new__(cls, device, posicion_actual=0):

        if device in _MOTOR_INSTANCES:
            return _MOTOR_INSTANCES[device]

        _MOTOR_INSTANCES[device] = obj = super().__new__(cls)

        # Posicion absoluta
        obj.posicion = posicion_actual
        
        # Numero de paso del motor dentro de la secuencia.
        obj._paso_motor = 0
      
        obj._do = DigitalOutput(device)

        obj._actualizar_do()

        return obj
    
    def _actualizar_do(self):
        """Actualiza los valores de la salida digital.
        """
        
        self._do.set(self.SECUENCIA[self._paso_motor])
        time.sleep(self.ESPERA)
        
    def anterior(self):
        """Mueve el motor un paso hacia atras y devuelve la nueva posicion.
        """
        
        self.posicion -= 1
        self._paso_motor -= 1
        if self._paso_motor < 0:
            self._paso_motor = len(self.SECUENCIA) - 1
            
        self._actualizar_do()
        
        return self.posicion
        
    def siguiente(self):
        """Mueve el motor un paso hacia adelante y devuelve la nueva posicion.
        """

        self.posicion += 1

        self._paso_motor += 1
        if self._paso_motor == len(self.SECUENCIA):
            self._paso_motor = 0
            
        self._actualizar_do()  
        
        return self.posicion
    
    def _iter(self, pasos):
        """Itera una cantidad de pasos (hacia adelante o atras segun el signo)
        Hace un yield de la nueva posicion en cada paso.
        """
        if pasos == 0:
            raise StopIteration
        
        if pasos > 0:
            fun = self.siguiente
        else:
            fun = self.anterior
            
        for n in range(1, pasos + 1):
            yield fun()
   
    def mover(self, destino):
        """Mueve el motor a una nueva posicion absoluta.
        """
        self._iter(destino - self.posicion)
        return self.posicion
        
    def barrer(self, desde, hasta):
        """Barre desde una posicion hasta otra.
        Hace un yield de la nueva posicion en cada paso
        """
        yield self.mover(desde)
        for posicion in self._iter(hasta - desde):
            yield posicion


### ---- Ejemplo de uso ----
# Esta seccion solo se ejecuta cuando se corre el programa como Script
# (si se importa no se ejecuta)

if __name__ == '__main__':

    motor = Motor(device=8)

    # Barrer un rango (en posiciones absolutas)
    for posicion in motor.barrer(5, 20):
        print("La posicion es %s" % posicion)
        # Aca podrias hacer algo.

    # Avanzar 10 pasos (relativos a la posicion actual)
    for n in range(10):
        motor.siguiente()

    print('La posicion actual es: %d' % motor.posicion)

    # Define cual es la posicion absoluta actual
    pos = input('Cual es la posicion actual (default %d)? ' % motor.posicion)
    if pos is not None:
        motor.posicion = int(pos)

    print('La posicion actual es: %d' % motor.posicion)
