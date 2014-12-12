%% osciloscopio Tektronics TDS 1002B

disp('Osciloscopio Tektronics TDS 1002B')

vu = visa('tek','USB0::0x0699::0x0363::C065088::INSTR');

%incrementa el tama�o del buffer
set(vu,'InputBufferSize',20000)

%abre la sesi?n Visa de comunicaci?n con el osciloscopio
fopen(vu);

canal=1;% defino que canal voy a pedir

%adquiero los datos de una pantalla
[voltaje tiempo]=OSC_adquiere_canal(vu,canal);

%cierro la comunicacion con el osciloscopio
fclose(vu); 