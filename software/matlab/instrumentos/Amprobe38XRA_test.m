%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% El multímetro Amprobe 38XR-A se comunica con la compu a través de un
%%% puerto serie (DB9). El multímetro devuelve una cadena de caracteres,
%%% que es necesario procesar para interpretar información de medida, 
%%% unidades, signo, etc. Eso se hace dentro de la función Amprobe38XRA.m
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

s=serial('COM1','BaudRate',9600,'DataBits',8,'StopBits',1,'Parity','none');
set(s,'terminator','CR','InputBufferSize',15,'ReadAsyncMode','manual');
fopen(s);

%% MEDICION SIMPLE
verbose=1;
[Ylab , value, str, count] = Amprobe38XRA(s,verbose);
fprintf('Valor: %g Unidades: %s str: %s count:%d\n',value,Ylab,str,count);

%% MEDICION EN FUNCION DEL TIEMPO
figure(1);clf
ndata=1000;
medicion=nan(ndata,1);
tiempo=medicion;
tic
for i=1:ndata
    [ Ylab , value ,str, count] = Amprobe38XRA(s,1);
    texto=sprintf('Valor: %g\nUnidades: %s\nstr: %s\ncount:%d\ni: %d',value,Ylab,str,count,i);
    medicion(i)=value;
    tiempo(i)=toc;
    plot(tiempo,medicion,'.-')
    text(mean(xlim),mean(ylim),texto)
    ylabel(Ylab)
    xlabel('Tiempo [s]')
    drawnow
end

%% Cierre de la conexion 
fclose(s);
    
    
    
   
   
