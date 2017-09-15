function out=busco_equipos
%busca todas las interfases de comunicacion, equipos y placas de adquisicion
%   y genera una lista de equipos disponibles, con su string de inicializacion

out={};%aca voy a poner todos nombres de los equipos disponibles
showoutput=1;%[0|1], si quiero que muestre el detalle de las interfases y eso

%informacion de Instrumentos
hw=instrhwinfo; %busco las interfases disponibles (visa, gpib, serial, etc)

%para cada interfase
for indinterfase=1:length(hw.SupportedInterfaces)
    
    interfase=hw.SupportedInterfaces{indinterfase};%'visa' o 'gpib' o 'serial' o ...
    
    % me fijo los objetos (equipos) disponibles en esta interfase
    hwif=instrhwinfo(interfase);

    if showoutput
        fprintf('Objetos disponibles en la interfase %s:\n',interfase)
    end
    
    %si hay objetos disponibles, los muestro y guardo el nombre
    if isprop(hwif,'ObjectConstructorName')
        for indobject=1:length(hwif.ObjectConstructorName)
            if showoutput
                fprintf('\t%s\n',hwif.ObjectConstructorName{indobject})
            end
            out=[out; hwif.ObjectConstructorName{indobject}];%agrego el constructorname
        end
    else
        if showoutput
            fprintf('\t%s\n','Nada')
        end
    end
end


%informacion de Adquisicion de datos
try 
    hw=daqhwinfo; %busco las interfases disponibles (visa, gpib, serial, etc)
catch ME
    %ME
    disp('daqhwinfo falla en Matlab 64bit')
    return
end  

%para cada Adaptador
for indinterfase=1:length(hw.InstalledAdaptors)
    
    interfase=hw.InstalledAdaptors{indinterfase};%'visa' o 'gpib' o 'serial' o ...

    % me fijo los objetos (equipos) disponibles en este Adaptador
    try 
        hwif=daqhwinfo(interfase);
    catch %pongo esto porque a veces 'parallel' falla
        continue
    end
    
    if showoutput
        fprintf('Objetos disponibles en la interfase %s:\n',interfase)
    end

    %si hay objetos disponibles, los muestro y guardo el nombre
    if isprop(hwif,'ObjectConstructorName')
        for indobject=1:length(hwif.ObjectConstructorName)
            if showoutput
                fprintf('\t%s\n',hwif.ObjectConstructorName{indobject})
            end
            out=[out; hwif.ObjectConstructorName{indobject}];%agrego el constructorname
        end
    else
        if showoutput
            fprintf('\t%s\n','Nada')
        end
    end
end
end
