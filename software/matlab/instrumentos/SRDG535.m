%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Este script mínimo muestra un par de instrucciones y la sintaxis de la  %
% sesión GPIB para comunicarse con el generador de retardos SRS.          %
% Para interfasear usando el adaptador USB-GPIB, hay que intercalar el    %
% cable GPIB entre el equipo y la PC.                                     %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%muestro la lista de equipos disponibles, y el string de inicializacion
out=busco_equipos

gn=visa('agilent','GPIB0::15::INSTR');  
%la direccion gpib (15) se puede cambiar desde el panel frontal

fopen(gn);

%muestra en el display del equipo la frecuencia del trigger interno:
fprintf(gn,'DL 0,1,0');  


%seteado para disparo interno, hace un barrido de frecuencias 
N=5;
t=1:N
for i=1:N
    str=sprintf('TR 0,%f',t(i)); 
    %el primer cero es para cambiar el rate del trigger interno
    %TR 1,xxxx cambia el rate del trigger de bursts
    fprintf(gn,str)
    pause(2)
end

fclose(gn)