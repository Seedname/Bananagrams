import tomli_w

def filter_text(lines: list[str], dictionary: dict, alphabet: str) -> list[str]:
    output = []

    def get_mapping(word):
        mapping = {}
        for letter in word:
            if not mapping.get(letter):
                mapping[letter] = alphabet[len(mapping)]
        return mapping

    def get_pattern(word):
        mapping = get_mapping(word)
        pattern = ""
        for letter in word:
            pattern += mapping[letter]
        return pattern

    def isalpha(str: str):
        for letter in str.lower():
            if letter not in alphabet:
                return False
        return True
    
    for line in lines:
        for word in line.strip().split(" "):
            pattern = get_pattern(word)
            # if not dictionary.get(pattern) or word not in dictionary[pattern]:
                # continue
            output.append((''.join(filter(isalpha, word))).lower().strip())

    return output

prefixes = ["mono", "di", "tri", "quad", "penta", "hexa", "septa", "octa", "nona", "deca"]

def main(feature_range) -> None:
    dictionary = {}
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"

    print("Creating Dictionary...")
    with open('frequency_analysis/dictionary.txt', 'r') as f:
        for pair in f.readlines():
            pattern, word = pair.strip().split(" ")
            if not dictionary.get(pattern):
                dictionary[pattern] = []
            dictionary[pattern].append(word)

    features = {}
    print("Formatting text...")
    with open('frequency_analysis/text.txt') as f:
        lines = f.readlines()
        text = filter_text(lines, dictionary, ALPHABET)

    print("Obtaining Features..")
    for count in feature_range:
        search_type = f"{count} contiguous letters"
        if count <= len(prefixes):
            search_type = f"{prefixes[count-1]}graphs"

        print(f"Looking for {search_type}")

        feature_dict = {}
        
        for word in text:
            for i in range(len(word)):
                if i + count > len(word):
                    break

                substr = word[i:i+count]

                if feature_dict.get(substr):
                    feature_dict[substr] += 1
                else:
                    feature_dict[substr] = 1

        if len(feature_dict) == 0:
            continue

        feature_dict = dict(sorted(feature_dict.items(), key=lambda x:x[1], reverse=True))
        total = sum(feature_dict.values())
        feature_dict = {key: value/total for key, value in feature_dict.items()}
        features[search_type] = feature_dict

    with open("fitness_analysis/features.toml", 'wb') as f:
        tomli_w.dump({"features": features}, f)

if __name__ == "__main__":
    main(range(1, 10 +1))