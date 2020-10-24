import mido
import migen.atomstructs

"""
    returns list of all notes in track
"""
def extractNotes(track:mido.MidiTrack):
    notes = []
    events = []
    curr_time = 0
    for msg in track:
        msg = msg.dict()
        curr_time += msg['time']
        if msg['type'] == 'note_on':
            msg['start_time'] = curr_time
            events.append(msg)
        elif msg['type'] == 'note_off':
            # search for a linked event that was parsed before
            event = None
            for e in events:
                if e['note'] == msg['note']:
                    event = events.pop(events.index(e))
                    break
            # craft new note from given info
            midikey = event['note']
            time = event['start_time']
            duration = curr_time - time
            velocity = event['velocity']

            note = migen.atomstructs.Note(midikey, time, duration, velocity)
            notes.append(note)

    notes.sort(key=lambda note: note.time)
    return notes

"""
    returns relative frequencies of each tone
    used in given notes
"""
def getToneDomain(notes:list):
    domain = [0] * 12
    for note in notes:
        domain[note.getTone().getValue()] += 1
    total = sum(domain)
    domain = [n/total for n in domain]
    return domain

"""
    returns relative probabilities for given scale type
    base tone does not matter
"""
def getScaleDomain(notes:list, scale:migen.atomstructs.Scale):
    toneDomain = getToneDomain(notes)
    scale = scale.clone()
    scale.base = migen.atomstructs.Tone(0)
    has = lambda T: scale.containsTone(migen.atomstructs.Tone(T))
    scale = [1 if has(n) else 0 for n in range(12)]
    trans = lambda i: (toneDomain[j] * (scale[i:] + scale[:i])[j] for j in range(12))
    domain = [sum(trans(i)) for i in range(12)]
    total = sum(domain)
    domain = [n/total for n in domain]
    return domain

"""
    returns most possible base for major scale
"""
def predictMajScale(notes:list) -> migen.atomstructs.Tone:
    base = migen.atomstructs.Tone(0)
    scale = migen.atomstructs.Scale.maj(base)
    domain = getScaleDomain(notes, scale)
    value = domain.index(max(domain))
    return migen.atomstructs.Tone(value)

"""
    Prints out keyboard for tones
"""
def showKeyboard(notes):
    template = ('┏━━┳━┳━┳━┳━━┳━━┳━┳━┳━┳━┳━┳━━┓\n' +
        '┃{0}{0}┃{1}┃{2}┃{3}┃{4}{4}┃{5}{5}┃{6}┃{7}┃{8}┃{9}┃{10}┃{11}{11}┃\n' * 2 +
        '┃{0}{0}┗┳┛{2}┗┳┛{4}{4}┃{5}{5}┗┳┛{7}┗┳┛{9}┗┳┛{11}{11}┃\n' +
        '┃{0}{0}{0}┃{2}{2}{2}┃{4}{4}{4}┃{5}{5}{5}┃{7}{7}{7}┃{9}{9}{9}┃{11}{11}{11}┃\n' * 2 +
        '┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛')

    notes = list(map(lambda n: '█' if 1 - n < 1e-12 else ' ', notes))
    print(template.format(*notes))

def showKeyboardScale(scale):
    notes = [migen.atomstructs.Tone(i) for i in range(12)]
    notes = map(scale.containsTone, notes)
    notes = list(map(int, notes))
    showKeyboard(notes)

if __name__ == '__main__':
    from migen.atomstructs import *

    showKeyboardScale(Scale.min(Tone('C')))