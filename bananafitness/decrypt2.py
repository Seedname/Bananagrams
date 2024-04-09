import sys
import random
import tomli
import math

sys.path.insert(1, '../fitness_analysis')
sys.path.insert(1, '../bananagrams')

import fitness_analysis.decrypt as fitness
import bananagrams.decrypt as bananagrams


def generate_key_from_keyspace(keyspace: dict, alphabet: str) -> str:
    remaining_letters = [*alphabet]
    key = ""
    for letter in keyspace:
        for current_letter in keyspace[letter]:
            if current_letter in random.sample(remaining_letters, len(remaining_letters)):
                key += current_letter
                remaining_letters.remove(current_letter)
                break
        else:
            current_letter = random.choice(remaining_letters)
            key += current_letter
            remaining_letters.remove(current_letter)
    return key


def evolve_keyspace(keyspace: dict, alphabet: str, single_letter_features: dict, current_features: list[dict],
                    feature_counts: list[int], message: list[str], keyspace_size: int = 20) -> str:

    keyspace = [generate_key_from_keyspace(keyspace, alphabet) for _ in range(keyspace_size)]
    results = {}
    for key in keyspace:
        evolved_key, score = fitness.evolve_key(single_letter_features, current_features, feature_counts, message,
                                                alphabet, key=key, passes=15)
        results[evolved_key] = score

    return max(results.items(), key=lambda x: x[1])[0]

def main() -> None:
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    dictionary = bananagrams.create_dictionary('../bananagrams/dictionary.txt')
    message = bananagrams.read_message('../encrypt/message.txt', alphabet)

    with open('../fitness_analysis/features.toml', 'rb') as f:
        features: dict = tomli.load(f)["features"]

    feature_counts = [2, 3, 4]
    current_features: list[dict] = [features[str(feature_count)] for feature_count in feature_counts]
    possible_keys = {letter: set(alphabet) for letter in alphabet}
    print("Narrowing Keyspace...")

    for word in message:
        word_mappings = bananagrams.all_mappings(word, dictionary, alphabet)
        if not word_mappings: continue
        for letter in word_mappings:
            possible_keys[letter] = possible_keys[letter] & word_mappings[letter]

        possible_keys = bananagrams.cull_extras(possible_keys)
        keyspace_size = bananagrams.count_all_keys(possible_keys)

        if keyspace_size == 1:
            decrypting_key = ''.join([list(possible_keys[mapping])[0] for mapping in possible_keys])
            encrypting_key = bananagrams.invert_key(decrypting_key, alphabet)
            print("Absolute key found!")
            print(f'{decrypting_key = }')
            print(f'{encrypting_key = }')
            bananagrams.decrypt(decrypting_key, '../encrypt/message.txt', '../bananafitness/correct.txt', alphabet)
            break
    else:
        print(f"Generating Keystrings from {keyspace_size:,} possible keys...")
        decrypting_key = evolve_keyspace(possible_keys, alphabet, features["1"], current_features, feature_counts,
                                         message)
        encrypting_key = bananagrams.invert_key(decrypting_key, alphabet)
        print(f'{decrypting_key = }')
        print(f'{encrypting_key = }')
        bananagrams.decrypt(decrypting_key, '../encrypt/message.txt', '../bananafitness/correct.txt', alphabet)


if __name__ == "__main__":
    main()
