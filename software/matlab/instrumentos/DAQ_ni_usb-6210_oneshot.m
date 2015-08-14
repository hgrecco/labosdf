%% NI daq, como las sensordaq

disp('NI USB-6210')
disp('MANUAL: ')

% %para saber como se llama la placa. Típicamente Dev6 o Dev7
% hw=daqhwinfo('nidaq')
% hw.InstalledBoardIds
% hw.ObjectConstructorName'

%muestro la lista de equipos disponibles, y el string de inicializacion
out=busco_equipos

ai = analoginput('nidaq','Dev3');%inicializo la conexion (uso DevX sacada de las lineas anteriores)
addchannel(ai, 0:2);%agrego canales (ver manual)

duracion = 1;%duracion en segundos
ai.SampleRate = 80000;%configuro rate
ai.SamplesPerTrigger = ai.SampleRate*duracion;

%configuro el modo diferencial o singleended
ai.InputType='Differential';%%[ NonReferencedSingleEnded | SingleEnded | {Differential} ]
%set(ai,'InputType','Differential');% alternativa hace lo mismo

%si quiero setear inputs y outputs digitales:
%digitalio('nidaq','Dev3')

start(ai);%mando un trigger, arranco la medicion
pause(duracion+0.2)%espero un poquito mas que lo que dura la medicion
%wait(ai, duracion+0.2);%alternativa para esperar un poco
[data time] = getdata(ai);%le pido los datos

figure(1)
plot(time,data)
  
stop(ai); %al finalizar, detengo la conexion
