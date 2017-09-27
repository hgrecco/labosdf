function [Ylab , value, str, count] = Amprobe38XRA(s,verbose)
% Driver Matlab para el multimetro Amprobe 38XR-A
% Basado en un driver de scilab: https://fileexchange.scilab.org/toolboxes/232000
% Armado por los docentes y pañoleros de Labo 4 A, 2do cuatrimestre de 2017, FCEyN, UBA
%
%Inicialización de la comunicación: 
% s=serial('COM1','BaudRate',9600,'DataBits',8,'StopBits',1,'Parity','none');
% set(s,'terminator','CR','InputBufferSize',20000,'ReadAsyncMode','manual');
% fopen(s);
%
%Input:
% s: serial port
% verbose: 1-> muestra lo que lee 0-> no muestra nada
%
%Output:
% Ylab: Magnitud y unidades medidas 
% value: el valor medido 
% str: el string que devuelve el multímetro
% count: la cantidad de veces que se leyó hasta obtener un string aceptable

%procesa el input
if nargin==0
    Ylab = ''; value = nan; str = ''; count = nan;
    return
elseif nargin==1
    verbose = 0;
end    

%lee el string que manda el multimetro
[str, count]=LeeStringAmprobe(s); 

if isempty(str)
    Ylab = ''; value = nan; str = ''; count = nan;
    return
end

%Procesa el string, interpreta el valor, la medida, etc.
[ Ylab , value ] = ProcesaStringAmprobe(str,verbose);

end

function [str, count]=LeeStringAmprobe(s)
%Lee el string que manda el multimetro.
%A veces manda strings de distintas longitudes. Itero hasta que me da uno
%de 15 caracteres.

if s.BytesAvailable>0 %si hay datos en el buffer...
    set(s,'ReadAsyncMode','manual'); %pongo en modo que solo ponga datos cuando se los pido
    flushinput(s);%y vacio el buffer
end

count=0;
str='';
while length(str)~=15 %si no tiene 15 caracteres, lo vuelve a medir
    count=count+1;%para saber cuantas veces entró en el loop
    str=fscanf(s);
    if isempty(str)
        fprintf('Salgo, probablemente timeout, desconectado')
        return
    end    
end

%le saco el primer y ultimo caracter, que es un char raro.
str=str(2:end-1);%devuelvo un string de 13 caracteres

end



function [ Ylab , value ] = ProcesaStringAmprobe(str,verbose)
%extraigo los valores pertinentes del string
code = str(1:2);
data=str2double(str(3:6));
modo=str2double(str(7));
exponente=str2double(str(9));
acdc=str2double(str(10));
absrel=str2double(str(12));
signo=str2double(str(13));

%muestro en pantalla (si me lo piden)
if verbose
    fprintf('Str:  %s\n',str)
    fprintf('Code: %s\n',code)
    fprintf('Data:   %04d\n',data)
    fprintf('Modo:       %d\n',modo)
    fprintf('str(8):      %s\n',str(8))
    fprintf('Exp:          %d\n',exponente)
    fprintf('AC|DC|AC+DC:   %d\n',acdc)
    fprintf('str(11):        %s\n',str(11))
    fprintf('absrel:          %d\n',absrel)
    fprintf('Signo:            %d\n',signo)
end

%inicializo
Ylab='';
value=0;
switch code,
    case '10'	% Voltmeter ~
        if modo == 0	% mode [V]
            Ylab = 'Voltage ~ [V]';
            if absrel==8
                Ylab = 'Delta(Voltage) ~ [V]';
            end
            value = data*1e-4*10^exponente;    % TO BE CONFIRMED
        else                                     % mode [dBm]
            Ylab  = 'Voltage ~ [dBm]';
            value = (-1)^(signo)*data*0.01;
            % ABS/REL has no effect
        end
        
    case '0C' 	% Voltmeter  --   %CHEQUEADO
        Ylab = 'Voltage';        
        if absrel==8;
            Ylab = 'Delta(Voltage)';
        end
%         if modo == 1%hex2dec(str(8))> 8;
%             Ylab= [Ylab ,' AC +'];
%         end  % mode AC+DC 
       
        Ylab = [Ylab ,' DC [V]'];
        value = (-1)^(signo)*data*(1e-4)*(10^exponente); % [V]
        
    case '07'	% µA
        Ylab = 'Current [A]';
        if absrel==8; 
            Ylab = 'Delta(Current) [A]';
        end
        switch acdc
            case 0
                Ylab = [Ylab ' DC'];
            case 1
                Ylab = [Ylab ' AC'];
            case 2
                Ylab = [Ylab ' AC+DC'];
        end
        value = (-1)^(signo)*data*1e-8*10^exponente;	% [A]
        
    case '0E'	% mA
        Ylab = 'Current';
        if absrel==8
            Ylab = 'Delta(Current)';
        end
        switch acdc
            case 0
                Ylab = [Ylab ' DC'];
            case 1
                Ylab = [Ylab ' AC'];
            case 2
                Ylab = [Ylab ' AC+DC'];
        end
        Ylab = [Ylab ' [A]'];
        value = (-1)^(signo)*data*1e-6*10^exponente; % [A]
        
    case '0A' 	% 10 A
        Ylab = 'Current';
        switch acdc
            case 0
                Ylab = [Ylab ' DC'];
            case 1
                Ylab = [Ylab ' AC'];
            case 2
                Ylab = [Ylab ' AC+DC'];
        end
        Ylab = [Ylab ' [A]'];
        value = (-1)^(signo)*data/1000. ;             % [A]
        
    case '06'	% Temperature [°C]
        Ylab = 'Temperature [°C]';
        value = (-1)^(signo)*data;
        % ABS/REL has no effect
        
    case '0F',	% Frequencemeter
        if modo == 2
            Ylab  = 'Cyclic Rate [%]';      % Rapport cyclique
            value = (-1)^(signo)*data*0.01*10^exponente;            % [%]
        else
            Ylab = 'Frequency [Hz]';
            if absrel==8, Ylab='Delta(Frequency) [Hz]'; end
            % absrel passe aussi à 8 en absolu lors des changements de calibre...
            % parece que tambien se pone en 8 en el modo aboluto... ver...
            value = (-1)^(signo)*data*0.01*10^exponente;    % [Hz]
        end
        
    case '08',	% Ohm-meter
        Ylab  = 'Resistance [Ohm]';
        if absrel==8, Ylab='Delta(Resistance) [Ohm]'; end
        value = (-1)^(signo)*data*1.0*10^(4-exponente);    % [Ohm]
        
    case '0B',	% Capacity
        Ylab = 'Capacity [µF]';
        if absrel==8, Ylab='Delta(Capacity) [µF]'; end
        % absrel passe aussi à 8 en absolu lors des changements de calibre...
        % parece que tambien se pone en 8 en el modo aboluto... ver...
        value = (-1)^(signo)*data*1e-5*10^exponente;    % [µF]
        
    case '03',	% mA 4-20 --			% [mA]
        Ylab ='Current 4-20 [mA] --';
        value = data;
        % ABS/REL has no effect
        
    case '02',	% Temperature [°F]
        Ylab  = 'Temperature [°F]';
        value = (-1)^(signo)*data;
        % ABS/REL has no effect
        
    case '04',	% Test diode
        Ylab  = 'Test diode [V]';
        value = data/1000.;
        % ABS/REL has no effect        
end

end