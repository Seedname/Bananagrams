import random

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

def generate_random_key():
    return ''.join(random.sample(ALPHABET, len(ALPHABET)))

class Generation:
    def __init__(self):
        pass

