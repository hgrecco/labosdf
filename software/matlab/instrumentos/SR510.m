%% Ejemplo para controlar el lockin SR-510
% La configuraci�n del Switch trasero SW2 debe estar as�:
% Bit 1: Down
% Bit 2: Up
% Bit 3: Up
% Bit 4: Down
% Bit 5: Up
% Bit 6: Up
% Bit 7: Down
% Bit 8: Up
% Para otras configuraciones, consultar el manual

s=serial('COM1','BaudRate',9600,'DataBits',8,'StopBits',1,'Parity','none');
set(s,'terminator','CR')

fopen(s);
%%
%Setea sensibilidad en 10mV. Para otras sensibilidades, consultar el manual
fprintf(s,'G 19');

%Pregunta frecuencia
str=query(s,'F');
Frecuencia=sscanf(str,'%f');

%Emula apretar el bot�n quad up (+90�)
fprintf(s,'K 19');

%Emula apretar el bot�n quad down (-90�)
fprintf(s,'K 20');

%Setea display to X
fprintf(s,'S 0');

%Pregunta la fase
phase=query(s,'P');

%Mide voltaje
str=query(s,'Q');
Voltaje=sscanf(str,'%f');

%Setea fase 0�, espera y luego mide voljaje X 
fprintf(s,'P 0');
pause(1)%Esperar un tiempo razonable, dependiendo de la constante de tiempo
str=query(s,'Q');
VoltajeX=sscanf(str,'%f');

%Setea fase 90�, espera y luego mide voljaje Y
fprintf(s,'P 90');
pause(1)%Esperar un tiempo razonable, dependiendo de la constante de tiempo
str=query(s,'Q');
VoltajeY=sscanf(str,'%f');