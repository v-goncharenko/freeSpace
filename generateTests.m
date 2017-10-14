function generateTests()
    %GENERATETESTS generate test cases for FreeSpace python class
    
    % case #1 siplest test
    sample_rate = 8e3;
    operating_frequency = 3e8;
    origin_pos = [1000;0;0];
    dest_pos = [300;200;50];
    origin_vel = [0;0;0];
    dest_vel = [0;0;0];
    signal = ones(5,1);
    save('testCases/1_input', 'signal', 'operating_frequency', 'sample_rate', 'origin_pos', 'dest_pos', 'origin_vel', 'dest_vel');

    henv = phased.FreeSpace('SampleRate', sample_rate, 'OperatingFrequency', operating_frequency);
    y = step(henv, signal, ...
        origin_pos, ...
        dest_pos,...
        origin_vel,...
        dest_vel);
    save('testCases/1_matlab', 'y')

    % case #2 FM wave
    waveform = phased.LinearFMWaveform('SweepBandwidth',1e5,...
        'PulseWidth',5e-5,'OutputFormat','Pulses',...
        'NumPulses',1,'SampleRate',1e6,'PRF',1e4);
    signal = waveform();
    operating_frequency = 1e9;
    sample_rate = 1e6;
    origin_pos = [1000; 250; 10];
    dest_pos = [3000; 750; 20];
    origin_vel = [0;0;0];
    dest_vel = [0;0;0];
    save('testCases/2_input', 'signal', 'operating_frequency', 'sample_rate', 'origin_pos', 'dest_pos', 'origin_vel', 'dest_vel');
    
    channel = phased.FreeSpace('SampleRate',sample_rate,...
        'TwoWayPropagation',false,'OperatingFrequency',operating_frequency);
    y = channel(signal, origin_pos, dest_pos, origin_vel, dest_vel);
    save('testCases/2_matlab', 'y');    
    
    % case #3 long signal
    sample_rate = 8e3;
    operating_frequency = 3e8;
    origin_pos = [1000; -500; 3000];
    dest_pos = [300; 200; 50];
    origin_vel = [0;0;0];
    dest_vel = [0;0;0];
    signal = ones(1e6,1);
    save('testCases/3_input', 'signal', 'operating_frequency', 'sample_rate', 'origin_pos', 'dest_pos', 'origin_vel', 'dest_vel');

    henv = phased.FreeSpace('SampleRate', sample_rate, 'OperatingFrequency', operating_frequency);
    y = step(henv, signal, ...
        origin_pos, ...
        dest_pos,...
        origin_vel,...
        dest_vel);
    save('testCases/3_matlab', 'y')
    
    % case #4 double step
    waveform = phased.LinearFMWaveform('SweepBandwidth',1e5,...
        'PulseWidth',5e-5,'OutputFormat','Pulses',...
        'NumPulses',1,'SampleRate',1e6,'PRF',1e4);
    signal_1 = waveform();
    signal_2 = ones(100, 1);
    operating_frequency = 1e9;
    sample_rate = 1e6;
    origin_pos = [1000; 250; 10];
    dest_pos = [3000; 750; 20];
    origin_vel = [0;0;0];
    dest_vel = [0;0;0];
    save('testCases/4_input', 'signal_1', 'signal_2', 'operating_frequency', 'sample_rate', 'origin_pos', 'dest_pos', 'origin_vel', 'dest_vel');
    
    channel = phased.FreeSpace('SampleRate',sample_rate,...
        'TwoWayPropagation',false,'OperatingFrequency',operating_frequency);
    y_1 = channel(signal_1, origin_pos, dest_pos, origin_vel, dest_vel);
    y_2 = channel(signal_2, origin_pos, dest_pos, origin_vel, dest_vel);
    save('testCases/4_matlab', 'y_1', 'y_2');    
end

