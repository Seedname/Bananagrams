f = open('frequencies.txt', 'r')
freqs = f.readlines()
f.close()

alphabet = ""
frequencies = []
for line in freqs:
    a = line.split(" ")
    alphabet += a[0].lower()
    frequencies.append(float(a[1]))

# import math
# frequencies = [0.08167,0.01492,0.02782,0.04253,0.12702,0.02288,0.02015,0.06094,0.06966,0.00153,0.00772,0.04025,0.02406,0.06749,0.07507,0.01929,0.00095,0.05987,0.06327,0.09056,0.02758,0.00978,0.0236,0.0015,0.01974,0.00074]
# alphabet = "abcdefghijklmnopqrstuvwxyz"

f = open('substitution.txt', 'r')
lines = f.readlines()
f.close()

occurences = [0] * 26
total = 0
for line in lines:
    line = line.strip()
    for letter in line:
        try:
            index = alphabet.index(letter)
            occurences[index] += 1
            total += 1
        except:
            continue

for i in range(len(occurences)):
    occurences[i] = 100 * occurences[i] / total

key = [''] * 26
errors = []
for i in range(len(occurences)):
    percentage = occurences[i]
    found = False
    cantUse = [-1] * 26

    while not found:
        minError = 100
        minIndex = -1

        for j in range(len(frequencies)):
            error = abs(frequencies[j] - percentage)
        
            if cantUse[j] == -1 and error < minError:
                minError = error
                minIndex = j

        if key[minIndex] == '': 
            key[minIndex] = alphabet[i]
            found = True
            errors.append(minError)
        else: 
            cantUse[minIndex] = 0

# print(errors)
print(''.join(key))


# key = "hunapymzkwqervxjobtlgdcisf"
# output = ""
# for line in lines:
#     line = line.strip()
#     for letter in line:
#         try:
#             output += key[alphabet.index(letter.lower())]
#         except:
#             output += letter
#     output += "\n"

# print(output)