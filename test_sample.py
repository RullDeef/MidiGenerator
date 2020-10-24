from migen import Tone, Note

def test_ToneClass():
    assert repr(Tone('F')) == repr(Tone(5)) == 'F'
    assert Tone.valueFromStr('F') == 5
    assert Tone('F').getValue() == 5
    assert Tone.fromMidiKey(9 + 70 * 12).getValue() == 9

def test_NoteClass():
    for s in ('A0', 'C1', 'D1', 'E1'):
        assert repr(Note(s)) == s
    assert Note('A0').getValue() == 9