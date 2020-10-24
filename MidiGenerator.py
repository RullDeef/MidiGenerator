import migen

song = migen.generators.generateTemplateSong(300)

notes = migen.generators.generateRandomNotes(100)
track = migen.generators.generateTrack(notes)
song.tracks.append(track)

song.save('./music/mid4.mid')
print('done!')


from migen.atomstructs import *
from migen.analizers import *
from migen.generators import *

s = Scale.maj(Tone('C'))

from random import sample
notes = sample(range(40, 80), 20)
notes = list(map(Note, notes))

from mido import MidiFile

song = MidiFile('./music/test.mid')
notes = extractNotes(song.tracks[1])
notes.sort(key=lambda n: n.time)

print('notes:', notes)

toneDomain = getToneDomain(notes)
print('tone domain:', toneDomain)

majDomain = getScaleDomain(notes, Scale.maj(Tone('C')))
print('major scale domain:', majDomain)

scale = Scale.maj(predictMajScale(notes))
print('Prediction:', scale.base)
showKeyboardScale(scale)