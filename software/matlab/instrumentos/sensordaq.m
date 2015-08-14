disp('Howto: http://www.mathworks.com/matlabcentral/fileexchange/32636-matlab-support-package-for-vernier-sensordaq')
% Vernier SensorDAQ (www.vernier.com/sensordaq) is a USB data-acquisition interface. It can be used to gather data from Vernier sensors (www.vernier.com/sensors) and also includes terminals for analog and digital I/O.
% 
% This support package extends the capabilites of Data Acquisition Toolbox (R2011b or later), and allows you to access the following SensorDAQ capabilities: 
%  * Vernier analog sensor measurements 
%  * Analog I/O (using the terminals) 
%  * Counter input 
%  * Digital I/O
% 
% The support package uses Data Acquisition Toolbox's "Session-based Interface" (except for the digital I/O, which uses the Legacy interface and requires 32-bit MATLAB).
% 
% Sample usage:

% --- Read a Vernier Sensor ---

session = sdaq.createSession(); 
sdaq.addSensor(session, 1, sdaq.Sensors.Barometer);

% the scaling function converts raw voltage to physical units 
scale = sdaq.getScaleFun(sdaq.Sensors.Barometer);

% get a single measurement, and convert to physical units 
rawdata = session.inputSingleScan(); 
data = scale(rawdata);

% collect 2 seconds worth of data 
session.DurationInSeconds = 2.0; 
rawdata = session.startForeground(); 
data = scale(rawdata);

% --- Analog input ---

session = sdaq.createSession(); 
sdaq.addAnalogInput(session,0);

% collect 2 seconds worth of data 
session.DurationInSeconds = 2.0; 
data = session.startForeground();