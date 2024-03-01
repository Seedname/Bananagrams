f = open('message.txt', 'r')
lines = f.readlines()
all_words = []
for line in lines:
    for word in line.rstrip().split(" "):
        all_words.append((''.join(filter(str.isalpha, word))).lower().rstrip())
# print(list(set(all_words)))

f.close()

f = open('dictionary.txt', 'r')
lists = f.readlines()
dictionary = {}
for word in lists:
    word = word.strip()
    if not dictionary.get(len(word)):
        dictionary[len(word)] = []
    dictionary[len(word)].append(word)
f.close()

alphabet = "abcdefghijklmnopqrstuvwxyz"

def allBananagrams(word):
    length = len(word)
    bananagrams = []
    keys = []
    for currentWord in dictionary[length]:
        key = ""
        mapped = ""

        canMap = True
        for i in range(length):
            if word[i] not in mapped:
                if currentWord[i] in key:
                    canMap = False
                    break

                key += currentWord[i]
                mapped += word[i]

        if not canMap: continue
        newString = ""
        for i in range(length):
            newString += key[mapped.index(word[i])]
        
        if newString == currentWord:
            bananagrams.append(currentWord)
            current_key = ["?"] * 26
            for i in range(len(mapped)):
                index = alphabet.index(key[i])
                current_key[index] = mapped[i]
            keys.append(''.join(current_key))
    return bananagrams, keys

# key = [""] * 26

keyspace = []

def merge_keys(current_key, test_key):
    new_key = ''
    for i in range(len(current_key)):
        if current_key[i] != test_key[i] and current_key[i] != "?" and test_key[i] != "?":
            return False
        
        if current_key[i] != "?":
            if current_key[i] in new_key:
                return False
            new_key += current_key[i]
        elif test_key[i] != "?":
            if test_key[i] in new_key:
                return False
            new_key += test_key[i]
        else:
            new_key += '?'

    return new_key

def update_keys(keyspace, keys):
    new_keyspace = []
    for i in range(len(keyspace)):
        test_key = keyspace[i]
        valid_key = ""
        for current_key in keys:   
            valid_key = merge_keys(current_key, test_key)
            if valid_key:
                break
        if not valid_key: continue
        num_unknown = valid_key.count("?")
        if len(list(set([*valid_key]))) + num_unknown - 1 != 26:
            continue
        new_keyspace.append(valid_key)

    return new_keyspace

def guess_last(key):
    new_alphabet = [*alphabet]
    for i in range(len(key)):
        if key[i] != "?":
            del new_alphabet[new_alphabet.index(key[i])]
    return key.replace("?", new_alphabet[0])
    
def find_key():
    
    _, keyspace = allBananagrams(all_words[0])

    for i in range(1, len(all_words)):
        word = all_words[i]
        bananagrams, keys = allBananagrams(word)
        prev_keyspace = keyspace.copy()
        keyspace = update_keys(keyspace, keys)

        if len(keyspace) == 0:
            keyspace = prev_keyspace

        print(len(keyspace))
        if len(keyspace) == 1 and keyspace[0].count("?") <= 1:
            break
    
    if len(keyspace) == 1 and keyspace[0].count("?") <= 1:
        return guess_last(keyspace[0])
    
    print(keyspace)
    return False

def decrypt(key):
    new_message = ""
    g = open('correct.txt', 'w')
    with open('message.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            for letter in line:
                if letter in alphabet:
                    new_message += alphabet[key.index(letter)]
                else:
                    new_message += letter

    g.write(new_message)
    g.close()

key = find_key()
if key:
    print(key)
    decrypt(key)
