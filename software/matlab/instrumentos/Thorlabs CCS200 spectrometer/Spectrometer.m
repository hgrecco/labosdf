


clc;
clear;
disp('Start spectrometer.');

% sets environment variable
setenv('MW_MINGW64_LOC','C:\TDM-GCC-64') 

%   Loading the dll and header file into MATLAB
libname='C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLCCS_64.dll';
hfile='C:\Program Files\IVI Foundation\VISA\Win64\Include\TLCCS.h';
loadlibrary(libname,hfile,'includepath','C:\Program Files\IVI Foundation\VISA\Win64\Include\', 'includepath', 'C:\Program Files\IVI Foundation\VISA\Win64\Lib_x64\');
disp('Library loaded.');

%   Displays the functions in the library
%   Also gives the data types used in a command
%   - Not necessary for normal use -
libfunctionsview 'TLCCS_64';

%   Some dll functions use pointers
%   The 'libpointer' command has to be used in MATLAB for this

%   !!! Change this instrument ID to the ID of your device !!!
%
%   Type-ID:
%   0x8081   // CCS100 Compact Spectrometer
%   0x8083   // CCS125 Special Spectrometer 
%   0x8085   // CCS150 UV Spectrometer 
%   0x8087   // CCS175 NIR Spectrometer 
%   0x8089   // CCS200 UV-NIR Spectrometer 
%
%   'USB0::0x1313::<Type-ID>::<Serial Number>::0::RAW'

%   Initialize the spectrometer
res=libpointer('int8Ptr',int8('USB0::0x1313::0x8089::M00311012::0::RAW'));
hdl=libpointer('ulongPtr',0);
[a,b,c]=calllib('TLCCS_64', 'tlccs_init', res, 0, 0, hdl);
disp(['Initialize device (0 = correct, rest = error): ', num2str(a)]);

%   Open figure window
figure;

for i=1:10
    
    %   Set integration time, measure spectrum and get data
    inttime=0.1;
    calllib('TLCCS_64','tlccs_setIntegrationTime',hdl.value,inttime);
    calllib('TLCCS_64', 'tlccs_startScan', hdl.value);
    %pause(1);
    specdata=libpointer('doublePtr',double(1:3648));
    calllib('TLCCS_64','tlccs_getScanData', hdl.value, specdata);
    wldata=libpointer('doublePtr',double(1:3648));
    calllib('TLCCS_64','tlccs_getWavelengthData', hdl.value, 0, wldata, 0, 0);

    %   Display spectrum
    pause(0.001);
    plot(wldata.value,specdata.value);
    title(['Spectrum ', num2str(i), ' (Integration time: ', num2str(inttime), ' sec)']);
    xlabel('Wavelength [nm]');
    ylabel('Counts [a.u.]');

end

%   Close spectrometer connection, unload library
calllib('TLCCS_64','tlccs_close', hdl.value);
unloadlibrary 'TLCCS_64';