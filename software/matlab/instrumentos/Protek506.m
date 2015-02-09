%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% El mult�metro Protek 506 se comunica con la compu a trav�s de un puerto
%%% serie (DB9). El mult�metro devuelve la lectura que muestra en pantalla 
%%% cada vez que desde el puerto serie recibe algo (puede ser un caracter 
%%% en blanco). En este ejemplo est� seteado para leer temperatura con una 
%%% termocupla, por lo que el string que devuelve el mult�metro es 
%%% 'TEMP 33,2'. De ah� el programa extrae el valor de temperatura y lo
%%% guarda en una variable
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear all;

s2 = serial('COM1','BaudRate',1200,'DataBits',7,'StopBits',2,'Parity','none','terminator','CR');
fopen(s2);
set(s2,'terminator','CR');

tic
N=5;

medicion = zeros(N, 1);
temp = zeros(N, 1);
tiempo = zeros(N, 1)

for i=1:N
    medicion(i) = i
    str = query(s2, '');
    temperatura = sscanf(str, 'TEMP %f')
    temp(i) = temperatura;
    tiempo(i) = toc
end

datos=[tiempo; temp ]';

fclose(s2);


save('datatemp.txt','datos','-ascii')

plot(tiempo,temp)

