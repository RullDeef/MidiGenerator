import glob
import np_utils
import numpy as np
from music21 import converter, instrument, note, chord
from keras import Sequential
from keras.utils import to_categorical
from keras.layers import LSTM, Dropout, Dense, Activation
from keras.callbacks import ModelCheckpoint

from serializer import Serializer

print("reading midi files...")

ser = Serializer()
notes = ser.notes
pitchnames = ser.pitchnames
note_to_int = ser.note_to_int
n_vocab = ser.n_vocab

print("readed all files!")

sequence_length = 100

network_input = []
network_output = []

print("creating corresponding outputs...")

# create input sequences and the corresponding outputs
for i in range(0, len(notes) - sequence_length, 1):
    sequence_in = notes[i:i + sequence_length]
    sequence_out  = notes[i + sequence_length]
    network_input.append([note_to_int[char] for char in sequence_in])
    network_output.append(note_to_int[sequence_out])

print("created!")

n_patterns = len(network_input)

# reshape the input into a format compatible with LSTM layers
network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
# normalize input
network_input = network_input / float(n_vocab)

network_output = to_categorical(network_output)

print("building model...")

# build a keras model
model = Sequential()
model.add(LSTM(512, input_shape=(network_input.shape[1], network_input.shape[2]), return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(512, return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(512))
model.add(Dense(256))
model.add(Dropout(0.3))
model.add(Dense(n_vocab))
model.add(Activation("softmax"))
model.compile(loss="categorical_crossentropy", optimizer="rmsprop")

filepath = "ML/weights/weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"

checkpoint = ModelCheckpoint(filepath, monitor="loss", verbose=0, save_best_only=True, mode="min")
callbacks_list = [checkpoint]

print("builded!\nnow training...")

model.fit(network_input, network_output, epochs=200, batch_size=64, callbacks=callbacks_list)

print("trained!")
