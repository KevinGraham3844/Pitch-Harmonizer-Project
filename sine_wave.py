'''
This library has been altered to allow for parameters from the project file
the link to the original is:
https://gist.github.com/alessandrocuda/9df6043b79e68e3ddc1c262eddcfa015
'''

# #MIT License

# Copyright (c) [2018] [Alessandro Cudazzo, Francesco Capuzzolo]

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Generate a sine wave and save it in a wav file.
# works on python 2 and python 3
#
# without agruments the behaviour generate a sine_wave.wav file
# 10 sec, 400hz, mono, volume = 10
#
# optional arguments:
#	-h, --help    show this help message and exit
# 	-s            set stereo mode; if missing, the file will be saved in mono
#	-t DURATION   set sine wave's duration in seconds
#	-f FREQUENCY  set sine wave's frequency [0,20000]Hz
#	-v VOLUME     set sine wave's amplitude [1,10]
#	-o OUTPUT     set name of wav file
import argparse, math, wave, struct
'''
parser = argparse.ArgumentParser(description='Generate a sine wave.')

parser.add_argument('-s', action='store_true', help='set stereo mode; if missing, the file will be saved in mono', default=False, dest='stereo')
parser.add_argument('-t', action='store', type=float, help='set sine wave\'s duration in seconds', default=10.0, dest='duration')
parser.add_argument('-f', action='store', type=float, help='set sine wave\'s frequency [0,20000]Hz', default=400.0, dest='frequency')
parser.add_argument('-v', action='store', type=float, help='set sine wave\'s amplitude [1,10]', default=10, dest='volume')
parser.add_argument('-o', action='store', help='set name of wav file', default='sine_wave.wav', dest='output')

args = parser.parse_args()
'''
def tone(seconds, frequency, fileout):
	IS_STEREO = False #args.stereo
	SAMPLE_RATE = 44100.0 		# hertz
	NUM_SECONDS = seconds #args.duration  	# seconds
	FREQUENCY = frequency #args.frequency    	# hertz
	VOLUME = 1000 #args.volume * 100
	OUTPUT_FILE = fileout #args.output 	# filepath

	try:
		assert NUM_SECONDS > 0.0, 'Duration must be higher than 0 seconds.'
	except AssertionError:
		pass
	assert 0 <= FREQUENCY <= 20000.0, 'Wave frequency must be positive and lesser than 20000 Hz.'
	assert 100 <= VOLUME <= 1000.0, 'Volume must be higher than 0 and lesser than 100.'
	'''
	assert NUM_SECONDS > 0.0, 'Duration must be higher than 0 seconds.'
	assert 0 <= FREQUENCY <= 20000.0, 'Wave frequency must be positive and lesser than 20000 Hz.'
	assert 100 <= VOLUME <= 1000.0, 'Volume must be higher than 0 and lesser than 100.'
	'''
	log = (
		'Generating a sine wave.\n\tSample rate: '+str(SAMPLE_RATE)+
		' Hz\n\tDuration: '+ str(NUM_SECONDS)+
		' s\n\tFrequency: '+str(FREQUENCY)+ 
		' Hz\n\tStereo: '+str(IS_STEREO)+
		'\n\tVolume: '+str(VOLUME)+
		'\n\tDestination: '+str(OUTPUT_FILE)
		)

	print (log)

	file = wave.open(OUTPUT_FILE,'wb')
	file.setnchannels(2 if IS_STEREO else 1)
	file.setsampwidth(2) 
	file.setframerate(SAMPLE_RATE)

	for i in range(int(NUM_SECONDS * SAMPLE_RATE)):
		value = int(VOLUME * math.sin(2 * FREQUENCY * math.pi * float(i) / float(SAMPLE_RATE)))
		data = struct.pack('<hh', value, value) if IS_STEREO else struct.pack('<h', value)
		file.writeframesraw(data)

	file.close()
