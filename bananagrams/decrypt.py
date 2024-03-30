import time


def create_dictionary(file_path: str) -> dict:
    dictionary = {}
    print(f"Creating Dictionary from {file_path}...")
    with open(file_path, 'r') as f:
        for pair in f.readlines():
            pattern, word = pair.strip().split(" ")
            if not dictionary.get(pattern):
                dictionary[pattern] = []
            dictionary[pattern].append(word)
    return dictionary


def read_message(file_path: str, alphabet: str) -> list[str]:
    message = []
    print(f"Reading message from {file_path}...")

    def isalpha(str: str) -> bool:
        for letter in str.lower():
            if letter not in alphabet:
                return False
        return True

    with open(file_path, 'r') as f:
        for line in f.readlines():
            for word in line.strip().split(" "):
                message.append((''.join(filter(isalpha, word))).lower().rstrip())
    return [word for word in list(set(message)) if word]


def get_mapping(word: str, alphabet: str) -> dict:
    mapping = {}
    for letter in word:
        if not mapping.get(letter):
            mapping[letter] = alphabet[len(mapping)]
    return mapping


def get_pattern(word: str, alphabet: str) -> str:
    mapping = get_mapping(word, alphabet)
    pattern = ""
    for letter in word:
        pattern += mapping[letter]
    return pattern


def all_mappings(word: str, dictionary: dict, alphabet: str) -> dict:
    pattern = get_pattern(word, alphabet)
    if not dictionary.get(pattern): return False
    bananagrams = dictionary[pattern]
    total_mapping = {letter: [] for letter in list(set(word))}
    for other_word in bananagrams:
        mapping = {value: key for key, value in get_mapping(other_word, alphabet).items()}
        for i in range(len(word)):
            total_mapping[word[i]].append(mapping[pattern[i]])
    total_mapping = {letter: set(mappings) for letter, mappings in total_mapping.items()}
    return total_mapping


def cull_extras(possible_keys: dict) -> dict:
    confirmed = set()
    for mapping, letters in possible_keys.items():
        if len(letters) == 1:
            confirmed.update(letters)

    for mapping, letters in possible_keys.items():
        if len(letters) > 1:
            possible_keys[mapping] -= confirmed

    return possible_keys


def count_all_keys(possible_keys: dict) -> int:
    prod = 1
    for key in possible_keys:
        prod *= len(possible_keys[key])
    return prod


def decrypt(key: str, message_path: str, output_path: str, alphabet: str) -> None:
    new_message = ""
    print(f"Writing translated message to {output_path}...")
    correct = open(output_path, 'w')
    with open(message_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            for letter in line:
                if letter.lower() in alphabet:
                    if letter.lower() == letter:
                        new_message += key[alphabet.index(letter.lower())]
                    else:
                        new_message += key[alphabet.index(letter.lower())].upper()
                else:
                    new_message += letter
    correct.write(new_message)


def decrypt_word(word: str, key: str, alphabet: str) -> str:
    new_word = ""
    for letter in word:
        new_word += key[alphabet.index(letter)]
    return new_word


def generate_keystrings(keyspace: dict, alphabet: str) -> list[str]:
    keystrings = ['']
    for next_letter in alphabet:
        next_keystrings = []
        for current_key in keystrings:
            possible_values = keyspace[next_letter]
            for letter in possible_values:
                if letter not in current_key:
                    next_keystrings.append(current_key + letter)
        keystrings = next_keystrings
    return keystrings


def brute_force(keyspace: dict, message: list[str], dictionary: dict, alphabet: str, threshold: float = 1) -> str:
    keyspace = generate_keystrings(keyspace, alphabet)
    start_time = time.time()
    for i in range(len(keyspace)):
        if i % 10000 == 0:
            if i > 0:
                elapsed_time = time.time() - start_time
                remaining_time = (elapsed_time / i) * (len(keyspace) - i)
                if remaining_time > 60:
                    print(
                        f"Brute Forcing Keyspace -- {i:,}/{len(keyspace):,} ({100 * (i) / len(keyspace):.2f}%) -- {remaining_time / 60:.2f} minutes remaining")
                else:
                    print(
                        f"Brute Forcing Keyspace -- {i:,}/{len(keyspace):,} ({100 * (i) / len(keyspace):.2f}%) -- {remaining_time:.2f} seconds remaining")
            else:
                print(
                    f"Brute Forcing Keyspace of {len(keyspace):,} key{'s'[:len(keyspace) ^ 1]} with {threshold * 100:.2f}% threshold...")
        key = keyspace[i]

        if threshold == 1:
            for word in message:
                pattern = get_pattern(word, alphabet)
                if not dictionary.get(pattern): continue
                decrypted_word = decrypt_word(word, key, alphabet)
                if decrypted_word not in dictionary[pattern]:
                    break
            else:
                print(f"Valid key found after {i + 1:,} search{'es'[:(i + 1) ^ 1]}!")
                return key
        else:
            valid_words = 0

            for word in message:
                pattern = get_pattern(word)
                if not dictionary.get(pattern): continue
                decrypted_word = decrypt_word(word, key)
                if decrypted_word not in dictionary[pattern]: continue
                valid_words += 1

            if valid_words / len(message) >= threshold:
                print(f"Valid key found after {i + 1:,} search{'es'[:(i + 1) ^ 1]}!")
                return key


def invert_key(reciprocal_key: str, alphabet: str) -> str:
    original_key = ['' for _ in range(len(alphabet))]
    for i in range(len(reciprocal_key)):
        letter = reciprocal_key[i]
        original_key[alphabet.index(letter)] = alphabet[i]
    return ''.join(original_key)


def main() -> None:
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    THRESHOLD = 1

    dictionary = create_dictionary('../bananagrams/dictionary.txt')
    message = read_message('../encrypt/message.txt', ALPHABET)

    possible_keys = {letter: set([l for l in ALPHABET]) for letter in ALPHABET}
    print("Narrowing Keyspace...")

    for word in message:
        word_mappings = all_mappings(word, dictionary, ALPHABET)
        if not word_mappings: continue
        for letter in word_mappings:
            possible_keys[letter] = possible_keys[letter] & word_mappings[letter]

        possible_keys = cull_extras(possible_keys)
        keyspace_size = count_all_keys(possible_keys)

        if keyspace_size == 1:
            decrypting_key = ''.join([list(possible_keys[mapping])[0] for mapping in possible_keys])
            encrypting_key = invert_key(decrypting_key, ALPHABET)
            print("Absolute key found!")
            print(f'{decrypting_key = }')
            print(f'{encrypting_key = }')
            decrypt(decrypting_key, '../encrypt/message.txt', '../bananagrams/correct.txt', ALPHABET)
            break
    else:
        # possible_keys = cull_extras(possible_keys)
        print(f"Generating Keystrings from {keyspace_size:,} possible keys...")
        decrypting_key = brute_force(possible_keys, message, dictionary, ALPHABET, THRESHOLD)
        if decrypting_key:
            encrypting_key = invert_key(decrypting_key, ALPHABET)
            print(f'{decrypting_key = }')
            print(f'{encrypting_key = }')
            decrypt(decrypting_key, '../encrypt/message.txt', '../bananagrams/correct.txt', ALPHABET)
        else:
            print("No key found ):")
            print("There is likely at least one word in your message that is not part of the dictionary.")


if __name__ == "__main__":
    main()
