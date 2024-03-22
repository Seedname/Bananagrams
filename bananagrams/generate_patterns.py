ALPHABET = "abcdefghijklmnopqrstuvwxyz"
f = open('../bananagrams/no_pattern.txt', 'r')
lines = [line.strip().lower() for line in f.readlines()]
f.close()

def get_pattern(word):
    mapping = {}
    for letter in word:
        if not mapping.get(letter):
            mapping[letter] = ALPHABET[len(mapping)]

    pattern = ""
    for letter in word:
        pattern += mapping[letter]

    return pattern

with open('../bananagrams/dictionary.txt', 'w') as f:
    for word in lines:
        f.write(f'{get_pattern(word)} {word}\n')