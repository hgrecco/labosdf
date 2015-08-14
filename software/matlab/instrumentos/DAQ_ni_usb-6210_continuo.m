%% inicializo la comunicacion con la placa


% %para saber como se llama la placa. Típicamente Dev6 o Dev7
% hw=daqhwinfo('nidaq')
% hw.InstalledBoardIds
% hw.ObjectConstructorName'

%muestro la lista de equipos disponibles, y el string de inicializacion
out=busco_equipos

%inicializo la comunicacion y el canal
ai = analoginput('nidaq','Dev7');%inicializo la conexion (uso DevX sacada de las lineas anteriores)
addchannel(ai, 1); %agrego canales (ver manual), si quisiera agregar mas tengo que ponerlos como vector

%% arranco con la medicion

stop(ai)%por si lo detuve antes y estaba corriendo
flushdata(ai) %saco los datos que quedaron desde el ultimo getdata y los elimina

Duration=10;%duración de la adquisición
Samplig_Rate=250000;%configuro rate (en Hz)
ai.SampleRate = Samplig_Rate ;
ai.SamplesPerTrigger = Duration*Samplig_Rate;

series=struct([]);

%arranco la adquisicion
start(ai);
tic
while ai.SamplesAvailable>0
    %Tiempo máximo de adquisición
    
    pause(0.01);
    %pauso un poquito para no bloquear el sistema
    
    NSamplesRequest=Samplig_Rate/2;%voy a pedir en series de medio segundo
    
    if ai.SamplesAvailable>NSamplesRequest%Si tengo suficientes muestras, las levanto y proceso
        
        %levanto una serie de datos 
        [data time]=getdata(ai,NSamplesRequest);                
               
        %armo una estructura para almacenar los datos
        cont=length(series)+1;        
        series(cont).nsamples=length(data);%agrego cuantos datos medi
        series(cont).data=data;%agrego data (si la medicion es larga, va a llenarse la memoria)
        series(cont).time=time;%agrego time (si la medicion es larga, va a llenarse la memoria)
        
        %grafico los datos de la ultima serie
        figure(1);clf;
        plot(time-time(1),data)        
        xlim(time([1 end]))%resto time(1) para que me muestre siempre lo mismo en el eje x            
        xlabel('Time [s]')
        ylabel('Voltage [V]')
        str=sprintf('Time: %02.2fs - Samples: %d - SR: %02.2f ', toc,sum([series.nsamples]),sum([series.nsamples])/toc);
        title(str)
        grid on                
        
    end    
end

stop(ai)%paro ai
flushdata(ai) %saco los datos que quedaron desde el ultimo getdata y los elimina


