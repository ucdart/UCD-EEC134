%This code originated from sample code given by Gregory Charvat. It's been heavily 'developed' into the code
%that you see now primarily by Zach Myers. However intermediate versions were developed by Jhonnaton Ascate
% and Christopher Young.
clear all;
close all;

%constants
dbv = @(x) 20*log10(abs(x));
c=3E8; %(m/s) speed of light

%radar parameters
FS = 44.1E3;
Tp = 0.1; %(s) pulse time
N = 8000; %# of samples per pulse
fc = 2590E6; %(Hz) Center frequency (connected VCO Vtune to +5)
recordLength = 0.20;

%filters:
%K: Used to filter incoming signal
K = Test23;
%K3: Used to window receive signal to reduce sidelobe noise
K3 = hanning(100);


%Recording Setup
r = audiorecorder(44100,16,2);
record(r);
pause(recordLength);
stop(r)
Y= getaudiodata(r);

%Set up shift register buffer
bufferVel = [];
bufferSize = 30;
bufferPosition = 0;

%All of the plots are initialized ahead of time and the set function is used
%later on instead of recalling plot

%Calling plot continuously is inefficient because it reinitializes memory whereas
%set simply changes one or two arrays

%Output of Dopplar Radar AFTER windowing
figure(1);
H = plot(Y);
H1 = axis;
ylabel('Amplitude of Doppler Shift (volts)');
xlabel('Time (sec)');
title('Doppler Radar - Received Signal (After Filtering)');
ylim([-5 5]);
xlim([0.005 0.08]);
C = 1;

%Waterfall-ish Diagram
figure(2);
H2 = mesh([0 1;2 3]);
ylim([1 Tp*bufferSize]);
xlim([0 50]);
zlim([-140 10]);
xlabel('Velocity (m/sec)');
ylabel('Time (sec)');
title('Doppler Radar - Velocity');

%Incredibly Rough Peak Detection Algorithm Display
figure(3);
H3 = plot(0,0);
title('Shift Buffer of Maximum Readings over -40 dB');
xlabel('Position in Buffer');
ylabel('Approximate Velocity (m/s)');

highspeed = zeros(bufferSize,1);
while 1,
	%While everything is processing, have the audio recorder record audio - This is basically a ping pong buffer - one buffer is processed
	%as another buffer is filled - although MATLAB obsfucates what buffer is being filled with the recorder wrapper class
    record(r);          
    
    %the input appears to be inverted <- MIT comment
    s = -1*Y(:,2);
	
	%The signal is windowed by a hanning filter 
    K3 = hanning(length(s));
    s = s.*K3;
    %s= filter(K, s);

	%This displays the windowed data to one graph
    set(H, 'YData', s(3:end), 'XData', (3:1:size(s,1))/FS);

    %create doppler vs. time plot data set here
    sif(1,:) = s(1:N);
    
    %subtract the average DC term here
    sif = sif - mean(s);
    zpad = 8*N/2;

    %doppler vs. time plot:
	%This takes the fourier transform of the signal - I am not sure why MIT chose to use the IFFT over the FFT
    v = dbv(ifft(sif,zpad,2));
    v = v(:,1:size(v,2)/2);
    
	%This section attempts to do a very rudimentary form of peak detection based on the top 3 highest signals
    A = sort(v(3:end), 'descend');
    %The three dopplar shifts that have the largest reflection are averaged together - this might require significant tweaking 
	%as there is significant near-DC components that need to be accounted for
    B(1) = find(v == A(1));
    B(2) = find(v == A(2));
    B(3) = find(v == A(3));
    A2 = mean(A(1:3));
    
    %This whole section could be optomized by manually tracking increase in
    %size - however it was not necessary due to the large amount of
    %processing power
	
	%In fact, this loop does not occupy enough time so I had to insert a delay later inorder for the number of samples accumulated to be appropiate. 
    bufferVel = [bufferVel; v];
    if size(bufferVel,1) > bufferSize;
        bufferVel = bufferVel((size(bufferVel,1)- bufferSize + 1):end,:);
    end
    
    %calculate velocity
    delta_f = linspace(0, FS/2, size(bufferVel,2)); %(Hz)
    lambda=c/fc;
    velocity = delta_f*lambda/2;
    avePeakVelo = (velocity(B(1))*A(1) + velocity(B(2))*A(2) + velocity(B(3))*A(3))/(sum(A(1:3)));
    
    %calculate time
    time = linspace(1,Tp*size(bufferVel,1),size(bufferVel,1)); %(sec)

    %plot
    set(H2, 'XDATA',velocity(3:700), 'YDATA', time(1:end), 'ZDATA', bufferVel(1:end,3:700));
    if A2 > -52,%this determines what is considered a detection - it is set manually (which is bad due to environment dependencies).
        highspeed = [highspeed; avePeakVelo];
        if size(highspeed,1) > bufferSize;
            highspeed = highspeed((size(highspeed,1)- bufferSize + 1):end,:);
        end
        set(H3, 'XDATA', 1:1:bufferSize, 'YDATA', highspeed);
    end

    clear SS S v sif ave count start thresh s trig time velocity;
    %Here is where the delay comes into play - after all the processing is done
    pause(recordLength);
	%Stop recording and saving the audio data into Y
    stop(r);
    Y = getaudiodata(r);
end
