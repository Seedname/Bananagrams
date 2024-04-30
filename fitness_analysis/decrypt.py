import sys
import get_features
import os
import tomli
import math
import random

sys.path.insert(1, '../bananagrams')
import bananagrams.decrypt as decrypt


def generate_random_key(alphabet: str) -> str:
    return ''.join(random.sample(alphabet, len(alphabet)))


def read_message(file_path: str, alphabet: str) -> list[str]:
    message: list[str] = []
    print(f"Reading message from {file_path}...")

    def isalpha(char: str) -> bool:
        for letter in char.lower():
            if letter not in alphabet:
                return False
        return True

    with open(file_path, 'r') as f:
        for line in f.readlines():
            for word in line.strip().split(" "):
                message.append((''.join(filter(isalpha, word))).lower().rstrip())

    return [word for word in list(message) if word]


def get_features_from_words(words: list[str], graphs: int) -> dict:
    feature_dict = {}

    for word in words:
        for i in range(len(word)):
            if i + graphs > len(word):
                break

            substr = word[i:i + graphs]

            if feature_dict.get(substr):
                feature_dict[substr] += 1
            else:
                feature_dict[substr] = 1

    return feature_dict


def get_fitness(key: str, fitness_values: list[dict], default_fitness: list[float],
                feature_counts: list[int], message: list[str], alphabet: str) -> float:
    words = [decrypt.decrypt_word(word, key, alphabet) for word in message]

    fitness: float = 0.0

    for i in range(len(feature_counts)):
        feature_count = feature_counts[i]

        features = get_features_from_words(words, feature_count)
        for feature in features:
            if feature in fitness_values[i]:
                fitness += features[feature] * fitness_values[i][feature]
            else:
                fitness += features[feature] * default_fitness[i]

    return fitness


def swap_chars(key: str, i: int, j: int) -> str:
    key = [*key]
    key[i], key[j] = key[j], key[i]
    return ''.join(key)


def generate_base_key(message: list[str], single_letter_features: dict, alphabet: str) -> str:
    current_features = list(sorted(get_features.get_feature(message, 1).items(), reverse=True, key=lambda x: x[1]))
    key = ["" for _ in range(len(alphabet))]
    current_letters = [*alphabet]
    single_letters = list(single_letter_features.keys())

    for i in range(len(single_letter_features)):
        if i < len(current_letters):
            letter = current_features[i][0]
            index = alphabet.index(letter)
            key[index] = single_letters[i]
            current_letters.remove(letter)
        else:
            index = alphabet.index(current_letters[0])
            key[index] = single_letters[i]
            current_letters.pop(0)

    return ''.join(key)


def determine_key(original_message: list[str], final_message: list[str], alphabet: str):
    mapping = {char: "" for char in alphabet}
    current_letters = [*alphabet]

    for i in range(len(original_message)):
        for j in range(len(original_message[i])):
            original_letter = original_message[i][j]
            final_letter = final_message[i][j]

            if not mapping[original_letter]:
                current_letters.remove(final_letter)
                mapping[original_letter] = final_letter

    non_mapped = [letter for letter in mapping if not mapping[letter]]
    for i in range(len(non_mapped)):
        mapping[non_mapped[i]] = current_letters[i]

    return ''.join(mapping.values())


def optimal_child(key: str, fitness_values: list[dict], default_fitness: list[float],
                  feature_counts: list[int], message: list[str], alphabet: str) -> tuple[str, float]:
    child_keys = []
    for i in range(len(key)):
        for j in range(i + 1, len(key)):
            child_keys.append(swap_chars(key, i, j))

    fitnesses = [get_fitness(key, fitness_values, default_fitness, feature_counts, message, alphabet) for key in
                 child_keys]
    max_fitness = max(fitnesses)

    return child_keys[fitnesses.index(max_fitness)], max_fitness


def evolve_generation(key: str, fitness_values: list[dict], default_fitness: list[float],
                      feature_counts: list[int], message: list[str], alphabet: str):
    while True:
        base_fitness = get_fitness(key, fitness_values, default_fitness, feature_counts, message, alphabet)

        child_key, max_fitness = optimal_child(key, fitness_values, default_fitness, feature_counts,
                                               message, alphabet)
        if max_fitness > base_fitness:
            key = child_key
            continue

        return key, max_fitness


def evolve_key(single_letter_features: dict, features: list[dict], feature_counts: list[int],
               message: list[str], alphabet: str, passes: int = 15, key: str = None) -> tuple[str, float]:
    default_fitness: list[float] = [math.log(min(feature.values())) / 10 for feature in features]
    fitness_values: list[dict] = [{key: math.log(value) for key, value in feature.items()}
                                  for feature in features]
    original_message = message.copy()

    if not key:
        key = generate_base_key(message, single_letter_features, alphabet)

    fitness = 0

    for num in range(passes):
        key, fitness = evolve_generation(key, fitness_values, default_fitness, feature_counts, message, alphabet)
        message = [decrypt.decrypt_word(word, key, alphabet) for word in message]
        print(f"Finished pass {num + 1}/{passes}")

    return determine_key(original_message, message, alphabet), fitness


def main() -> None:
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    feature_counts = [2, 3, 4]

    if not os.path.exists("../fitness_analysis/features.toml"):
        get_features.main([1] + feature_counts)

    with open('../fitness_analysis/features.toml', 'rb') as f:
        features: dict = tomli.load(f)["features"]

    current_features: list[dict] = [features[str(feature_count)] for feature_count in feature_counts]

    message: list[str] = read_message('../encrypt/message.txt', alphabet)

    if len(message) > 100:
        message = random.sample(message, 100)

    print("Evolving key...")
    decrypting_key, _ = evolve_key(features["1"], current_features, feature_counts, message, alphabet)
    encrypting_key = decrypt.invert_key(decrypting_key, alphabet)

    print(f'{decrypting_key = }')
    print(f'{encrypting_key = }')

    decrypt.decrypt(decrypting_key, '../encrypt/message.txt', '../fitness_analysis/correct.txt', alphabet)


if __name__ == "__main__":
    main()
