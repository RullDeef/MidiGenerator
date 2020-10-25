from os.path import isfile
import pickle
from glob import glob
from music21 import note, chord, instrument, converter

class Serializer(object):
    def __init__(self):
        self.notes = []
        self.pitchnames = []
        self.note_to_int = dict()
        self.n_vocab = 0

        if isfile("nt.dat"):
            with open("nt.dat", "rb") as file:
                self.notes, self.pitchnames, self.note_to_int, self.n_vocab = pickle.load(file)
        else:
            for file in glob("data/*.mid"):
                try:
                    midi = converter.parse(file)
                    notes_to_parse = None

                    parts = instrument.partitionByInstrument(midi)

                    if parts: # file has instrument parts
                        notes_to_parse = midi.parts[0].recurse()
                    else:
                        notes_to_parse = midi.flat.notes

                    for element in notes_to_parse:
                        if isinstance(element, note.Note):
                            self.notes.append(str(element.pitch))
                        elif isinstance(element, chord.Chord):
                            self.notes.append(".".join(str(n) for n in element.normalOrder))
                except Exception as e:
                    print(f"could not load midi {file}. Reason: {e}")

            # get all pitch names
            self.pitchnames = sorted(set(self.notes))
            self.n_vocab = len(self.pitchnames)

            # create a dictionary to map pitches to integers
            self.note_to_int = dict((note, number) for number, note in enumerate(self.pitchnames))

            with open("nt.dat", "wb") as file:
                pickle.dump((self.notes, self.pitchnames, self.note_to_int, self.n_vocab), file)
