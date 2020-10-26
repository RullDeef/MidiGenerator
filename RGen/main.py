import music21
from rulesparser import apply_rules, print_notes

rules = {
    "": "T-12 :song",
    ":song": ":begin :mid :end",

    ":begin": ":bp1 :bp2 T*3 :bp1 T^",

    ":bp1": "I I V I> I> V V+1 IV :bp1",
    ":bp2": "V< II V VII I> III-1 IV II"
}

#print(tokens)
note_stream = apply_rules(rules, generations=7)
print_notes(note_stream)

note_stream.write("midi", fp="out2.midi")
