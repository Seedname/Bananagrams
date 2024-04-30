import random
import sys
sys.path.insert(1, '../bananagrams')
import bananagrams.decrypt as bananagrams

def generate_random_key(alphabet: str) -> str:
    return ''.join(random.sample(alphabet, len(alphabet)))


def encrypt(key: str, message_path: str, output_path: str, alphabet: str) -> None:
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


if __name__ == "__main__":
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    encrypting_key = generate_random_key(alphabet)
    decrypting_key = bananagrams.invert_key(encrypting_key, alphabet)
    print(f'{encrypting_key = }')
    print(f'{decrypting_key = }')
    encrypt(encrypting_key, 'plaintext.txt', 'message.txt', alphabet)
