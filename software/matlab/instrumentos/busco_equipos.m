function out=busco_equipos
%busca todas las interfases de comunicacion, equipos y placas de adquisicion
%   y genera una lista de equipos disponibles, con su string de inicializacion

fprintf('Información de instrumentos conectados (instrhwinfo):\n')

%informacion de Instrumentos
hw=instrhwinfo; %busco las interfases disponibles (visa, gpib, serial, etc)
out={};%aca voy a poner todos nombres de los equipos disponibles
for indinterfase=1:length(hw.SupportedInterfaces)    
    interfase=hw.SupportedInterfaces{indinterfase};%'visa' o 'gpib' o 'serial' o ...
    fprintf('\tObjetos disponibles en:  hw=instrhwinfo(''%s'')\n',interfase)
    
    % busco objetos (equipos) disponibles en esta interfase
    hwif=instrhwinfo(interfase);    
    temp=busco_ObjectConstructorName(hwif);
    out=[out;temp]; %#ok<*AGROW>
    
    % busco objetos (equipos) disponibles en cada adaptador de esta interfase
    if isfield(hwif,'InstalledAdaptors')
        adaptors=hwif.InstalledAdaptors;
        if ~iscell(adaptors);adaptors={adaptors};end%pues si es uno solo, devuelve un string en lugar de una celda!
        for indad=1:length(adaptors)    
            adaptor=adaptors{indad};
            fprintf('\tObjetos disponibles en:  hw=instrhwinfo(''%s'',''%s'')\n',interfase,adaptor)
            % me fijo los objetos (equipos) disponibles en este adaptador
            hwad=instrhwinfo(interfase,adaptor);            
            temp=busco_ObjectConstructorName(hwad);
            out=[out;temp];
        end
    end
    
end



fprintf('\n')
fprintf('Información de hardware de Adquisición de datos (daqhwinfo):\n')
%informacion de Adquisicion de datos
if(strcmp(computer,'PCWIN64'))
    fprintf('\tOJO: daqhwinfo falla en Matlab 64bit\n')
    return
else
    hw=daqhwinfo;
    %para cada Adaptador
    for indad=1:length(hw.InstalledAdaptors)
        
        adaptor=hw.InstalledAdaptors{indad};%'visa' o 'gpib' o 'serial' o ...
        fprintf('\tObjetos disponibles en:  hw=daqhwinfo(''%s'')\n',adaptor)       
        try%pongo esto porque a veces 'parallel' falla, y tambien 'mcc'
            % me fijo los objetos (equipos) disponibles en este Adaptador
            hwif=daqhwinfo(adaptor);
        catch  %#ok<CTCH>
            fprintf('\t\tOJO: daqhwinfo(''%s'') devuelve error.\n',adaptor)       
            continue
        end                
        
        temp=busco_ObjectConstructorName(hwif);
        out=[out;temp];        
    end
end
end

function out=busco_ObjectConstructorName(hw)
%si hay objetos disponibles, los muestro y guardo el nombre
out={};
if isfield(hw,'ObjectConstructorName')
    for indobject=1:length(hw.ObjectConstructorName)
        if ~isempty(hw.ObjectConstructorName{indobject})
            fprintf('\t\t%s\n',hw.ObjectConstructorName{indobject})
            out=[out; hw.ObjectConstructorName{indobject}];%agrego el constructorname            
        end
    end
end        
end
