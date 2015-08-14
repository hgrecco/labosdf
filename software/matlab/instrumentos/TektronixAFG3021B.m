%% Generador de funciones Tektronics AFG 3021B

disp('Generador de funciones Tektronics AFG 3021B')
disp('MANUAL: www.pd.infn.it/~zotto/laboratorio/AFG3000.pdf?')

%muestro la lista de equipos disponibles, y el string de inicializacion
out=busco_equipos

%reconoce al generador
gf = visa('ni','USB0::0x0699::0x0346::C034165::INSTR');

%abre la sesión Visa de comunicación con el generador de funciones
fopen(gf);

%loop seteando la frecuencia
FREQ=100:0.1:110;
for i=1:(length(FREQ))
    str=sprintf('FREQ %f',FREQ(i));
    fprintf(gf,str);
    pause(0.1);
end

%cierra la sesión Visa de comunicación con el generador de funciones
fclose(gf);