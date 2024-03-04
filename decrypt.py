dictionary = {}
ALPHABET = "abcdefghijklmnopqrstuvwxyz"

with open('dictionary.txt', 'r') as f:
    for pair in f.readlines():
        pattern, word = pair.strip().split(" ")
        if not dictionary.get(pattern):
            dictionary[pattern] = []
        dictionary[pattern].append(word)

message = []
with open('message.txt', 'r') as f:    
    for line in f.readlines():
        for word in line.strip().split(" "):
            message.append((''.join(filter(str.isalpha, word))).lower().rstrip())
message = [word for word in list(set(message)) if word]

def get_mapping(word):
    mapping = {}
    for letter in word:
        if not mapping.get(letter):
            mapping[letter] = ALPHABET[len(mapping)]
    return mapping

def get_pattern(word):
    mapping = get_mapping(word)
    pattern = ""
    for letter in word:
        pattern += mapping[letter]
    return pattern

def all_mappings(word):
    pattern = get_pattern(word)
    if not dictionary.get(pattern): return False
    bananagrams = dictionary[pattern]
    total_mapping = {letter: [] for letter in list(set(word))}
    for other_word in bananagrams:
        mapping = {value: key for key, value in get_mapping(other_word).items()}
        for i in range(len(word)):
            total_mapping[word[i]].append(mapping[pattern[i]])
    total_mapping = {letter: list(set(mappings)) for letter, mappings in total_mapping.items()}
    return total_mapping

def cull_extras(possible_keys):
    confirmed = ""
    for mapping in possible_keys:
        if len(possible_keys[mapping]) == 1:
            confirmed += possible_keys[mapping][0]

    for mapping in possible_keys:
        if len(possible_keys[mapping]) > 1:
            new_mapping = []
            for letter in possible_keys[mapping]:
                if letter not in confirmed:
                    new_mapping.append(letter)
            possible_keys[mapping] = new_mapping

    return possible_keys

def count_all_keys(possible_keys):
    prod = 1
    for key in possible_keys:
        prod *= len(possible_keys[key])
    return prod

def decrypt(key):
    new_message = ""
    correct = open('correct.txt', 'w')
    with open('message.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            for letter in line:
                if letter.lower() in ALPHABET:
                    if letter.lower() == letter:
                        new_message += key[ALPHABET.index(letter.lower())]
                    else:
                        new_message += key[ALPHABET.index(letter.lower())].upper()
                else:
                    new_message += letter
    correct.write(new_message)

def generate_keystrings(keyspace):
    keystrings = ['']
    for i in range(len(ALPHABET)):
        next_keystrings = []
        for current_key in keystrings:
            next_letter = ALPHABET[i]
            possible_values = keyspace[next_letter]
            for letter in possible_values:
                if letter not in current_key:
                    next_keystrings.append(current_key + letter)
        keystrings = next_keystrings
    return keystrings

def decrypt_word(word, key):
    new_word = ""
    for letter in word:
        new_word += key[ALPHABET.index(letter)]
    return new_word

def brute_force(keyspace, message):
    keyspace = generate_keystrings(keyspace)
    for i in range(len(keyspace)):
        key = keyspace[i]
        for word in message:
            pattern = get_pattern(word)
            if not dictionary.get(pattern): continue
            decrypted_word = decrypt_word(word, key)
            if decrypted_word not in dictionary[pattern]:
                break
        else:
            return key
        print(f'{i+1:,}/{len(keyspace):,} keys tested')


possible_keys = {letter: [l for l in ALPHABET] for letter in ALPHABET}
for word in message:
    word_mappings = all_mappings(word)
    if not word_mappings: continue
    for letter in word_mappings:
        possible_keys[letter] = list(set(possible_keys[letter]) & set(word_mappings[letter]))
    possible_keys = cull_extras(possible_keys)
    keyspace_size = count_all_keys(possible_keys)
    print(f'{keyspace_size:,} possible keys (with overlaps)')

    if keyspace_size == 1:
        key = ''.join([possible_keys[mapping][0] for mapping in possible_keys])
        print(f'{key = }')
        decrypt(key)
        break
else:
    key = brute_force(possible_keys, message)
    print(f'{key = }')
    decrypt(key)
    pass