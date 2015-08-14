%% Multimetro HP 34401

disp('Multimetro HP 34401')
disp('MANUAL: http://www.physics.rutgers.edu/ugrad/327/HP34401.pdf')

%muestro la lista de equipos disponibles, y el string de inicializacion
out=busco_equipos

%reconoce al multimetro
vu = visa('ni','GPIB1::22::INSTR');

%abre la sesión Visa de comunicación con el multimetro
fopen(m);

%pide voltaje dc
str=query(mm,'measure:voltage:DC?');

%otras cosas que se pueden medir
% MEASure
%  :VOLTage:DC? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
%  :VOLTage:DC:RATio? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
%  :VOLTage:AC? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
%  :CURRent:DC? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
%  :CURRent:AC? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
%  :RESistance? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
%  :FRESistance? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
%  :FREQuency? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
%  :PERiod? {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
%  :CONTinuity?
%  :DIODe?


%cierra la sesión con mm
fclose(mm);
