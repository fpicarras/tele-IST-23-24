clear all;

filename = 'pilot.dat';

fid = fopen(filename, 'rb');

pilot = fread(fid, 'float32');

fclose(fid);

filename = 'L-R.dat';

fid = fopen(filename, 'rb');

LmR = fread(fid, 'float32');

fclose(fid);

samp_rate = 125000;

t = (0:(length(pilot)-1)) /samp_rate;

plot(t(8000:8500), pilot(8000:8500), 'DisplayName', 'L+R');
hold on
plot(t(8000:8500), LmR(8000:8500), 'DisplayName', '[R-L]*cos(w_p*t)');
legend('[L-R]*cos(w_p*t)', 'L-R', 'Location','best');

%delay = finddelay(data(8000:8500), data2(8000:8500)) / samp_rate * 1000;

peak1 = findpeaks(pilot(8000:8500), 'MinPeakHeight',0);
peak2 = findpeaks(LmR(8000:8500), 'MinPeakHeight',0);
amp1 = max(peak1)/2;
amp2 = max(peak2)/2;