
import signal
import copy

mem = []
play_pt = 0
mem_size = 0
def recording_init():
	global mem
	mem = []

def play_init():
	global mem_size
	global mem
	global play_pt
	mem_size = len(mem)
	play_pt = 0

def get_next():
	global mem
	global mem_size
	global play_pt
	play_pt = (play_pt + 1)%mem_size
	return copy.deepcopy(mem[play_pt])

def record(data):
	global mem
	mem.append(copy.deepcopy(data))


from collections import deque
sample_pt = 0
queue_size = 3
queue_mem = deque()
def queue_init(CHUNK):
	global queue_mem
	global sample_pt
	global queue_size
	queue_size = 3
	queue_mem = deque([[] for i in range(0,queue_size)])
	sample_pt = CHUNK*(queue_size - 1)

def queue_record(data):
	if (len(queue_mem) >= queue_size):
		queue_mem.popleft()
	queue_mem.append(copy.deepcopy(data))

# Gets the signal recorded on ch according to delay!!\
def queue_get_signal(CHUNK, ch, dly):
	global sample_pt
	global queue_size
	sample_pt -= int(dly)

	if (sample_pt > CHUNK*(queue_size - 1)):
		print("OOPS BECOMING NON-CAUSAL!!!!")
		sample_pt -= CHUNK

	out = []
	for i in range(sample_pt, CHUNK + sample_pt):
		out.append(queue_mem[int(i/CHUNK)][ch][i%CHUNK])

	if (sample_pt < CHUNK):
		queue_size += 1
		sample_pt += CHUNK

	return out