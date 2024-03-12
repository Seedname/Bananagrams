dictionary = {}
ALPHABET = "abcdefghijklmnopqrstuvwxyz"

with open('bananagrams/dictionary.txt', 'r') as f:
    for pair in f.readlines():
        pattern, word = pair.strip().split(" ")
        if not dictionary.get(pattern):
            dictionary[pattern] = []
        dictionary[pattern].append(word)

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

print(dictionary[get_pattern("mammoth".lower())])