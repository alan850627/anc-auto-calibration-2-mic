
import numpy as np 
import signal

def rms(y):
	y = np.array(signal.high_pass([y], 1, 2048))[0]
	return np.sqrt(np.mean(y**2))

def close_enough(x, y, range):
	return abs(x-y) < range

running_started = False;
avg = 0;
count = 0;
running_count = 0;
mem = []
def running_avg(data):
	global running_started
	global avg
	global count
	global running_count
	global mem

	mem.append(data)
	
	if not running_started:
		avg = data
		running_started = True
	elif count < running_count:
		avg = (avg*count + data)/(count+1)
	else:
		avg = avg + data/running_count - mem[count - running_count]/running_count
	count += 1;
	return avg

def running_avg_init(newn):
	global running_count
	global running_started
	global avg
	global count
	global mem
	running_count = newn
	running_started = False
	avg = 0
	count = 0
	mem = []