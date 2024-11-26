import os
import csv
import librosa
import pyaudio
import sounddevice
import soundfile
from new_tones import generate_pitches
from pydub import AudioSegment
from pydub.playback import play
import wave
import sys
import crepe
from scipy.io import wavfile
from scipy.io.wavfile import write
import tensorflow.python as tf
from sine_wave import tone
from auto_tune import tune_file 

CHORD_SIZE = 3


def main():
    # record audio
    #input_file = get_user_recording()
    input_file="start_file.wav"
    # auto tune the wav file
    tune_file(input_file)
    # get the duration of the wave file
    full_duration = round(librosa.get_duration(filename=input_file), 1)
    # generate a table with frequency, pitch, and octaves 
    pitch_table = generate_pitch_table("pitches.csv")
    # parse through the recording to compare with the table and return matching pitches
    input_pitches = parse_pitches("tuned_start_file.wav", pitch_table, full_duration)
    # set number of notes to apply the chords
    note_range = CHORD_SIZE
    # Set index of chord being built 
    note_index = 1
    # generate sine waves matching the found pitches at the correct duration 
    while note_range > 0:
        # alter the frequencies to specific intervals
        note_list = generate_pitches(input_pitches, note_index, full_duration, pitch_table)
        # generate the new tone waves
        wave_count = generate_tone_waves(note_list, len(note_list))
        # combine generated wave files 
        combine_files(wave_count)
        # Overlay the two files
        if note_range < CHORD_SIZE:
            file_overlay("final_wave.wav", 10, note_range)
        else:
            file_overlay(input_file, 10, note_range)
        note_range -= 1
        note_index += 1
    # Clear wave files used for new final file
    clean_data(wave_count * CHORD_SIZE)
    # Play file 
    play_new("final_wave.wav")

# Citing deepgram for use of pyAudio library for recording sound (https://deepgram.com/learn/best-python-audio-manipulation-tools#recording-audio-data-with-python)
def get_user_recording():
    try:
        chunk = 1024
        sample_format = pyaudio.paInt16
        channels = 1
        fs = 44100
        seconds = 15
        filename = "start_file.wav"
        p = pyaudio.PyAudio()
        print("Recording ...")
        stream = p.open(format = sample_format,
                        channels = channels,
                        rate = fs,
                        frames_per_buffer = chunk,
                        input = True)
        frames = []
        for _ in range(0, int(fs/chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()
        print(" ... Ending Recording")
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(sample_format))
            wf.setframerate(fs)
            wf.writeframes(b''.join(frames))
            wf.close()
        return filename
    except OSError:
        sys.exit("Microphone must be plugged in for usage")


def parse_pitches(audiofile, pitches, wave_length):
    sr, audio = wavfile.read(audiofile)
    time, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=True)
    pitch_time_stamps = []
    pitch_found = False
    # find each pitch within the recording and store its values
    for i in range(len(time)):
        time_stamp = {"time": time[i], "frequency" : frequency[i], "confidence" : confidence[i]}
        #pprint.pprint(time_stamp)
        if time_stamp["confidence"] > 0.8 and pitch_found == False:
            pitch_time_stamps.append(time_stamp)
            pitch_found = True
        elif time_stamp["confidence"] < 0.8 and pitch_found == True:
            time_stamp = {"time": time[i-1], "frequency" : frequency[i-1], "confidence" : confidence[i-1]}
            pitch_time_stamps.append(time_stamp)
            pitch_found = False
        elif i == len(time) - 1 and pitch_found == True:
            pitch_time_stamps.append(time_stamp)
    return_pitches = []
    # match pitches in recording to the pitch table
    for point in pitch_time_stamps:
        for i in range(len(pitches)):
            if  (pitches[i]["frequency"] - 7) <= point["frequency"] <= (pitches[i]["frequency"] + 7):
                return_pitches.append({"note" : pitches[i]["note"], "octave" : pitches[i]["octave"], "time" : point["time"], "frequency" : pitches[i]["frequency"]})
    return return_pitches

def generate_tone_waves(notes, wave_count):
    wave_file = 0
    note_index = 0
    # generate wave files for pitches and silences in order
    while wave_count > 0:
        wave_file += 1
        tone(notes[note_index]["duration"], notes[note_index]["frequency"], f"wave{wave_file}.wav")
        print(f"wave{wave_file} generated successfully")
        note_index += 1
        wave_count -= 1
    return wave_file


def generate_pitch_table(file):
    pitches = []
    with open(file) as file:
        reader = csv.DictReader(file)
        for row in reader:
            pitches.append({"note" : row["note"], "octave" : row["octave"], "frequency" : float(row["frequency"])})
    return pitches

#Citing deepgrams tutorials on combining files
def combine_files(count):
    wave_count = 1
    while count > 0:
        if wave_count == 1:
            final_wave = AudioSegment.from_wav(f"wave{wave_count}.wav")
            final_wave.export("output_file.wav", format="wav")
            wave_count += 1
            count -= 1
        else: 
            first_file = AudioSegment.from_wav("output_file.wav")
            second_file = AudioSegment.from_wav(f"wave{wave_count}.wav")
            combined = first_file + second_file
            combined.export("output_file.wav", format="wav")
            wave_count += 1
            count -= 1

#Citing Deepgram's tutorials on overlaying wav files
def file_overlay(file, amplitude, complete_count):
    file_one = AudioSegment.from_wav(file)
    file_two = AudioSegment.from_wav("output_file.wav")
    # Increase file_two's volume 
    louder = file_two + amplitude
    overlay = file_one.overlay(louder)
    overlay.export("final_wave.wav", format="wav")

def clean_data(count):
    wave_number = 1
    while count > 0:
        if os.path.exists(f"wave{wave_number}.wav"):
            os.remove(f"wave{wave_number}.wav")
            wave_number += 1
            count -= 1
        else:
            wave_number += 1
            count -= 1
            pass
    if os.path.exists("output_file.wav"):
        os.remove("output_file.wav")

#Citing Deepgram's tutorials on playing audio
def play_new(file):
    filename = file
    data, fs = soundfile.read(filename, dtype='float32')
    sounddevice.play(data, fs)
    status = sounddevice.wait()

if __name__ == "__main__":
    main()
