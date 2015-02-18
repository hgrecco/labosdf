%% Fuente Agilent B2901A
% manufacturer: http://www.hantek.com.cn/en/ProductDetail_32.html
% Manual Usuario (local): \\Srvlabos\manuales\HP-Agilent\B2901A\B2910-90010.pdf

disp('Fuente Agilent B2901A')


% Este string determina el intrumento que van a usar.
% Lo tienen que cambiar de acuerdo a lo que tengan conectado.
resource_name = 'USB0::0x0957::0x8B18::MY51140178::INSTR'

vu = visa('ni', resource_name);

% abre la sesi?n Visa de comunicacion
fopen(vu);

% query idn
disp(query(vu,'*IDN?'))

%  Ultimos valores medidos de 
%  Voltage, corriente, resistencia, tiempo, status, source ouput setting

% adquiero los datos
disp(query(vu,':READ:SCALar?'))

% cierro la comunicacion
fclose(vu); 
