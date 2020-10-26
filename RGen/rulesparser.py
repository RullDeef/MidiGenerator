import music21


def roman_to_int(s):
    roman = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500,
             'M': 1000, 'IV': 4, 'IX': 9, 'XL': 40, 'XC': 90, 'CD': 400, 'CM': 900}
    i, num = 0, 0
    while i < len(s):
        if i + 1 < len(s) and s[i:i+2] in roman:
            num += roman[s[i:i+2]]
            i += 2
        else:
            num += roman[s[i]]
            i += 1
    return num


def extract_roman(s):
    l = 1
    num = -1
    while l <= len(s):
        try:
            num = roman_to_int(s[0:l])
            l += 1
        except:
            break
    return num, s[l-1:]


def is_roman(s):
    l = 1
    num = -1
    while l <= len(s):
        try:
            num = roman_to_int(s[0:l])
            l += 1
        except:
            break
    return num != -1


def is_int(s):
    try:
        int(s)
        return True
    except:
        return False


def print_notes(stream):
    stream = stream.flat.sorted
    for q in range(int(stream.duration.quarterLength)):
        row = ""
        for f in range(21, 109):
            for note in stream.notes:
                if note.offset <= q and q < note.offset + note.duration.quarterLength and note.pitch.ps == f:
                    row = row + "█"
                    break
            else:
                row = row + " "
        print(row)


def parse_note(token, key):
    tone, add = extract_roman(token)
    note = music21.note.Note()
    note.pitch.ps = music21.note.Note(" CDEFGAB"[tone]).pitch.ps
    try:
        while add[0] == "<":
            note.pitch.ps -= 12
            add = add[1:]
        while add[0] == ">":
            note.pitch.ps += 12
            add = add[1:]
        note.pitch.ps += int(add)
    except:
        pass
    note.pitch.ps += key
    note.duration.quarterLength = 0.5
    return note


def parse_tokens(tokens):
    prime_pitch = music21.note.Note("C4").pitch.ps
    note_stream = music21.stream.Stream()

    keys_stack = [0]

    for token in tokens:
        if token == "T^":  # key pop
            keys_stack = keys_stack[1:]
        # key push
        elif token[0] == "T" and (is_int(token[1:]) or len(token) > 2 and is_int(token[2:])):
            new_key = 0
            token = token[1:]
            if token[0] == "*":
                new_key += keys_stack[0]
                token = token[1:]
            new_key += int(token)
            keys_stack = [new_key] + keys_stack
        elif is_roman(token):  # starts with roman number
            note = parse_note(token, keys_stack[0])
            note_stream.append(note)

    return note_stream


def generate_tokens(rules, generations, max_tokens):
    tokens = [""]
    generation = 0

    while max_tokens == 0 and generation < generations or len(tokens) < max_tokens:
        new_tokens = []
        for token in tokens:
            new_tokens.extend(rules.get(token, token).split())
        tokens = new_tokens
        generation += 1

    return tokens


def apply_rules(rules, *, generations=1, max_tokens=None):
    tokens = generate_tokens(rules, generations, max_tokens)
    return parse_tokens(tokens)
