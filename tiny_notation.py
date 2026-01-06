from music21 import stream, note, chord, converter

def get_tinynotation_octave(pitch):
    octave = pitch.octave
    step = pitch.step.lower()
    
    if octave <= 1:
        return pitch.step.upper() * (3 - octave)
    elif octave == 2:
        return pitch.step.upper() * 2
    elif octave == 3:
        return pitch.step.upper()
    elif octave == 4:
        return step
    else:
        return step + "'" * (octave - 4)

def accidental_to_str(accidental):
    if accidental is None:
        return ''
    alter = accidental.alter
    if alter == 1:
        acc = '#'
    elif alter == -1:
        acc = '-'
    elif alter == 0:
        acc = 'n'
    elif alter == 2:
        acc = '##'
    elif alter == -2:
        acc = '--'
    else:
        acc = ''
    if getattr(accidental, 'editorial', False):
        acc = f"({acc})"
    return acc

def duration_to_str(elem, prev_duration):
    dur_map = {
        'whole': '1',
        'half': '2',
        'quarter': '4',
        'eighth': '8',
        '16th': '16',
        '32nd': '32',
        '64th': '64'
    }
    dur_num = dur_map.get(elem.duration.type, '4')
    dot_str = '.' * elem.duration.dots
    full = dur_num + dot_str
    if full == prev_duration:
        return '', full
    return full, full

def tie_to_str(elem):
    if elem.tie and elem.tie.type in ('start', 'continue'):
        return '~'
    return ''

def note_to_tn(n, duration_str, tie_str):
    octave_str = get_tinynotation_octave(n.pitch)
    acc = accidental_to_str(n.pitch.accidental)
    return f"{n.pitch.step.lower()}{octave_str[1:]}{acc}{duration_str}{tie_str}"

def chord_to_tn(ch, duration_str, tie_str):
    notes = []
    for n in ch.notes:
        octave_str = get_tinynotation_octave(n.pitch)
        acc = accidental_to_str(n.pitch.accidental)
        notes.append(f"{n.pitch.step.lower()}{octave_str[1:]}{acc}")
    return f"<{' '.join(notes)}>{duration_str}{tie_str}"

def wrap_tuplet(elem, content):
    for tup in elem.duration.tuplets:
        if tup.numberNotesActual == 3 and tup.numberNotesNormal == 2:
            return f"trip{{{content}}}"
        if tup.numberNotesActual == 4 and tup.numberNotesNormal == 3:
            return f"quad{{{content}}}"
    return content

def voice_to_tinynotation_custom(part: stream.Part, use_bars=True) -> str:
    tn = []
    prev_duration = None
    bar_count = 1

    for meas in part.getElementsByClass('Measure'):
        if use_bars:
            tn.append(f"[{bar_count}]")
            bar_count += 1

        for elem in meas.notesAndRests:
            duration_str, prev_duration = duration_to_str(elem, prev_duration)
            tie_str = tie_to_str(elem)

            if isinstance(elem, note.Rest):
                content = f"r{duration_str}{tie_str}"

            elif isinstance(elem, note.Note):
                content = note_to_tn(elem, duration_str, tie_str)

            elif isinstance(elem, chord.Chord):
                content = chord_to_tn(elem, duration_str, tie_str)

            else:
                continue

            content = wrap_tuplet(elem, content)
            tn.append(content)

        if use_bars:
            tn.append("|")

    return " ".join(tn)

def score_to_tinyscore(score: stream.Score) -> str:
    tinyscore = ""
    for i, voice in enumerate(score.parts):
        tn = voice_to_tinynotation_custom(voice, use_bars=True)
        tinyscore += f"V{i}: {tn}\n"
    return tinyscore
