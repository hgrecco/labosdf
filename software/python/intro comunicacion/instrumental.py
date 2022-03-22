import visa
import numpy as np
import time

class HantekPPS2320A:
    """
    Fuente DC
    Send Command Word	Perform Operation
    a + line break (Hereafter, every command must take 0x0a as the line break to over, ignore the following)	Back to device model
    suXXXX	CH1 preset output voltage, units V; e.g. 1200 stands for 12.00V
    siXXXX 	CH1 preset output current, units A; e.g. 2500 stands for 2.500A
    saXXXX	CH2 preset output voltage, units V; e.g. 1200 stands for 12.00V
    sdXXXX	CH2 preset output current, units A; e.g. 2500 stands for 2.500A
    O0	Output indicator light switch-off
    O1	Output indicator light switch-on
    O2	Parallel, series, trace, output indicator light switch-off
    O3	Series, trace, output indicator switch-off; Parallel indicator light switch-on
    O4	Parallel, trace, output indicator switch-off; Series indicator light switch-on
    O5	Parallel, series, output indicator switch-off; Trace indicator light switch-on
    O6	CH1 indicator light switch-on
    O7	CH2 indicator light switch-on
    O8	CH3 3.3V indicator light switch-on
    O9	CH3 5V indicator light switch-on
    Oa	CH3 2.5V indicator light switch-on
    rv	Read the measured voltage of CH1
    ra	Read the measured current of CH1
    ru	Read the preset voltage of CH1
    ri	Read the preset current of CH1
    rh	Read the measured voltage of CH2
    rj	Read the measured current of CH2
    rk	Read the preset voltage of CH2
    rq	Read the preset current of CH2
    rm	Read the device working mode
    rl	Read lock state
    rp	Read CH2 state
    rs	Read CH1 state
    rb	Read CH3 state	
    """    
    def __init__(self, resource):
        self._fuente = visa.ResourceManager().open_resource(resource)
        print(self._fuente.query('*IDN?'))
                
    def set_voltage1(self, value):
        if value > 3:
            raise ValueError("El valor no puede ser mayor que 3")
        self._fuente.write("su{0:04d}".format(round(value*100)))


class SR830(object):
    '''Clase para el manejo amplificador Lockin SR830 usando PyVISA de interfaz'''
    
    def __init__(self,resource):
        self._lockin = visa.ResourceManager().open_resource(resource)
        print(self._lockin.query('*IDN?'))
        self._lockin("LOCL 2") #Bloquea el uso de teclas del Lockin
        
    def __del__(self):
        self._lockin("LOCL 0") #Desbloquea el Lockin
        self._lockin.close()
        
    def setModo(self, modo):
        '''Selecciona el modo de medición, A, A-B, I, I(10M)'''
        self._lockin.write("ISRC {0}".format(modo))
        
    def setFiltro(self, sen, tbase, slope):
        '''Setea el filtro de la instancia'''
        #Página 90 (5-4) del manual
        self._lockin.write("OFLS {0}".format(slope))
        self._lockin.write("OFLT {0}".format(tbase)) 
        self._lockin.write("SENS {0}".format(sen)) 
        
    def setAuxOut(self, auxOut = 1, auxV = 0):
        '''Setea la tensión de salida de al Aux Output indicado.
        Las tensiones posibles son entre -10.5 a 10.5'''
        self._lockin.write('AUXV {0}, {1}'.format(auxOut, auxV))
            
    def setReferencia(self,isIntern, freq, vRef = 1):
        if isIntern:
            #Referencia interna
            #Configura la referencia si es así
            self._lockin.write("FMOD 1")
            self._lockin.write("SLVL {0:f}".format(voltaje))
            self._lockin.write("FREQ {0:f}".format(freq))
        else:
            #Referencia externa
            self._lockin.write("FMOD 0")
            
    def setDisplay(self, isXY):
        if isXY:
            self._lockin.write("DDEF 1, 0") #Canal 1, x
            self._lockin.write('DDEF 2, 0') #Canal 2, y
        else:
            self._lockin.write("DDEF 1,1") #Canal 1, R
            self._lockin.write('DDEF 2,1') #Canal 2, T
    
    def getDisplay(self):
        '''Obtiene la medición que acusa el display. 
        Es equivalente en resolución a la medición de los parámetros con SNAP?'''
        orden = "SNAP? 10, 11"
        return self._lockin.query_ascii_values(orden, separator=",")
        
    def getMedicion(self,isXY = True):
        '''Obtiene X,Y o R,Ang, dependiendo de isXY'''
        orden = "SNAP? "
        if isXY:
            self._lockin.write("DDEF 1,0") #Canal 1, XY
            orden += "1, 2" #SNAP? 1,2
        else:
            self._lockin.write("DDEF 1,1") #Canal 1, RTheta
            orden += "3, 4" #SNAP? 3, 4
        return self._lockin.query_ascii_values(orden, separator=",")
		
class AFG3021B:
    
    def __init__(self, name='USB0::0x0699::0x0346::C034165::INSTR'):
        self._generador = visa.ResourceManager().open_resource(name)
        print(self._generador.query('*IDN?'))
        
        #Activa la salida
        self._generador.write('OUTPut1:STATe on')
        self.setFrequency(1000)
        
    def __del__(self):
        self._generador.close()
        
    def setFrequency(self, freq):
        self._generador.write(f'FREQ {freq}')
        
    def getFrequency(self):
        return self._generador.query_ascii_values('FREQ?')
        
    def setAmplitude(self, freq):
        print('falta')
        
    def getAmplitude(self):
        print('falta')
        return 0



class TDS1002B:
    """Clase para el manejo osciloscopio TDS2000 usando PyVISA de interfaz
    """
    
    def __init__(self, name):
        self._osci = visa.ResourceManager().open_resource(name)
        self._osci.query("*IDN?")

    	#Configuración de curva
        
        # Modo de transmision: Binario positivo.
        self._osci.write('DAT:ENC RPB') 
        # 1 byte de dato. Con RPB 127 es la mitad de la pantalla
        self._osci.write('DAT:WID 1')
        # La curva mandada inicia en el primer dato
        self._osci.write("DAT:STAR 1") 
        # La curva mandada finaliza en el último dato
        self._osci.write("DAT:STOP 2500") 

        #Adquisición por sampleo
        self._osci.write("ACQ:MOD SAMP")
		
        #Seteo de canal
        self.set_channel(channel=1, scale=20e-3)
        self.set_channel(channel=2, scale=20e-3)
        self.set_time(scale=1e-3, zero=0)
		
        #Bloquea el control del osciloscopio
        self._osci.write("LOC")
    
	def __del__(self):
        self._osci.close()			

    def unlock(self):
         #Desbloquea el control del osciloscopio
        self._osci.write("UNLOC")

    def set_channel(self, channel, scale, zero=0):
    	#if coup != "DC" or coup != "AC" or coup != "GND":
    	    #coup = "DC"
    	#self._osci.write("CH{0}:COUP ".format(canal) + coup) #Acoplamiento DC
    	#self._osci.write("CH{0}:PROB 
        self._osci.write("CH{0}:SCA {1}".format(channel, scale))
        self._osci.write("CH{0}:POS {1}".format(channel, zero))
	
    def get_channel(self, channel):
        return self._osci.query("CH{0}?".format(channel))
		
    def set_time(self, scale, zero=0):
        self._osci.write("HOR:SCA {0}".format(scale))
        self._osci.write("HOR:POS {0}".format(zero))	
	
    def get_time(self):
        return self._osci.query("HOR?")
	
    def read_data(self, channel):
        # Hace aparecer el canal en pantalla. Por si no está habilitado
        self._osci.write("SEL:CH{0} ON".format(channel)) 
        # Selecciona el canal
        self._osci.write("DAT:SOU CH{0}".format(channel)) 
    	#xze primer punto de la waveform
    	#xin intervalo de sampleo
    	#ymu factor de escala vertical
    	#yoff offset vertical
        xze, xin, yze, ymu, yoff = self._osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', 
                                                                 separator=';') 
        data = (self._osci.query_binary_values('CURV?', datatype='B', 
                                               container=np.array) - yoff) * ymu + yze        
        tiempo = xze + np.arange(len(data)) * xin
        return tiempo, data
    
    def get_range(self, channel):
        xze, xin, yze, ymu, yoff = self._osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', 
                                                                 separator=';')         
        rango = (np.array((0, 255))-yoff)*ymu +yze
        return rango   

class Agilent34970A:
    """Clase para el manejo multiplexor Agilent34970A usando PyVISA de interfaz
    """
    def __init__(self, name):
        self._mux = visa.ResourceManager().open_resource(name)
        self._mux.query("*IDN?")

    	#Configuración de barrido
		self.ScanInterval = 1
		self.channelDelay = 0.2
		self.canales = (101,102,103,104,105,106,107, 108)
		self.ncanales = len(self.canales)

		self._mux.write('ROUTE:SCAN', '(@' + str(self.canales)[1:])
		self._mux.write('ROUT:CHAN:DELAY ' + str(self.channelDelay))
		self._mux.write('FORMAT:READING:CHAN ON') #Return channel number with each reading
		self._mux.write('FORMAT:READING:TIME ON') # Return time stamp with each reading
		#self._mux.write('FORMat:READing:TIME:TYPE  RELative') #Return time stamp im seconds since scanstart
		self._mux.write('FORMat:READing:TIME:TYPE  ABSolute') #Return time stamp absolute
		self._mux.write('FORMat:READing:UNIT OFF')
		self._mux.write('TRIG:TIMER ' + str(self.ScanInterval))		
		self._mux.write('TRIG:COUNT ' + str(1)) # one scan sweep per measure

    def __del__(self):
        self._mux.close()		
	
	def get_time(self):	
		a = self._mux.query_ascii_values('SYSTEM:TIME?') #pido la hora de inicio			
        return float(a[0])*3600+float(a[1])*60+a[2]	
	
	def one_scan(self):
		t0 = self._mux.query('INIT;:SYSTEM:TIME:SCAN?')		

		time.sleep(.5+(self.channelDelay+0.1)*self.ncanales)

		%query number of datapoints per scan
		Ndata=int(self._mux.query('DATA:POINTS?'))

		data = []
		time = []
		chan = []
		for ind in range(Ndata):
			str=self._mux.query(mux,'DATA:REMOVE? 1');
			d,t,ch = str.splot(',')
			data.append(d)
			time.append(t)
			chan.append(ch)
		
		return data,time,chan
		