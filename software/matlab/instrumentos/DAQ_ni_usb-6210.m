%% NI daq, como las sensordaq

disp('NI USB-6210')
disp('MANUAL: ')

% para saber que aparatos hay conectados
hw = daqhwinfo('nidaq'); 
disp(hw)
hw.InstalledBoardIds
hw.BoardNames


% inicializo la conexion (uso DevX sacada de las lineas anteriores)
ai = analoginput('nidaq', 'Dev3');

% agrego canales (ver manual)
addchannel(ai, 0:2);

% duracion en segundos
duracion = 1;
% configuro rate
ai.SampleRate = 80000;
ai.SamplesPerTrigger = ai.SampleRate * duracion;

% configuro el modo diferencial o singleended
% Otras opciones son: [ NonReferencedSingleEnded | SingleEnded | {Differential} ]
ai.InputType = 'Differential';
% alternativa hace lo mismo
% set(ai, 'InputType', 'Differential');

% si quiero setear inputs y outputs digitales:
% digitalio('nidaq', 'Dev3')

% mando un trigger, arranco la medicion
start(ai);

% espero un poquito mas que lo que dura la medicion
pause(duracion + 0.2)
% alternativa para esperar un poco
% wait(ai, duracion+0.2);
% le pido los datos
[data time] = getdata(ai);

figure(1)
plot(time,data)

% al finalizar, detengo la conexion
stop(ai);
