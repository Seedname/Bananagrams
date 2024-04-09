import get_features
import tomli_w


def main() -> None:
    dictionary = {}
    print("Creating Dictionary...")
    with open('../frequency_analysis/dictionary.txt', 'r') as f:
        for pair in f.readlines():
            pattern, word = pair.strip().split(" ")
            if not dictionary.get(pattern):
                dictionary[pattern] = []
            dictionary[pattern].append(word)

    feature_counts = [1, 2, 3, 4]

    feature_mappings = {}
    for pattern in dictionary:
        words = dictionary[pattern]

        for count in feature_counts:
            current_features: list[str] = list(get_features.get_feature([pattern], count).keys())
            for feature in current_features:
                if feature not in feature_mappings:
                    feature_mappings[feature] = [*words]
                    continue
                feature_mappings[feature].extend(words)

    with open('feature_mappings', 'wb') as f:
        tomli_w.dump(feature_mappings, f)


if __name__ == "__main__":
    main()
