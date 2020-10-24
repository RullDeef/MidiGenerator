class Tone(object):
    """
        Base class for representing tone (value from 0 to 11)
    """
    toneValues = {'C':0, 'D':2, 'E':4, 'F':5, 'G':7, 'A':9, 'B':11}

    """
        int value = 0...11
        char value = 'C' ... 'G'
    """
    def __init__(self, value):
        if type(value) == str:
            value = Tone.valueFromStr(value)

        self.base = Tone.getBaseFromValue(value)
        self.alteration = value % 12 - self.base

    def clone(self):
        tone = Tone(0)
        tone.base = self.base
        tone.alteration = self.alteration
        return tone

    """
        returns true value of a tone
    """
    def getValue(self):
        return (self.base + self.alteration) % 12
    
    def transpose(self, interval):
        self.base += interval.value
        self.base %= 12

    """
        converts string representation of tone into its value
    """
    @classmethod
    def valueFromStr(cls, value):
        value = value.upper()
        base = Tone.toneValues[value[0]]
        if len(value) > 1:
            for sign in value[1:]:
                if sign == 'b': base -= 1
                elif sign == '#': base += 1
        return base

    """
        reeturns the value that linked with base tone (no alterations)
    """
    @classmethod
    def getBaseFromValue(cls, value):
        bases = [0, 2, 4, 5, 7, 9, 11]
        value %= 12
        if value in bases:
            return value
        for base in bases:
            if abs(value - base) <= 1:
                return base
        assert False, 'something went wrong...'

    """
        converts midikey to a particular tone
        midikey of C0 = 21
    """
    @classmethod
    def fromMidiKey(cls, midikey):
        return Tone(midikey - 24)

    """
        returns representation of tone
    """
    def __repr__(self):
        valuesTones = dict(zip(Tone.toneValues.values(), Tone.toneValues.keys()))
        res = valuesTones[self.base]
        alt = self.alteration
        while alt > 0:
            res += '#'
            alt -= 1
        while alt < 0:
            res += 'b'
            alt += 1
        return res


class Note(object):
    """
        Advanced tone representation
        uses midi keys as values
    """

    """
        int midikey = 21...109
        char midikey = 'A0'...'C8'

        TODO: make use of alteration signs!
        bemols wont work in current realization!!!
    """
    def __init__(self, midikey, time=0, duration=1000, velocity=127):
        if type(midikey) == str:
            midikey = Note.midiKeyFromStr(midikey)
        self.base = Tone.getBaseFromValue(midikey)
        self.alteration = midikey % 12 - self.base
        self.octave = midikey // 12
        self.time = time
        self.duration = duration
        self.velocity = velocity

    """
        in fact returns midikey from which this note can be reconstructed
    """
    def getValue(self):
        return self.base + self.alteration + self.octave * 12

    """
        extracts tone from current note
    """
    def getTone(self):
        return Tone(self.getValue())

    """
        Mixcraft notation used: midikey(C0) == 0
    """
    @classmethod
    def midiKeyFromStr(cls, string):
        pos = string.rindex('-') if '-' in string else -1
        tone, octave = string[:pos], int(string[pos:])
        return Tone(tone).getValue() + (octave) * 12

    """
        returns Tone combined with octave shift index
    """
    def __repr__(self):
        return Tone.__repr__(self) + str(self.octave)


class Interval(object):
    """
        Base interval class
    """

    def __init__(self, value:int):
        self.value = value

    def clone(self):
        return Interval(self.value)

    def collapse(self):
        self.value %= 12

    @classmethod
    def fromPair(cls, note1:Note, note2:Note):
        return Interval(note2.getValue() - note1.getValue())

    def __repr__(self):
        return str(self.value)


class Scale(object):
    """
        Base class for harmonic structure of particular part of the song
    """

    def __init__(self, base:Tone, intervals:list):
        self.base = base
        self.intervals = intervals

    def clone(self):
        intvs = list(map(Interval.clone, self.intervals))
        return Scale(self.base.clone(), intvs)

    def containsTone(self, tone:Tone):
        intvs = map(lambda i: i.value, self.intervals)
        interval = Interval.fromPair(self.base, tone)
        interval.collapse()
        return interval.value in intvs

    """ I II III IV V VI VII """
    @classmethod
    def maj(cls, base:Tone):
        intervals = [0, 2, 4, 5, 7, 9, 11]
        intervals = list(map(Interval, intervals))
        return Scale(base, intervals)

    """ I II IIIb IV V VIb VIIb """
    @classmethod
    def min(cls, base:Tone):
        intervals = [0, 2, 3, 5, 7, 8, 10]
        intervals = list(map(Interval, intervals))
        return Scale(base, intervals)

    """ I II III IV# V VI VII """
    @classmethod
    def lyd(cls, base:Tone):
        intervals = [0, 2, 4, 6, 7, 9, 11]
        intervals = list(map(Interval, intervals))
        return Scale(base, intervals)

    """ I II III IV V VI VIIb """
    @classmethod
    def mics(cls, base:Tone):
        intervals = [0, 2, 4, 5, 7, 9, 10]
        intervals = list(map(Interval, intervals))
        return Scale(base, intervals)

    """ I IIb IIIb IV V VIb VIIb """
    @classmethod
    def frig(cls, base:Tone):
        intervals = [0, 1, 3, 5, 7, 8, 10]
        intervals = list(map(Interval, intervals))
        return Scale(base, intervals)

    """ I II IIIb IV V VI(#) VIIb    (#) == becar """
    @classmethod
    def dor(cls, base:Tone):
        intervals = [0, 2, 3, 5, 7, 9, 10]
        intervals = list(map(Interval, intervals))
        return Scale(base, intervals)

    @classmethod
    def penta(cls, base:Tone):
        intervals = [0, 3, 6, 9]
        intervals = list(map(Interval, intervals))
        return Scale(base, intervals)

    def __repr__(self):
        return ','.join(map(str, self.intervals))