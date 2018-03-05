
import numpy as np 

SIGNAL_SAMPLE_SIZE = 1024
SINE1024 = [0,0.006135885,0.012271538,0.01840673,0.024541229,0.030674803,0.036807223,0.042938257,0.049067674,0.055195244,0.061320736,0.06744392,0.073564564,0.079682438,0.085797312,0.091908956,0.09801714,0.104121634,0.110222207,0.116318631,0.122410675,0.128498111,0.134580709,0.140658239,0.146730474,0.152797185,0.158858143,0.16491312,0.170961889,0.17700422,0.183039888,0.189068664,0.195090322,0.201104635,0.207111376,0.21311032,0.21910124,0.225083911,0.231058108,0.237023606,0.24298018,0.248927606,0.25486566,0.260794118,0.266712757,0.272621355,0.278519689,0.284407537,0.290284677,0.296150888,0.302005949,0.30784964,0.31368174,0.319502031,0.325310292,0.331106306,0.336889853,0.342660717,0.34841868,0.354163525,0.359895037,0.365612998,0.371317194,0.37700741,0.382683432,0.388345047,0.39399204,0.3996242,0.405241314,0.410843171,0.41642956,0.422000271,0.427555093,0.433093819,0.438616239,0.444122145,0.44961133,0.455083587,0.460538711,0.465976496,0.471396737,0.47679923,0.482183772,0.48755016,0.492898192,0.498227667,0.503538384,0.508830143,0.514102744,0.51935599,0.524589683,0.529803625,0.53499762,0.540171473,0.545324988,0.550457973,0.555570233,0.560661576,0.565731811,0.570780746,0.575808191,0.580813958,0.585797857,0.590759702,0.595699304,0.600616479,0.605511041,0.610382806,0.615231591,0.620057212,0.624859488,0.629638239,0.634393284,0.639124445,0.643831543,0.648514401,0.653172843,0.657806693,0.662415778,0.666999922,0.671558955,0.676092704,0.680600998,0.685083668,0.689540545,0.693971461,0.698376249,0.702754744,0.707106781,0.711432196,0.715730825,0.720002508,0.724247083,0.72846439,0.732654272,0.736816569,0.740951125,0.745057785,0.749136395,0.753186799,0.757208847,0.761202385,0.765167266,0.769103338,0.773010453,0.776888466,0.780737229,0.784556597,0.788346428,0.792106577,0.795836905,0.799537269,0.803207531,0.806847554,0.810457198,0.81403633,0.817584813,0.821102515,0.824589303,0.828045045,0.831469612,0.834862875,0.838224706,0.841554977,0.844853565,0.848120345,0.851355193,0.854557988,0.85772861,0.860866939,0.863972856,0.867046246,0.870086991,0.873094978,0.876070094,0.879012226,0.881921264,0.884797098,0.88763962,0.890448723,0.893224301,0.89596625,0.898674466,0.901348847,0.903989293,0.906595705,0.909167983,0.911706032,0.914209756,0.91667906,0.919113852,0.921514039,0.923879533,0.926210242,0.92850608,0.930766961,0.932992799,0.93518351,0.937339012,0.939459224,0.941544065,0.943593458,0.945607325,0.947585591,0.949528181,0.951435021,0.95330604,0.955141168,0.956940336,0.958703475,0.960430519,0.962121404,0.963776066,0.965394442,0.966976471,0.968522094,0.970031253,0.971503891,0.972939952,0.974339383,0.97570213,0.977028143,0.978317371,0.979569766,0.98078528,0.981963869,0.983105487,0.984210092,0.985277642,0.986308097,0.987301418,0.988257568,0.98917651,0.99005821,0.990902635,0.991709754,0.992479535,0.993211949,0.99390697,0.994564571,0.995184727,0.995767414,0.996312612,0.996820299,0.997290457,0.997723067,0.998118113,0.998475581,0.998795456,0.999077728,0.999322385,0.999529418,0.999698819,0.999830582,0.999924702,0.999981175,1,0.999981175,0.999924702,0.999830582,0.999698819,0.999529418,0.999322385,0.999077728,0.998795456,0.998475581,0.998118113,0.997723067,0.997290457,0.996820299,0.996312612,0.995767414,0.995184727,0.994564571,0.99390697,0.993211949,0.992479535,0.991709754,0.990902635,0.99005821,0.98917651,0.988257568,0.987301418,0.986308097,0.985277642,0.984210092,0.983105487,0.981963869,0.98078528,0.979569766,0.978317371,0.977028143,0.97570213,0.974339383,0.972939952,0.971503891,0.970031253,0.968522094,0.966976471,0.965394442,0.963776066,0.962121404,0.960430519,0.958703475,0.956940336,0.955141168,0.95330604,0.951435021,0.949528181,0.947585591,0.945607325,0.943593458,0.941544065,0.939459224,0.937339012,0.93518351,0.932992799,0.930766961,0.92850608,0.926210242,0.923879533,0.921514039,0.919113852,0.91667906,0.914209756,0.911706032,0.909167983,0.906595705,0.903989293,0.901348847,0.898674466,0.89596625,0.893224301,0.890448723,0.88763962,0.884797098,0.881921264,0.879012226,0.876070094,0.873094978,0.870086991,0.867046246,0.863972856,0.860866939,0.85772861,0.854557988,0.851355193,0.848120345,0.844853565,0.841554977,0.838224706,0.834862875,0.831469612,0.828045045,0.824589303,0.821102515,0.817584813,0.81403633,0.810457198,0.806847554,0.803207531,0.799537269,0.795836905,0.792106577,0.788346428,0.784556597,0.780737229,0.776888466,0.773010453,0.769103338,0.765167266,0.761202385,0.757208847,0.753186799,0.749136395,0.745057785,0.740951125,0.736816569,0.732654272,0.72846439,0.724247083,0.720002508,0.715730825,0.711432196,0.707106781,0.702754744,0.698376249,0.693971461,0.689540545,0.685083668,0.680600998,0.676092704,0.671558955,0.666999922,0.662415778,0.657806693,0.653172843,0.648514401,0.643831543,0.639124445,0.634393284,0.629638239,0.624859488,0.620057212,0.615231591,0.610382806,0.605511041,0.600616479,0.595699304,0.590759702,0.585797857,0.580813958,0.575808191,0.570780746,0.565731811,0.560661576,0.555570233,0.550457973,0.545324988,0.540171473,0.53499762,0.529803625,0.524589683,0.51935599,0.514102744,0.508830143,0.503538384,0.498227667,0.492898192,0.48755016,0.482183772,0.47679923,0.471396737,0.465976496,0.460538711,0.455083587,0.44961133,0.444122145,0.438616239,0.433093819,0.427555093,0.422000271,0.41642956,0.410843171,0.405241314,0.3996242,0.39399204,0.388345047,0.382683432,0.37700741,0.371317194,0.365612998,0.359895037,0.354163525,0.34841868,0.342660717,0.336889853,0.331106306,0.325310292,0.319502031,0.31368174,0.30784964,0.302005949,0.296150888,0.290284677,0.284407537,0.278519689,0.272621355,0.266712757,0.260794118,0.25486566,0.248927606,0.24298018,0.237023606,0.231058108,0.225083911,0.21910124,0.21311032,0.207111376,0.201104635,0.195090322,0.189068664,0.183039888,0.17700422,0.170961889,0.16491312,0.158858143,0.152797185,0.146730474,0.140658239,0.134580709,0.128498111,0.122410675,0.116318631,0.110222207,0.104121634,0.09801714,0.091908956,0.085797312,0.079682438,0.073564564,0.06744392,0.061320736,0.055195244,0.049067674,0.042938257,0.036807223,0.030674803,0.024541229,0.01840673,0.012271538,0.006135885,1.22515E-16,-0.006135885,-0.012271538,-0.01840673,-0.024541229,-0.030674803,-0.036807223,-0.042938257,-0.049067674,-0.055195244,-0.061320736,-0.06744392,-0.073564564,-0.079682438,-0.085797312,-0.091908956,-0.09801714,-0.104121634,-0.110222207,-0.116318631,-0.122410675,-0.128498111,-0.134580709,-0.140658239,-0.146730474,-0.152797185,-0.158858143,-0.16491312,-0.170961889,-0.17700422,-0.183039888,-0.189068664,-0.195090322,-0.201104635,-0.207111376,-0.21311032,-0.21910124,-0.225083911,-0.231058108,-0.237023606,-0.24298018,-0.248927606,-0.25486566,-0.260794118,-0.266712757,-0.272621355,-0.278519689,-0.284407537,-0.290284677,-0.296150888,-0.302005949,-0.30784964,-0.31368174,-0.319502031,-0.325310292,-0.331106306,-0.336889853,-0.342660717,-0.34841868,-0.354163525,-0.359895037,-0.365612998,-0.371317194,-0.37700741,-0.382683432,-0.388345047,-0.39399204,-0.3996242,-0.405241314,-0.410843171,-0.41642956,-0.422000271,-0.427555093,-0.433093819,-0.438616239,-0.444122145,-0.44961133,-0.455083587,-0.460538711,-0.465976496,-0.471396737,-0.47679923,-0.482183772,-0.48755016,-0.492898192,-0.498227667,-0.503538384,-0.508830143,-0.514102744,-0.51935599,-0.524589683,-0.529803625,-0.53499762,-0.540171473,-0.545324988,-0.550457973,-0.555570233,-0.560661576,-0.565731811,-0.570780746,-0.575808191,-0.580813958,-0.585797857,-0.590759702,-0.595699304,-0.600616479,-0.605511041,-0.610382806,-0.615231591,-0.620057212,-0.624859488,-0.629638239,-0.634393284,-0.639124445,-0.643831543,-0.648514401,-0.653172843,-0.657806693,-0.662415778,-0.666999922,-0.671558955,-0.676092704,-0.680600998,-0.685083668,-0.689540545,-0.693971461,-0.698376249,-0.702754744,-0.707106781,-0.711432196,-0.715730825,-0.720002508,-0.724247083,-0.72846439,-0.732654272,-0.736816569,-0.740951125,-0.745057785,-0.749136395,-0.753186799,-0.757208847,-0.761202385,-0.765167266,-0.769103338,-0.773010453,-0.776888466,-0.780737229,-0.784556597,-0.788346428,-0.792106577,-0.795836905,-0.799537269,-0.803207531,-0.806847554,-0.810457198,-0.81403633,-0.817584813,-0.821102515,-0.824589303,-0.828045045,-0.831469612,-0.834862875,-0.838224706,-0.841554977,-0.844853565,-0.848120345,-0.851355193,-0.854557988,-0.85772861,-0.860866939,-0.863972856,-0.867046246,-0.870086991,-0.873094978,-0.876070094,-0.879012226,-0.881921264,-0.884797098,-0.88763962,-0.890448723,-0.893224301,-0.89596625,-0.898674466,-0.901348847,-0.903989293,-0.906595705,-0.909167983,-0.911706032,-0.914209756,-0.91667906,-0.919113852,-0.921514039,-0.923879533,-0.926210242,-0.92850608,-0.930766961,-0.932992799,-0.93518351,-0.937339012,-0.939459224,-0.941544065,-0.943593458,-0.945607325,-0.947585591,-0.949528181,-0.951435021,-0.95330604,-0.955141168,-0.956940336,-0.958703475,-0.960430519,-0.962121404,-0.963776066,-0.965394442,-0.966976471,-0.968522094,-0.970031253,-0.971503891,-0.972939952,-0.974339383,-0.97570213,-0.977028143,-0.978317371,-0.979569766,-0.98078528,-0.981963869,-0.983105487,-0.984210092,-0.985277642,-0.986308097,-0.987301418,-0.988257568,-0.98917651,-0.99005821,-0.990902635,-0.991709754,-0.992479535,-0.993211949,-0.99390697,-0.994564571,-0.995184727,-0.995767414,-0.996312612,-0.996820299,-0.997290457,-0.997723067,-0.998118113,-0.998475581,-0.998795456,-0.999077728,-0.999322385,-0.999529418,-0.999698819,-0.999830582,-0.999924702,-0.999981175,-1,-0.999981175,-0.999924702,-0.999830582,-0.999698819,-0.999529418,-0.999322385,-0.999077728,-0.998795456,-0.998475581,-0.998118113,-0.997723067,-0.997290457,-0.996820299,-0.996312612,-0.995767414,-0.995184727,-0.994564571,-0.99390697,-0.993211949,-0.992479535,-0.991709754,-0.990902635,-0.99005821,-0.98917651,-0.988257568,-0.987301418,-0.986308097,-0.985277642,-0.984210092,-0.983105487,-0.981963869,-0.98078528,-0.979569766,-0.978317371,-0.977028143,-0.97570213,-0.974339383,-0.972939952,-0.971503891,-0.970031253,-0.968522094,-0.966976471,-0.965394442,-0.963776066,-0.962121404,-0.960430519,-0.958703475,-0.956940336,-0.955141168,-0.95330604,-0.951435021,-0.949528181,-0.947585591,-0.945607325,-0.943593458,-0.941544065,-0.939459224,-0.937339012,-0.93518351,-0.932992799,-0.930766961,-0.92850608,-0.926210242,-0.923879533,-0.921514039,-0.919113852,-0.91667906,-0.914209756,-0.911706032,-0.909167983,-0.906595705,-0.903989293,-0.901348847,-0.898674466,-0.89596625,-0.893224301,-0.890448723,-0.88763962,-0.884797098,-0.881921264,-0.879012226,-0.876070094,-0.873094978,-0.870086991,-0.867046246,-0.863972856,-0.860866939,-0.85772861,-0.854557988,-0.851355193,-0.848120345,-0.844853565,-0.841554977,-0.838224706,-0.834862875,-0.831469612,-0.828045045,-0.824589303,-0.821102515,-0.817584813,-0.81403633,-0.810457198,-0.806847554,-0.803207531,-0.799537269,-0.795836905,-0.792106577,-0.788346428,-0.784556597,-0.780737229,-0.776888466,-0.773010453,-0.769103338,-0.765167266,-0.761202385,-0.757208847,-0.753186799,-0.749136395,-0.745057785,-0.740951125,-0.736816569,-0.732654272,-0.72846439,-0.724247083,-0.720002508,-0.715730825,-0.711432196,-0.707106781,-0.702754744,-0.698376249,-0.693971461,-0.689540545,-0.685083668,-0.680600998,-0.676092704,-0.671558955,-0.666999922,-0.662415778,-0.657806693,-0.653172843,-0.648514401,-0.643831543,-0.639124445,-0.634393284,-0.629638239,-0.624859488,-0.620057212,-0.615231591,-0.610382806,-0.605511041,-0.600616479,-0.595699304,-0.590759702,-0.585797857,-0.580813958,-0.575808191,-0.570780746,-0.565731811,-0.560661576,-0.555570233,-0.550457973,-0.545324988,-0.540171473,-0.53499762,-0.529803625,-0.524589683,-0.51935599,-0.514102744,-0.508830143,-0.503538384,-0.498227667,-0.492898192,-0.48755016,-0.482183772,-0.47679923,-0.471396737,-0.465976496,-0.460538711,-0.455083587,-0.44961133,-0.444122145,-0.438616239,-0.433093819,-0.427555093,-0.422000271,-0.41642956,-0.410843171,-0.405241314,-0.3996242,-0.39399204,-0.388345047,-0.382683432,-0.37700741,-0.371317194,-0.365612998,-0.359895037,-0.354163525,-0.34841868,-0.342660717,-0.336889853,-0.331106306,-0.325310292,-0.319502031,-0.31368174,-0.30784964,-0.302005949,-0.296150888,-0.290284677,-0.284407537,-0.278519689,-0.272621355,-0.266712757,-0.260794118,-0.25486566,-0.248927606,-0.24298018,-0.237023606,-0.231058108,-0.225083911,-0.21910124,-0.21311032,-0.207111376,-0.201104635,-0.195090322,-0.189068664,-0.183039888,-0.17700422,-0.170961889,-0.16491312,-0.158858143,-0.152797185,-0.146730474,-0.140658239,-0.134580709,-0.128498111,-0.122410675,-0.116318631,-0.110222207,-0.104121634,-0.09801714,-0.091908956,-0.085797312,-0.079682438,-0.073564564,-0.06744392,-0.061320736,-0.055195244,-0.049067674,-0.042938257,-0.036807223,-0.030674803,-0.024541229,-0.01840673,-0.012271538,-0.006135885]

def decode(data, WIDTH, CHANNELS, CHUNK):
	decoded = [[] for y in range(CHANNELS)] 
	for i in range(0, int(CHUNK * CHANNELS * WIDTH), WIDTH * CHANNELS):
		for j in range(0, CHANNELS):
			decoded[j].append(int.from_bytes(data[i+j*WIDTH:i+j*WIDTH+WIDTH], byteorder='little', signed=True))
	return high_pass(decoded, CHANNELS, CHUNK)

previous_filtered = []
previous_raw = []
alpha = 0.8;
def high_pass_init(channels, chunk):
	global previous_filtered
	global previous_raw
	previous_filtered = [[0 for i in range (chunk)] for y in range(channels)]
	previous_raw = [[0 for i in range (chunk)] for y in range(channels)]

def high_pass(data, channels, chunk):
	global previous_filtered
	global previous_raw
	global alpha

	filtered = [[] for y in range(channels)]
	for i in range(0, channels):
		filtered[i].append(int(alpha * (previous_filtered[i][chunk - 1] + data[i][0] - previous_raw[i][chunk - 1])))
		for j in range(1, chunk):
			filtered[i].append(int(alpha * (filtered[i][j-1] + data[i][j] - data[i][j-1])))

	previous_filtered = filtered
	previous_raw = data
	return filtered

get_sine_period = 0
get_sine_pt = 0
def get_sine_init(PERIOD):
	global get_sine_period
	global get_sine_pt
	get_sine_period = PERIOD
	get_sine_pt = 0

def get_sine(AMP, CHUNK):
	global get_sine_pt
	out = []
	for i in range(0, CHUNK):
		out.append(int(SINE1024[get_sine_pt] * AMP))
		get_sine_pt = int(get_sine_pt + SIGNAL_SAMPLE_SIZE/get_sine_period) % SIGNAL_SAMPLE_SIZE
	return out

def encode_data(data, WIDTH, CHANNELS, CHUNK):
	encoded = bytes([])
	for i in range(0, CHUNK):
		for j in range(0, CHANNELS):
			encoded = encoded + int_to_bytes(data[j][i], WIDTH)

	return encoded

encode_pts = []
period = 0
channels = 0
def encode_init(CHANNELS, PERIOD):
	global encode_pts
	global period
	global channels
	encode_pts = [0 for col in range(0,CHANNELS)]
	period = PERIOD
	channels = CHANNELS

def encode_signal(WIDTH, CHUNK, ch_data):
	# ch_data should look like [[ch1_amp, ch1_dly], [ch2_amp, ch2_dly], ...]

	for i in range(0, channels):
		encode_pts[i] = (encode_pts[i] + SIGNAL_SAMPLE_SIZE - ch_data[i][1]) % SIGNAL_SAMPLE_SIZE

	encoded = bytes([])
	for i in range(0, CHUNK):
		for j in range(0, channels):
			encoded = encoded + int_to_bytes(int(ch_data[j][0]*SINE1024[encode_pts[j]]), WIDTH)
			encode_pts[j] = int(encode_pts[j] + SIGNAL_SAMPLE_SIZE/period) % SIGNAL_SAMPLE_SIZE

	return encoded

def int_to_bytes(x, WIDTH):
    return int(x).to_bytes(WIDTH, 'little', signed=True)