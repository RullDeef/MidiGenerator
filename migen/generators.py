import random, mido
import migen.atomstructs

"""
    generates randomly placed notes
"""
def generateRandomNotes(n:int, **kwargs):
    notes = []

    timeDiff     = kwargs.get('timeDiff',    1000)
    err_timeDiff = kwargs.get('err_timeDiff', 200)
    duration     = kwargs.get('duration',    1000)
    err_duration = kwargs.get('err_duration', 200)
    velocity     = kwargs.get('velocity',      96)
    err_velocity = kwargs.get('err_velocity',  10)
    keysIntv     = kwargs.get('keys',   (21, 108))
    curr_time = 0

    for i in range(n):
        midikey = random.randint(*keysIntv)
        time = round(curr_time)
        duration = round(random.gauss(duration, err_duration))
        vel = round(random.gauss(velocity, err_velocity))

        notes.append(migen.atomstructs.Note(midikey, time, duration, vel))
        curr_time += abs(random.gauss(timeDiff, err_timeDiff))

    return notes

"""
    generates track, containing midi events with given notes list
"""
def generateTrack(notes:list):
    track = mido.MidiTrack()

    # add some meta messages
    track.append(mido.MetaMessage('channel_prefix', channel=0, time=0))

    # transform notes into midi events
    events = []

    for note in notes:
        events.append({'type': 'on', 'note': note.getValue(), 'time': note.time, 'velocity': note.velocity})
        events.append({'type': 'off', 'note': note.getValue(), 'time': note.time + note.duration, 'velocity': note.velocity})

    # sort events by time attribute
    events.sort(key=lambda event: event['time'])

    # append events to the track
    curr_time = 0
    for event in events:
        note = event['note']
        time = event['time'] - curr_time
        velocity = event['velocity']
        curr_time += time
        track.append(mido.Message('note_' + event['type'], note=note, velocity=velocity, time=time))

    track.append(mido.MetaMessage('end_of_track', time=0))
    return track

"""
    generates template song with one track within meta messages about tempo and time signature
"""
def generateTemplateSong(bpm=120):
    song = mido.MidiFile()

    # add meta track
    song.add_track()
    track = song.tracks[0]

    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm), time=0))
    track.append(mido.MetaMessage('time_signature', numerator=4,
        denominator=4, clocks_per_click=24,
        notated_32nd_notes_per_beat=8, time=0))

    track.append(mido.MetaMessage('end_of_track', time=0))

    return song