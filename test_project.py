import pytest
from project import get_user_recording, parse_pitches, generate_pitch_table, generate_pitch_table, generate_pitches
import librosa

input_file = "start_file.wav"
full_duration = round(librosa.get_duration(filename=input_file), 1)
pitch_table = generate_pitch_table("pitches.csv")
CHORD_SIZE = 3
note_index = 1

def test_generate_pitch_table():
    with pytest.raises(FileNotFoundError):
        generate_pitch_table("")

def test_parse_pitches():
    with pytest.raises(TypeError):
        parse_pitches("tuned_start_file.wav")

def test_generate_pitches():       
    with pytest.raises(TypeError):
        generate_pitches(note_index, full_duration, pitch_table)
