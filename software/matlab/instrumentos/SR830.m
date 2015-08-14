%% LOCKIN SR830
disp('LOCKIN SR830')
disp('MANUAL: http://www.thinksrs.com/downloads/PDFs/Manuals/SR830m.pdf')

%muestro la lista de equipos disponibles, y el string de inicializacion
out=busco_equipos

%inicializo el lockin, conectado con la interfase USB - GPIB
li = gpib('ni',0,8);

%abre la sesión con lockin
fopen(li);

%Leo x: X=1
str=query(li,'outp ?1');
X=str2double(str);

%Leo Y: Y=2
str=query(li,'outp ?2');
Y=str2double(str);

%Leo el modulo: R=3
str=query(li,'outp ?3');
R=str2double(str);

%Leo el ángulo: tita=4
str=query(li,'outp ?4');
tita=str2double(str);

str=query(li, 'SNAP ? 1,2,3,4');%pide las cuatro cosas %X=1, Y=2 ; R=3 , tita=4
data=str2num(str);

%cierra la sesión con lockin
fclose(li);    