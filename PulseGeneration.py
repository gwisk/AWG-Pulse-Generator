import numpy as np
import csv
import matplotlib.pyplot as plt

def gaussian(pulse_width, center, time):
    sigma = pulse_width / (2*np.sqrt(2*np.log(2)))
    return np.exp(-(time-center)**2/(2*sigma**2))
	
#Sampling parameters. Do not change unless planning to change sampling rate
#setting AWG params
#UNITS ARE IN NANOSECONDS
sampling_rate = 92.   #92 Gsamples/second
sample_time = 1./sampling_rate

#Change the pulse width , seperation and overall pattern repetition time
#setting pulse times
pulse_width = 0.2
pulse_seperation = 2 #1e-9
pulse_shape = "gaussian"
pulse_repetition = 20 #10e-9

#total_data_points = int((pulse_width + pulse_seperation + pulse_repetition)//sample_time)
total_time = 5565.2173913#about 5.5 us
total_data_points = int(pulse_repetition/sample_time)
repetitions = int(total_time/pulse_repetition)
print (total_data_points,repetitions)
if total_data_points > 512000:
    print ("Warning. The waveform is bigger than AWG's memory")
	
file_name = "AWG"+"_timebin_"+str(pulse_width)+"ns"+"_sep_"+str(pulse_seperation)+"ns"+"_"+pulse_shape

pulse_width_in_steps = pulse_width//sample_time
pulse_seperation_in_steps = pulse_seperation//sample_time
center = 10 #ns
x = []
y = []
m = []
p_first = []
p_second = []
for j in range(1, repetitions+1):
    if(len(x) > 512000/4):
        break
    for i in range(total_data_points):
        x.append(pulse_repetition*float(j)+float(i)*sample_time)
        current_time = float(i)*sample_time# current time for gaussian peaks
        #if j < 2 :
        #    print(j, i, current_time)
        amp = gaussian(pulse_width, center, current_time)+gaussian(pulse_width, center+pulse_seperation, current_time)
        if amp > 5e-5:
            y.append(amp)
            if x[i] < (center + (pulse_width*2)):
                p_first.append(1)
                p_second.append(0)
            else:
                p_first.append(0)
                p_second.append(1)
        else:
            y.append(0)
            p_first.append(0)
            p_second.append(0)
        m.append(0)

with open(file_name+'.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(zip(y,m))
    