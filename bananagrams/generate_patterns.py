import pathlib

def get_pattern(word: str, alphabet: str) -> str:
    mapping = {}
    for letter in word:
        if not mapping.get(letter):
            mapping[letter] = alphabet[len(mapping)]

    pattern = ""
    for letter in word:
        pattern += mapping[letter]

    return pattern


if __name__ == "__main__":
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    parent_dir = pathlib.Path(__file__).parent

    with open(parent_dir.parent / "bananagrams" / "no_pattern.txt", 'r') as f:
        lines = [line.strip().lower() for line in f.readlines()]

    with open(parent_dir.parent / "bananagrams" / "dictionary.txt", 'w') as f:
        for word in lines:
            f.write(f'{get_pattern(word, alphabet)} {word}\n')