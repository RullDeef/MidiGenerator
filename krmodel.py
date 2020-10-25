from keras import Sequential
from keras.layers import LSTM, Dropout, Dense, Activation

def make_model(shape, n_vocab):
    model = Sequential()
    model.add(LSTM(512, input_shape=(shape[1], shape[2]), return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(512, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(512))
    model.add(Dense(256))
    model.add(Dropout(0.3))
    model.add(Dense(n_vocab))
    model.add(Activation("softmax"))
    model.compile(loss="categorical_crossentropy", optimizer="rmsprop")

    return model
