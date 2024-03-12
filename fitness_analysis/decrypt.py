import sys
sys.path.insert(1, '../bananagrams')
import get_features
import os
import tomli
import math

def main() -> None:
    if not os.path.exists("fitness_analysis/features.toml"):
        get_features.main([2, 3, 4])
    
    with open('fitness_analysis/features.toml', 'rb') as f:
        features: list[dict] = tomli.load(f)["features"]

    features = [list(feature.values())[0] for feature in features]
    for feature in features:
        for value in feature:
            feature[value] = math.log(feature[value]) 
    print(features)
    
if __name__ == "__main__":
    main()