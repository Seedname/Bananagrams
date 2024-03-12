import sys
sys.path.insert(1, '../bananagrams')
import bananagrams.decrypt as decrypt
import get_features
import os
import tomli
import math
import random
import time

def generate_random_key(alphabet: str) -> str:
    return ''.join(random.sample(alphabet, len(alphabet)))

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

    return [word for word in list(message) if word]

def get_features_from_words(words: list[str], graphs: int) -> dict:
    feature_dict = {}
    
    for word in words:
        for i in range(len(word)):
            if i + graphs > len(word):
                break

            substr = word[i:i+graphs]

            if feature_dict.get(substr):
                feature_dict[substr] += 1
            else:
                feature_dict[substr] = 1
    
    return feature_dict

def get_fitness(key: str, fitness_values: list[dict], default_fitness: list[float], feature_counts: list[int], message: list[str], alphabet: str) -> float:
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

def evolve_key(key: str, fitness_values: list[dict], default_fitness: list[float], feature_counts: list[int], message: list[str], alphabet: str, max_iterations:int = 10**2) -> str:
    start_time = time.time()
    for num in range(max_iterations):
        if num % 10 == 0 and num > 0:
            elapsed_time = time.time() - start_time
            remaining_time = (elapsed_time / num) * (max_iterations - num)
            print(f"Evolving Key {num}/{max_iterations} ---- Time remaining: {remaining_time/60:.2f} minutes")

        base_fitness = get_fitness(key, fitness_values, default_fitness, feature_counts, message, alphabet)

        child_keys = []
        for i in range(len(key)):
            for j in range(i+1, len(key)):
                child_keys.append(swap_chars(key, i, j))

        fitnesses = [get_fitness(key, fitness_values, default_fitness, feature_counts, message, alphabet) for key in child_keys]
        max_fitness = max(fitnesses)

        if max_fitness > base_fitness:
            key = child_keys[fitnesses.index(max_fitness)]
        else:
            return key
        
    return key

def main() -> None:
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    feature_counts = [2, 3, 4]

    if not os.path.exists("fitness_analysis/features.toml"):
        get_features.main(feature_counts)
    
    with open('fitness_analysis/features.toml', 'rb') as f:
        features: dict = tomli.load(f)["features"]
    
    features: list[dict] = [features[str(feature_count)] for feature_count in feature_counts]
    default_fitness: list[float] = [math.log(min(feature.values())) + 7 for feature in features]
    fitness_values: list[dict] = [{key: math.log(value) + 8 for key, value in feature.items()} for feature in features]

    message = read_message('bananagrams/message.txt', ALPHABET)
    base_key = generate_random_key(ALPHABET)

    print("Evolving key...")
    final_key = evolve_key(base_key, fitness_values, default_fitness, feature_counts, message, ALPHABET)
    print(final_key)
    decrypt.decrypt(final_key, 'bananagrams/message.txt', 'fitness_analysis/correct.txt', ALPHABET)

if __name__ == "__main__":
    main()