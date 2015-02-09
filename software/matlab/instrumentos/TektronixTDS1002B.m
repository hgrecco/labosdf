%% osciloscopio Tektronics TDS 1002B

disp('Osciloscopio Tektronics TDS 1002B')


% Este string determina el intrumento que van a usar.
% Lo tienen que cambiar de acuerdo a lo que tengan conectado.
resource_name = 'USB0::0x0699::0x0346::C034165::INSTR'

vu = visa('ni', resource_name);

% incrementa el tamano del buffer
set(vu,'InputBufferSize',20000)

% abre la sesi?n Visa de comunicacion con el osciloscopio
fopen(vu);

% defino que canal voy a pedir
canal=1;

% adquiero los datos de una pantalla
[voltaje tiempo] = OSC_adquiere_canal(vu,canal);

% cierro la comunicacion con el osciloscopio
fclose(vu); 
