import music21
from music21.note import Note
from music21.pitch import Pitch
import numpy as np


def _get_available_pitches(pitch_lowest: str, pitch_highest: str):
    p_start = Pitch(pitch_lowest)
    p_end = Pitch(pitch_highest)
    assert p_start.octave < p_end.octave or (p_start.octave == p_end.octave and p_start.pitch <= p_end.pitch), "Highest pitch is lower than the lowest pitch."
    ret_pitches = []
    tmp_p = Pitch('C4')

    if p_start.octave == p_end.octave:
        tmp_p.octave = p_start.octave
        for pclass in range(p_start.pitchClass, p_end.pitchClass+1):
            tmp_p.pitchClass = pclass
            ret_pitches.append(tmp_p.nameWithOctave)
    else:
        tmp_p.octave = p_start.octave
        for pclass in range(p_start.pitchClass, 12):
            tmp_p.pitchClass = pclass
            ret_pitches.append(tmp_p.nameWithOctave)
        for octave in range(p_start.octave+1, p_end.octave):
            tmp_p.octave = octave
            for i in range(12):
                tmp_p.pitchClass = i
                ret_pitches.append(tmp_p.nameWithOctave)
        tmp_p.octave = p_end.octave
        for pclass in range(0, p_end.pitchClass):
            tmp_p.pitchClass = pclass
            ret_pitches.append(tmp_p.nameWithOctave)
    
    return ret_pitches

