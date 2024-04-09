import random
import math
import decrypt
import tomli
import os
import sys

sys.path.insert(1, '../bananagrams')
import bananagrams.decrypt as bananagrams


def accept(temperature: float, old_energy: float, new_energy: float) -> bool:
    delta_energy = new_energy - old_energy

    if new_energy >= old_energy:
        return True

    print(-delta_energy / temperature)
    if random.random() < math.exp(-delta_energy / temperature):
        return True

    return False


def calculate_score(value: float) -> float:
    return value / 1000


def optimize(single_letter_features: dict, features: list[dict], feature_counts: list[int], message: list[str],
             alphabet: str) -> str:
    default_fitness: list[float] = [calculate_score(min(feature.values())) / 10 for feature in features]
    fitness_values: list[dict] = [{key: calculate_score(value) for key, value in feature.items()} for feature in
                                  features]
    key = decrypt.generate_base_key(message, single_letter_features, alphabet)
    temperature = 1
    min_temp = 0.1
    cooling_rate = 0.9999

    energy = decrypt.get_fitness(key, fitness_values, default_fitness, feature_counts, message, alphabet)

    while temperature > min_temp:
        i = random.randrange(0, len(key))
        j = random.randrange(0, len(key))
        while i == j: j = random.randrange(0, len(key))
        next_key = decrypt.swap_chars(key, i, j)
        new_energy = calculate_score(decrypt.get_fitness(next_key, fitness_values, default_fitness, feature_counts, message, alphabet))
        if accept(temperature, energy, new_energy):
            key = next_key
            energy = new_energy
        temperature *= cooling_rate
        print(f'Temperature: {temperature}, Energy: {energy}')
    print(energy)
    return key


def main() -> None:
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    feature_counts = [2, 3, 4]

    if not os.path.exists("../fitness_analysis/features.toml"):
        decrypt.get_features.main([1] + feature_counts)

    with open('../fitness_analysis/features.toml', 'rb') as f:
        features: dict = tomli.load(f)["features"]

    current_features: list[dict] = [features[str(feature_count)] for feature_count in feature_counts]

    message: list[str] = decrypt.read_message('../encrypt/message.txt', alphabet)

    if len(message) > 100:
        message = random.sample(message, 100)

    decrypting_key = optimize(features["1"], current_features, feature_counts, message, alphabet)
    encrypting_key = bananagrams.invert_key(decrypting_key, alphabet)
    print(f'{decrypting_key = }')
    print(f'{encrypting_key = }')
    bananagrams.decrypt(decrypting_key, '../encrypt/message.txt', '../fitness_analysis/correct.txt', alphabet)


if __name__ == "__main__":
    main()
