function [voltaje tiempo]=OSC_adquiere_canal(vu,canal)

%le digo que quiero datos del canal "canal"
str=sprintf('DATA:SOURCE CH%d',canal);
fprintf(vu,str);

%no se
fprintf(vu,'DAT:ENC RPB');

%no se
fprintf(vu,'DAT:WID 1');

%le pido algunos parametros de la pantalla, para poder escalear adecuadamente
ji=query(vu,'WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;');
er=str2num(ji);
XZE=er(1);
XIN=er(2);
YZE=er(3);
YMU=er(4);
YOFF=er(5);

%le pido los datos de la pantalla
fprintf(vu,'CURV?');
[hh,count]=binblockread(vu,'uint8');

%los transformo adecuadamente:
%la conversion es 'datos_y'=(gg-YOFF)*YMU + YZE
%                     xend=XZE+XIN*length(gg)
%                 'datos_x'=[XZE:XIN:xend]

voltaje=(hh-YOFF)*YMU+YZE;
xend=XZE+XIN*length(voltaje)-XIN;
tiempo=(XZE:XIN:xend)';
end


