ALPHABET = "abcdefghijklmnopqrstuvwxyz"

from bananagrams.decrypt import invert_key
import pathlib

def decrypt(key):
    new_message = ""

    parent_dir = pathlib.Path(__file__).parent

    correct = open(parent_dir.parent / 'bananagrams' / 'correct.txt', 'w')
    with open(parent_dir.parent / 'encrypt' / 'message.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            for letter in line:
                if letter.lower() in ALPHABET:
                    if letter.lower() == letter:
                        new_message += key[ALPHABET.index(letter.lower())]
                    else:
                        new_message += key[ALPHABET.index(letter.lower())].upper()
                else:
                    new_message += letter
    correct.write(new_message)

key = 'presntdayimouhlfwkcvgbjqxz'
# key = invert_key(key, alphabet=ALPHABET)
decrypt(key)