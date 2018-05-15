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

%% Acquire Counter Input Data, single data
%create session object
s = daq.createSession('ni');
%add counter input channel
ch = addCounterInputChannel(s,'Dev6', 'ctr0', 'EdgeCount');%if type is 'pulsewidth', it will wait until pulse is detected
%reset counters
resetCounters(s);
%read counter status
c=inputSingleScan(s)

%% Acquire Counter Input Data, with internal clock
%create session object
s=daq.createSession('ni');
%add counter input channel
ch=addCounterInputChannel(s,'dev3','ctr0','edgecount');
%add analog input channel, required to set clock and rate
addAnalogInputChannel(s,'dev3', 'ai1', 'Voltage');

%set duration and rate
s.DurationInSeconds = 2;
s.Rate = 10000;

%get data
data =  startForeground(s);
%plot measured data
plot (diff(data(:,1)))