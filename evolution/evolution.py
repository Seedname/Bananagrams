from __future__ import annotations
import random
import sys
sys.path.insert(1, '../bananagrams')
import bananagrams.decrypt as decrypt
import time

def generate_random_key(alphabet: str) -> str:
    return ''.join(random.sample(alphabet, len(alphabet)))

def fitness(key: str, dictionary: dict, message: list[str], alphabet: str) -> int:
    valid_words = 0
    for word in message:
        word = decrypt.decrypt_word(word, key, alphabet)
        pattern = decrypt.get_pattern(word, alphabet)
        if not dictionary.get(pattern):
            continue
        if word not in dictionary[decrypt.get_pattern(word, alphabet)]:
            continue
        valid_words += 1
    return valid_words

class Evolution:
    def __init__(self, pop_size:int) -> None:
        self.ALPHABET = "abcdefghijklmnopqrstuvwxyz"
        self.dictionary = decrypt.create_dictionary('../bananagrams/dictionary.txt')
        self.message = decrypt.read_message('../bananagrams/message.txt', self.ALPHABET)

        self.pop_size = pop_size
        self.population = [generate_random_key(self.ALPHABET) for _ in range(pop_size)]
        self.mutation_rate = 3

    def get_fitnesses(self) -> list[tuple[str,int]]:
        return [(key, fitness(key, self.dictionary, self.message, self.ALPHABET)) for key in self.population]
    
    def mutate(self, key: str) -> str:
        length = len(key)
        key = [*key]
        for _ in range(self.mutation_rate):
            first_index = random.randrange(0, length)
            second_index = random.randrange(0, length)

            while first_index == second_index:
                second_index = random.randrange(0, length)
            
            first_item = key[first_index]
            key[first_index] = key[second_index]
            key[second_index] = first_item

        return ''.join(key)
        # uhh maybe figure out how to add crossover as well
    
    def filter(self, survivors: float = 0.5) -> None:
        self.population = [key for key, _ in list(sorted(self.get_fitnesses(), key=lambda x:x[1], reverse=True))]
        survivors = self.population[:int(self.pop_size * survivors)]
        self.population = survivors.copy()
        current_index = 0
        while len(self.population) < self.pop_size:
            self.population.append(self.mutate(survivors[current_index]))
            current_index += 1
            current_index %= len(survivors)
        # print(len(self.population))

def main() -> None:
    start_time = time.time()
    genetic_solver = Evolution(pop_size=10)
    for i in range(1000):
        # print(f"Evolving Generation {i+1}/1000")
        if i % 10 == 0 and i > 0:
            elapsed_time = time.time() - start_time
            remaining_time = (elapsed_time / i) * (1000 - i)
            print(f"Evolving Generation {i}/1000 ---- Time remaining: {remaining_time:.2f} seconds")
        genetic_solver.filter(0.2)
    print(max(genetic_solver.get_fitnesses(), key=lambda x: x[1]))


if __name__ == "__main__":
    main()