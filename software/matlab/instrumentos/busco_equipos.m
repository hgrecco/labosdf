function out=busco_equipos
%busca todas las interfases de comunicacion, equipos y placas de adquisicion
%   y genera una lista de equipos disponibles, con su string de inicializacion

out={};%aca voy a poner todos nombres de los equipos disponibles

%informacion de Instrumentos
hw=instrhwinfo; %busco las interfases disponibles (visa, gpib, serial, etc)

%para cada interfase
for indinterfase=1:length(hw.SupportedInterfaces)
    
    interfase=hw.SupportedInterfaces{indinterfase};%'visa' o 'gpib' o 'serial' o ...
    
    % me fijo los objetos (equipos) disponibles en esta interfase
    hwif=instrhwinfo(interfase);
    
%     fprintf('Objetos disponibles en la interfase %s:\n',interfase)
    
    %si hay objetos disponibles, los muestro y guardo el nombre
    if isfield(hwif,'ObjectConstructorName')
        for indobject=1:length(hwif.ObjectConstructorName)
%             fprintf('\t%s\n',hwif.ObjectConstructorName{indobject})
            out=[out; hwif.ObjectConstructorName{indobject}];
        end
    else
%         fprintf('\t%s\n','Nada')
    end
end


%informacion de Adquisicion de datos
hw=daqhwinfo; %busco las interfases disponibles (visa, gpib, serial, etc)

%para cada Adaptador
for indinterfase=1:length(hw.InstalledAdaptors)
    
    interfase=hw.InstalledAdaptors{indinterfase};%'visa' o 'gpib' o 'serial' o ...

    %por algun motivo, parallel no anda, lo salteo
    if strcmp(interfase,'parallel')
        continue
    end
    
    % me fijo los objetos (equipos) disponibles en este Adaptador
    hwif=daqhwinfo(interfase);
    
%     fprintf('Objetos disponibles en la interfase %s:\n',interfase)

    %si hay objetos disponibles, los muestro y guardo el nombre
    if isfield(hwif,'ObjectConstructorName')
        for indobject=1:length(hwif.ObjectConstructorName)
%             fprintf('\t%s\n',hwif.ObjectConstructorName{indobject})
            out=[out; hwif.ObjectConstructorName{indobject}];
        end
    else
%         fprintf('\t%s\n','Nada')
    end
end
end