%% Generador de funciones Tektronics AFG 3021B

disp('Generador de funciones Tektronics AFG 3021B')
disp('MANUAL: https://github.com/hgrecco/labosdf-bin/raw/master/manuals/TektronixAFG3000.pdf')

% Este string determina el intrumento que van a usar.
% Lo tienen que cambiar de acuerdo a lo que tengan conectado.
resource_name = 'USB0::0x0699::0x0346::C033250::INSTR';

fungen = visa('ni', resource_name);

% Abre la sesion VISA de comunicacion
fopen(fungen);

% Rampa logaritmica de frequencias
% Los dos primeros numeros (1 y 3) indican los exponentes de los limites(10^1 y 10^3)
% El siguiente el numero de pasos
FREQ=logspace(1, 3, 20);
for i=1:(length(FREQ))
    str=sprintf('FREQ %f',FREQ(i));
    fprintf(fungen,str);
    pause(0.1);
end

% Rampa lineal de amplitudes
AMP=0:10;
for i=1:(length(AMP))
    str=sprintf('VOLT %f',AMP(i));
    fprintf(fungen,str);
    pause(0.1);
end

% Rampa lineal de offset
OFF=0:10;
for i=1:(length(AMP))
    str=sprintf('VOLT:OFFS  %f',AMP(i));
    fprintf(fungen,str);
    pause(0.1);
end


% cierra la sesion VISA de comunicacion.
fclose(fungen);
