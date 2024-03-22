import tomli
import matplotlib.pyplot as plt
from regression import inverse_regression
from scipy.optimize import curve_fit
import math

def inverse(x, Beta_1, Beta_2):
    return Beta_1 / x ** Beta_2

from os import environ

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

if __name__ == "__main__":
    suppress_qt_warnings()
    
    print("Reading features...")
    with open('../frequency_analysis/features.toml', 'rb') as f:
        features: list[dict] = tomli.load(f)["features"]

    for feature in features:
        feature_type, values = list(feature.items())[0]
        words = []
        frequencies = []
        for word, frequency in values.items():
            words.append(word)
            frequencies.append(frequency)
        x_values = range(1, len(words)+1)

        try:
            popt, pcov = curve_fit(inverse, x_values, frequencies)
            b = popt[1]
        except:
            b = 1

        regression = inverse_regression(x_values, frequencies, b)
        print(regression)
        print(f"nth root: {1/b}")

        a = regression["a"]
        # c = regression["b"]
        c = 0
        func = lambda x: a/x**b + c

        plt.plot(x_values, [func(x) for x in x_values])
        plt.plot(x_values, frequencies)

        plt.title(f"Sorted frequencies of {feature_type}")
        # plt.xticks(visible=False)
        plt.xlabel(feature_type)
        plt.ylabel("Frequency")
        plt.show()
