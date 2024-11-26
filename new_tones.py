import csv
import random 

chord_chart_M = [
    ["C", "E", "B", "D", "F#", "A"],
    ["C#", "F", "C", "D#", "G", "A#"],
    ["D", "F#", "C#", "E", "G#", "B"],
    ["D#", "G", "D", "F", "A", "C"],
    ["E", "B", "F#", "A#", "C#"],
    ["F", "A", "E", "G", "B", "D"],
    ["F#", "A#", "F", "G#", "C#", "D#"],
    ["G", "B", "F#", "A", "C#", "E"],
    ["G#", "C", "G", "A#", "D", "F"],
    ["A", "C#", "G#", "B", "D#", "F#"],
    ["A#", "D", "A", "C", "E", "G"],
    ["B", "D#", "A#", "C#", "F", "G#"]
]

chord_chart_D = [
    ["C", "E", "A#", "D", "F#", "G#", "A"],
    ["C#", "F", "B", "D#", "G", "A" "A#"],
    ["D", "F#", "C", "E", "G#", "A#", "B"],
    ["D#", "G", "C#", "F", "A", "B", "C"],
    ["E", "G#", "D", "F#", "A#", "C", "C#"],
    ["F", "A", "D#", "G", "B", "C#", "D"],
    ["F#", "A#", "E", "G#", "C", "D", "D#"],
    ["G", "B", "F", "A", "C#", "D#", "E"],
    ["G#", "C", "F#", "A#", "D", "E", "F"],
    ["A", "C#", "G", "B", "D#", "F", "F#"],
    ["A#", "D", "G#", "C", "E", "F#", "G"],
    ["B", "D#", "A", "C#", "F", "G", "G#"]
]

chord_chart = [
    ["C", "E", "G", "B"],
    ["C#", "F", "G#", "C"],
    ["D", "F#", "A", "C#"],
    ["D#", "G", "A#", "D"],
    ["E", "G#", "B", "D#"],
    ["F", "A", "C", "E"],
    ["F#", "A#", "C#", "F"],
    ["G", "B", "D", "F#"],
    ["G#", "C", "D#", "G"],
    ["A", "C#", "E", "G#"],
    ["A#", "D", "F", "A"],
    ["B", "D#", "F#", "A#"]
]

def generate_pitches(original_pitches, chord_index, wave_length, pitch_table):
    note_list = []
    note = ""
    octave = ""
    duration = 0
    frequency = 0
    for i in range(len(original_pitches)):
        octave = original_pitches[i]["octave"]
        note = original_pitches[i]["note"]
        if i == 0 and original_pitches[i]["time"] != 0:
            note_list.append({"duration" : original_pitches[i]["time"], "frequency" : 0}) 
        if i == len(original_pitches) - 1:
            duration = wave_length - original_pitches[i]["time"]
            if duration < 0:
                duration = 0.1
            frequency = 0
            note_list.append({"duration" : duration, "frequency" : frequency})
        elif original_pitches[i]["frequency"] == original_pitches[i + 1]["frequency"]:
            octave = original_pitches[i]["octave"]
            duration = round((original_pitches[i + 1]["time"] - original_pitches[i]["time"]), 1)
            for j in range(len(pitch_table)):
                if original_pitches[i]["frequency"] == pitch_table[j]["frequency"]:
                    for k in range(len(chord_chart)):
                        if pitch_table[j]["note"] == chord_chart[k][0]:
                            note = chord_chart[k][chord_index]
                            break
                    break
            for l in range(len(pitch_table)):
                try:
                    if note == pitch_table[l]["note"] and octave == pitch_table[l]["octave"]:
                        frequency = pitch_table[l]["frequency"]
                        if frequency < original_pitches[i]["frequency"]:
                            frequency = pitch_table[l + 12]["frequency"]
                        note_list.append({"duration" : duration, "frequency" : frequency})
                except IndexError:
                        if note == pitch_table[l]["note"] and octave == pitch_table[l]["octave"]:
                            frequency = pitch_table[l]["frequency"]
                            note_list.append({"duration" : duration, "frequency" : frequency})
        else:
            note = "silence"
            octave = "silence"
            frequency = 0 
            duration = round((original_pitches[i + 1]["time"] - original_pitches[i]["time"]), 1)
            note_list.append({"duration" : duration, "frequency" : frequency})
    return note_list