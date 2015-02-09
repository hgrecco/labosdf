%% LOCKIN SR830
disp('LOCKIN SR830')
disp('MANUAL: http://www.thinksrs.com/downloads/PDFs/Manuals/SR830m.pdf')


% Este string determina el intrumento que van a usar.
% Lo tienen que cambiar de acuerdo a lo que tengan conectado.
resource_name = 'GPIB::8::INSTR'

% inicializo el lockin, conectado con la interfase USB - GPIB
li = visa('ni', resource_name);

% abre la sesion con lockin
fopen(li);

% Leo x: X=1
str = query(li,'outp ?1');
X = str2double(str);

% Leo Y: Y=2
str = query(li,'outp ?2');
Y = str2double(str);

% Leo el modulo: R=3
str = query(li,'outp ?3');
R = str2double(str);

% Leo el angulo: tita=4
str = query(li,'outp ?4');
tita = str2double(str);

disp([X, Y, R, tita])

% pide las cuatro cosas %X=1, Y=2 ; R=3 , tita=4
str = query(li, 'SNAP ? 1,2,3,4');
data = str2num(str);

disp(data)

% cierra la sesion con lockin
fclose(li);    
