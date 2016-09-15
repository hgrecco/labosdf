% LOCKIN SR510
disp('LOCKIN SR510')
disp('MANUAL: http://www.thinksrs.com/downloads/PDFs/Manuals/SR510m.pdf')


% Inicializo el Lockin, conectado con la interfase USB-GPIB
% Address 23 en GPIB (buscar address en NI MAX)
lockin = visa('ni','GPIB0::23::INSTR'); 
% Abre la sesión con el lockin
fopen(lockin);
    % F : lee la frecuencia de referencia (ASCII string)
    % G : lee (o setea) la ganancia (sensibilidad)
    % P : lee (o setea) la fase
    % G : lee (o setea) la sensibilidad
    % Q : lee la amplitud de la señal en canal A
    % ¡¡ Ver manual para explicacion mas detallada !!
    % ¡¡ Ver manual para lista de comandos disponibles !!
    
% Programar la salida X5 o X6 
fwrite(lockin,['X5,',num2str(k)])
%
% Configurar la fase respecto de referencia
fwrite(lockin,'P45');
% Leer la fase
query(lockin,'P');
% Leer la amplitud y almacenarla en una variable
A= query(lockin,'Q');
% Cierra sesion
fclose(lockin);
% transformar variable a un numero
A_num = str2num(A);
