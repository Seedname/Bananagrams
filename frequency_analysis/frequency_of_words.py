import sys
from get_features import filter_text
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math
from regression import inverse_regression

def inverse(x, Beta_1, Beta_2):
    return Beta_1 / x ** Beta_2
    
def main() -> None:
    dictionary = {}
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"

    print("Creating Dictionary...")
    with open('../frequency_analysis/dictionary.txt', 'r') as f:
        for pair in f.readlines():
            pattern, word = pair.strip().split(" ")
            if not dictionary.get(pattern):
                dictionary[pattern] = []
            dictionary[pattern].append(word)

    print("Formatting text...")
    with open('../frequency_analysis/text.txt') as f:
        lines = f.readlines()
        message = filter_text(lines, dictionary, ALPHABET)

    words = {}
    for word in message:
        if not words.get(word):
            words[word] = 1
        else:
            words[word] += 1

    words = dict(sorted(words.items(), key=lambda x:x[1], reverse=True))
    most_words_displayed = len(words)
    x_values = range(1, most_words_displayed+1)
    y_values = [word/len(words) for word in list(words.values())[:most_words_displayed]]

    popt, pcov = curve_fit(inverse, x_values, y_values)
    b = popt[1]
    regression = inverse_regression(x_values, y_values, b)
    print(regression)
    print(f"nth root: {1/b}")
    
    a = regression["a"]
    # c = regression["b"]
    c = 0
    func = lambda x: a/x**b + c

    plt.plot(x_values, [func(x) for x in x_values])
    plt.plot(x_values, y_values)
    # plt.xticks(visible=False)
    plt.show()

 

if __name__ == "__main__":
    main()