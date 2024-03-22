import sys
import random
import tomli
import math

sys.path.insert(1, '../fitness_analysis')
sys.path.insert(1, '../bananagrams')

import fitness_analysis.decrypt as fitness
import bananagrams.decrypt as bananagrams

def evolve_keyspace(keyspace: dict, alphabet: str, features: list[dict], feature_counts: list[int], message: list[str]) -> str:
    keyspace: list[str] = bananagrams.generate_keystrings(keyspace, alphabet)
    if len(keyspace) > 20:
        keyspace = random.sample(keyspace, 20)

    print(f"Evolving {len(keyspace)} keys...")

    result = {}
    for i in range(len(keyspace)):
        print(f"{i+1}/{len(keyspace)}")
        key = keyspace[i]
        evolved_key, score = fitness.evolve_key(key, features, feature_counts, message, alphabet)
        result[evolved_key] = score

    return max(result.items(), key=lambda x: x[1])[0]

def main() -> None:
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    dictionary = bananagrams.create_dictionary('../bananagrams/dictionary.txt')
    message = bananagrams.read_message('../bananagrams/message.txt', alphabet)

    with open('../fitness_analysis/features.toml', 'rb') as f:
        features: dict = tomli.load(f)["features"]

    feature_counts = [2, 3, 4]
    features: list[dict] = [features[str(feature_count)] for feature_count in feature_counts]
    possible_keys = {letter: set([l for l in alphabet]) for letter in alphabet}
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
            bananagrams.decrypt(decrypting_key, '../bananagrams/message.txt', '../bananafitness/correct.txt', alphabet)
            break
    else:
        print(f"Generating Keystrings from {keyspace_size:,} possible keys...")
        decrypting_key = evolve_keyspace(possible_keys, alphabet, features, feature_counts, message)
        encrypting_key = bananagrams.invert_key(decrypting_key, alphabet)
        print(f'{decrypting_key = }')
        print(f'{encrypting_key = }')
        bananagrams.decrypt(decrypting_key, '../bananagrams/message.txt', '../bananafitness/correct.txt', alphabet)

if __name__ == "__main__":
    main()