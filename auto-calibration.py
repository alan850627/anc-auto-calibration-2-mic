import pyaudio
import time
import avg
import signal
import recording
import numpy as np
from enum import Enum

class state(Enum):
	STARTED = 0
	RECORD_NOISE = 1
	RECORD_NOISE_DONE = 2
	PLAY_NOISE = 3
	MATCH_PLAYBACK = 5
	MATCH_PLAYBACK_DONE = 6
	MEASURE_BOTH_INIT = 7
	MEASURE_BOTH = 8
	DELAY_SPEAKER = 9
	EXPEDITE_SPEAKER = 10
	DONE = 11

# GLOBALS
WIDTH = 2
CHANNELS = 2
RATE = 44100
CHUNK = 2048
STATE = state.STARTED
NEXT_STATE = state.DELAY_SPEAKER

# DATA
counter = 0
alternate_counter = 0
freq = 1000
period = int(RATE/freq)
prev_sound = 0
min_sound = 0
max_sound = 0

noise_rms = 0
noise_amp = 20000
noise_dly = 0

spk_rms = 0
spk_mult = 0.5
spk_dly = 0

avg.running_avg_init(25)
signal.encode_init(CHANNELS, period)
signal.high_pass_init(CHANNELS, CHUNK)
p = pyaudio.PyAudio()

######################################################
#                                                    #
# [ch1_spk] --> [ch1_mic]    [ch2_mic] <-- [ch2_spk] #
#                   |                          |     #
#                   |_------>[computer]------>_|     #
#                                                    #
######################################################

def callback(data, frame_count, time_info, status):
	# GLOBALS
	global WIDTH
	global CHANNELS
	global RATE
	global CHUNK
	global STATE
	global NEXT_STATE

	# DATA
	global counter
	global alternate_counter
	global freq
	global period
	global prev_sound
	global min_sound
	global max_sound

	global noise_rms
	global noise_amp
	global noise_dly

	global spk_rms
	global spk_mult
	global spk_dly


	out = bytes([])

	#######################################
	#            STATE STARTED            #
	#######################################
	if (STATE == state.STARTED):
		de = signal.decode(data, WIDTH, CHANNELS, CHUNK)
		min_sound = avg.running_avg(avg.rms(de[0]))
		out = signal.encode_signal(WIDTH, CHUNK,[[1,0],[1,0]]) #Apparently setting all values to 0 turns the sound stream off...
		
		if (counter > 50):
			STATE = state.PLAY_NOISE;
			counter = 0;
			signal.encode_init(CHANNELS, period)
			out = signal.encode_signal(WIDTH, CHUNK, [[noise_amp, 0],[0,0]])
	
	#######################################
	#           STATE PLAY NOISE          #
	#######################################
	elif (STATE == state.PLAY_NOISE):
		out = signal.encode_signal(WIDTH, CHUNK, [[noise_amp, 0],[0,0]])

		if (counter > 50):
			STATE = state.RECORD_NOISE;
			counter = 0;
			avg.running_avg_init(25)
			recording.recording_init()
			print(STATE)

	#######################################
	#          STATE RECORD NOISE         #
	#######################################
	elif (STATE == state.RECORD_NOISE):
		de = signal.decode(data, WIDTH, CHANNELS, CHUNK)
		recording.record(de)
		noise_rms = avg.running_avg(avg.rms(de[1]))
		out = signal.encode_signal(WIDTH, CHUNK, [[noise_amp, 0],[0,0]])

		if (counter > 50):
			print("noise RMS:%f" %noise_rms)
			recording.play_init()
			STATE = state.RECORD_NOISE_DONE;
			counter = 0

	#######################################
	#       STATE RECORD NOISE DONE       #
	#######################################
	elif(STATE == state.RECORD_NOISE_DONE):
		de = recording.get_next()
		de[1] = [int(i * spk_mult) for i in de[0]]
		de[0] = [0 for k in range(0, CHUNK)]
		out = signal.encode_data(de, WIDTH, CHANNELS, CHUNK)
		if (counter > 10):
			STATE = state.MATCH_PLAYBACK
			avg.running_avg_init(5)
			counter = 0

	#######################################
	#        STATE MATCH PLAYBACK         #
	#######################################
	elif(STATE == state.MATCH_PLAYBACK):
		re = recording.get_next()
		re[1] = [int(i * spk_mult) for i in re[0]]
		re[0] = [0 for k in range(0, CHUNK)]

		out = signal.encode_data(re, WIDTH, CHANNELS, CHUNK)

		de = signal.decode(data, WIDTH, CHANNELS, CHUNK)
		spk_rms = avg.running_avg(avg.rms(de[1]))

		if (counter > 10):
			counter = 0
			avg.running_avg_init(5)

			if (avg.close_enough(spk_rms, noise_rms, 10)):
				STATE = state.MATCH_PLAYBACK_DONE

			# NOT SURE IF GOOD
			elif (spk_rms > noise_rms):
				spk_mult = spk_mult - (spk_rms - noise_rms)/100000
			elif (spk_rms < noise_rms):
				spk_mult = spk_mult + (noise_rms - spk_rms)/100000

	#######################################
	#      STATE MATCH PLAYBACK DONE      #
	#######################################
	elif (STATE == state.MATCH_PLAYBACK_DONE):
		print("AMPLITUDE MATCHED!")
		alternate_counter = 0
		counter = 0
		avg.running_avg_init(5)
		signal.get_sine_init(period)
		max_sound = spk_rms + noise_rms
		recording.queue_init(CHUNK)

		de = signal.decode(data, WIDTH, CHANNELS, CHUNK)
		recording.queue_record(de)
		re = recording.queue_get_signal(CHUNK, 0, 0)
		de[1] = [i * spk_mult for i in re]
		de[0] = signal.get_sine(noise_amp, CHUNK)
		out = signal.encode_data(de, WIDTH, CHANNELS, CHUNK)

		STATE = state.MEASURE_BOTH_INIT

	#######################################
	#       STATE MEASURE BOTH INIT       #
	#######################################
	elif (STATE == state.MEASURE_BOTH_INIT):
		dly = 18
		print(min_sound,prev_sound,spk_dly)
		spk_dly += dly

		de = signal.decode(data, WIDTH, CHANNELS, CHUNK)
		prev_sound = avg.running_avg(avg.rms(de[1]))
		recording.queue_record(de)
		re = recording.queue_get_signal(CHUNK, 0, dly)
		de[1] = [i * spk_mult for i in re]
		de[0] = signal.get_sine(noise_amp, CHUNK)
		out = signal.encode_data(de, WIDTH, CHANNELS, CHUNK)

		avg.running_avg_init(5)
		print("Begin tweaking phase!")
		STATE = state.DELAY_SPEAKER
		counter = 0

	#######################################
	#         STATE DELAY SPEAKER         #
	#######################################
	elif (STATE == state.DELAY_SPEAKER):
		NEXT_STATE = state.DELAY_SPEAKER

		# dly = int((prev_sound - min_sound)/(max_sound-min_sound)*RATE/signal.SIGNAL_SAMPLE_SIZE)+1
		dly = 1
		print(min_sound,prev_sound,spk_dly)
		spk_dly += dly

		de = signal.decode(data, WIDTH, CHANNELS, CHUNK)
		recording.queue_record(de)
		re = recording.queue_get_signal(CHUNK, 0, dly)
		de[1] = [i * spk_mult for i in re]
		de[0] = signal.get_sine(noise_amp, CHUNK)
		out = signal.encode_data(de, WIDTH, CHANNELS, CHUNK)

		STATE = state.MEASURE_BOTH

	#######################################
	#       STATE EXPEDITE SPEAKER        #
	#######################################
	elif (STATE == state.EXPEDITE_SPEAKER):
		NEXT_STATE = state.EXPEDITE_SPEAKER

		# dly = int((prev_sound - min_sound)/(max_sound-min_sound)*RATE/signal.SIGNAL_SAMPLE_SIZE)+1
		dly = 1
		print(min_sound,prev_sound,spk_dly)
		spk_dly -= dly

		de = signal.decode(data, WIDTH, CHANNELS, CHUNK)
		recording.queue_record(de)
		re = recording.queue_get_signal(CHUNK, 0, -dly)
		de[1] = [i * spk_mult for i in re]
		de[0] = signal.get_sine(noise_amp, CHUNK)
		out = signal.encode_data(de, WIDTH, CHANNELS, CHUNK)

		STATE = state.MEASURE_BOTH

	#######################################
	#         STATE MEASURE BOTH          #
	#######################################
	elif (STATE == state.MEASURE_BOTH):
		de = signal.decode(data, WIDTH, CHANNELS, CHUNK)
		cur_sound = avg.running_avg(avg.rms(de[1]))
		recording.queue_record(de)
		re = recording.queue_get_signal(CHUNK, 0, 0)
		de[1] = [i * spk_mult for i in re]
		de[0] = signal.get_sine(noise_amp, CHUNK)
		out = signal.encode_data(de, WIDTH, CHANNELS, CHUNK)

		if counter > 10:
			if (cur_sound <= min_sound or alternate_counter > 10): # LOL FIX!!
				STATE = state.DONE
				# Actual delay: queue_size * CHUNK - sample_pt
				print("freq: %d, noise_amp: %d, noise_dly: %d, spk_mult: %f spk_dly: %d" %(freq, noise_amp, noise_dly, spk_mult, spk_dly ))

			elif (cur_sound < prev_sound):
				STATE = NEXT_STATE
			else:
				alternate_counter += 1
				if(NEXT_STATE == state.EXPEDITE_SPEAKER):
					STATE = state.DELAY_SPEAKER
				else:
					STATE = state.EXPEDITE_SPEAKER
			print(STATE)
			prev_sound = cur_sound
			avg.running_avg_init(5)
			counter = 0

	#######################################
	#             STATE DONE              #
	#######################################
	elif (STATE == state.DONE):
		de = signal.decode(data, WIDTH, CHANNELS, CHUNK)
		cur_sound = avg.running_avg(avg.rms(de[1]))
		recording.queue_record(de)
		re = recording.queue_get_signal(CHUNK, 0, 0)
		de[1] = [i * spk_mult for i in re]
		de[0] = signal.get_sine(noise_amp, CHUNK)
		out = signal.encode_data(de, WIDTH, CHANNELS, CHUNK)

		if (counter > 100):
			print(min_sound, cur_sound)
			counter = 0

	counter += 1;
	return (out, pyaudio.paContinue);

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                frames_per_buffer=CHUNK,
                input=True,
                output=True,
                stream_callback=callback)

stream.start_stream()

while True:
    time.sleep(0.1)

stream.stop_stream()
stream.close()

p.terminate()
