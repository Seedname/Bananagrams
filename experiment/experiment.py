import time
import sys
import math
import tomli
import tomli_w
import matplotlib.pyplot as plt
import random

sys.path.insert(1, '../fitness_analysis')
sys.path.insert(1, '../bananagrams')

import fitness_analysis.decrypt as fitness
import bananagrams.decrypt as bananagrams


def normalized_hamming_distance(test_key: str, real_key: str) -> float:
    num_correct = 0
    for i in range(len(test_key)):
        if test_key[i] == real_key[i]:
            num_correct += 1
    return num_correct / len(test_key)


def fitness_analysis_runner():
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    message = fitness.read_message('../encrypt/message.txt', alphabet)

    with open('../fitness_analysis/features.toml', 'rb') as f:
        features: dict = tomli.load(f)["features"]

    feature_counts = [2, 3, 4]
    features: list[dict] = [features[str(feature_count)] for feature_count in feature_counts]

    base_key = fitness.generate_random_key(alphabet)
    real_key = "sprgwhkjoqzldcuvyemnbtiafx"

    start_length = 20
    end_length = 200

    runtimes = {str(i): 0 for i in range(start_length, end_length + 1, 10)}
    accuracies = {str(i): 0 for i in range(start_length, end_length + 1, 10)}
    times = 100

    start_time = time.time()
    for curr_num in range(1, times + 1):
        for num_words in range(start_length, end_length + 1, 10):
            print(num_words)
            sub_message = random.sample(message, num_words)
            start_time = time.time()
            key, _ = fitness.evolve_key(base_key, features, feature_counts, sub_message, alphabet)
            end_time = time.time()
            runtime = end_time - start_time
            accuracy = normalized_hamming_distance(key, real_key)

            runtimes[str(num_words)] += runtime
            accuracies[str(num_words)] += accuracy

        elapsed_time = time.time() - start_time
        remaining_time = (elapsed_time / curr_num) * (times - curr_num)
        print(f"Experiment {curr_num}/{times} ---- Time remaining: {remaining_time / 60:.2f} minutes")

    runtimes = {key: value / times for key, value in runtimes.items()}
    accuracies = {key: value / times for key, value in accuracies.items()}

    with open('fitness_analysis.toml', 'wb') as f:
        tomli_w.dump({"n": times,
                      "runtimes": runtimes,
                      "accuracies": accuracies}, f)

    runtime_x = list(map(int, runtimes.keys()))
    runtime_y = list(runtimes.values())

    plt.plot(runtime_x, runtime_y, "-b", label="Runtime")

    plt.xlabel("Number of Words")
    plt.ylabel("Runtime (sec)")
    plt.title("Runtime vs. Number of Words")

    plt.savefig("runtime_graph.png")
    plt.show()

    accuracy_x = list(map(int, accuracies.keys()))
    accuracy_y = list(accuracies.values())

    plt.plot(accuracy_x, accuracy_y, "-r", label="Accuracy")

    plt.xlabel("Number of Words")
    plt.ylabel("Accuracy")
    plt.title("Accuracy vs. Number of Words")

    plt.savefig("accuracy_graph.png")
    plt.show()


def bananagrams_runner():
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    message = fitness.read_message('../encrypt/message.txt', alphabet)
    dictionary = bananagrams.create_dictionary('../bananagrams/dictionary.txt')
    threshold = 1

    real_key = "sprgwhkjoqzldcuvyemnbtiafx"

    start_length = 20
    end_length = 200

    runtimes = {str(i): 0 for i in range(start_length, end_length + 1, 10)}
    accuracies = {str(i): 0 for i in range(start_length, end_length + 1, 10)}
    times = 100

    total_time = time.time()
    for curr_num in range(1, times + 1):
        for num_words in range(start_length, end_length + 1, 10):
            print(num_words)

            sub_message = random.sample(message, num_words)
            possible_keys = {letter: {char for char in alphabet} for letter in alphabet}

            start_time = time.time()

            for word in sub_message:
                word_mappings = bananagrams.all_mappings(word, dictionary, alphabet)
                if not word_mappings: continue
                for letter in word_mappings:
                    possible_keys[letter] = possible_keys[letter] & word_mappings[letter]

                possible_keys = bananagrams.cull_extras(possible_keys)
                keyspace_size = bananagrams.count_all_keys(possible_keys)

                if keyspace_size == 1:
                    key = ''.join([list(possible_keys[mapping])[0] for mapping in possible_keys])
                    break
            else:
                key = bananagrams.brute_force(possible_keys, message, dictionary, alphabet, threshold)

            end_time = time.time()
            runtime = end_time - start_time
            accuracy = normalized_hamming_distance(key, real_key)

            runtimes[str(num_words)] += runtime
            accuracies[str(num_words)] += accuracy

        elapsed_time = time.time() - total_time
        remaining_time = (elapsed_time / curr_num) * (times - curr_num)
        print(f"Experiment {curr_num}/{times} ---- Time remaining: {remaining_time / 60:.2f} minutes")

    runtimes = {key: value / times for key, value in runtimes.items()}
    accuracies = {key: value / times for key, value in accuracies.items()}

    with open('bananagrams.toml', 'wb') as f:
        tomli_w.dump({"n": times,
                      "runtimes": runtimes,
                      "accuracies": accuracies}, f)

    runtime_x = list(map(int, runtimes.keys()))
    runtime_y = list(runtimes.values())

    plt.plot(runtime_x, runtime_y, "-b", label="Runtime")

    plt.xlabel("Number of Words")
    plt.ylabel("Runtime (sec)")
    plt.title("Runtime vs. Number of Words")

    plt.savefig("runtime_graph_bananagrams.png")
    plt.show()

    accuracy_x = list(map(int, accuracies.keys()))
    accuracy_y = list(accuracies.values())

    plt.plot(accuracy_x, accuracy_y, "-r", label="Accuracy")

    plt.xlabel("Number of Words")
    plt.ylabel("Accuracy (%)")
    plt.title("Accuracy vs. Number of Words")

    plt.savefig("accuracy_graph_bananagrams.png")
    plt.show()


if __name__ == "__main__":
    # fitness_analysis_runner()
    bananagrams_runner()
