import music21
from rulesparser import apply_rules, print_notes

rules = {
    "": "T-12 :pyro",
    ":pyro": "I T*5 :inner T^ I",
    ":inner": "I V I T*2 :pyro :inner :pyro T^ I IV I"
}

# generations = 10
tokens_count = 200

#print(tokens)
note_stream = apply_rules(rules, max_tokens=tokens_count)
print_notes(note_stream)

#note_stream.write("midi", fp="out.midi")
