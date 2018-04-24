%% Acquire Data in the Foreground
%create session object
s = daq.createSession('ni');
%Set acquisition duration
s.DurationInSeconds = 2.0;
%add analog input channel
addAnalogInputChannel(s,'Dev6','ai0','Voltage')
%get data
data = startForeground(s);
%plot data
plot(data)

%% Acquire Counter Input Data
%create session object
s = daq.createSession('ni');
%add counter input channel
ch = addCounterInputChannel(s,'Dev6', 'ctr0', 'EdgeCount');
%reset counters
resetCounters(s);
%read counter status
c=inputSingleScan(s)

