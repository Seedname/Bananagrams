import tomli_w

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

def filter_text(lines: list[str]) -> list[str]:
    output = []

    def isalpha(str: str):
        for letter in str.lower():
            if letter not in ALPHABET:
                return False
        return True
    
    for line in lines:
        for word in line.strip().split(" "):
            output.append((''.join(filter(isalpha, word))).lower().strip())

    return output

prefixes = ["mono", "di", "tri", "quad", "penta", "hexa", "sexa", "septa", "octa", "nona", "deca"]

if __name__ == "__main__":
    features = []
    feature_range = [2, 3]
    
    print("Formatting text...")
    with open('frequency_analysis/text.txt') as f:
        lines = f.readlines()
        text = filter_text(lines)

    print("Obtaining Features..")
    for count in feature_range:
        if count < len(prefixes):
            print(f"Looking for {prefixes[count-1]}graphs")
        else:
            print(f"Looking for {count} contiguous letters")

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
        
        feature_dict = dict(sorted(feature_dict.items(), key=lambda x:x[1], reverse=True))
        features.append(feature_dict)

    with open('frequency_analysis/features.toml', 'wb') as f:
        tomli_w.dump({"features": features}, f)