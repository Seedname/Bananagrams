f = open('study-guide.txt', 'r')
lines = f.readlines()
f.close()

f = open('dictionary.txt', 'r')
lists = f.readlines()
f.close()

def allBananagrams(word):
    length = len(word)
    bananagrams = []

    for dict in lists:
        currentWord = dict.strip()
        if len(currentWord) is not length: continue
        
        key = ""
        mapped = ""

        canMap = True
        for i in range(length):
            if word[i] not in mapped:
                if currentWord[i] in key:
                    canMap = False
                    break

                key += currentWord[i]
                mapped += word[i]

        if not canMap: continue
        newString = ""
        for i in range(length):
            newString += key[mapped.index(word[i])]
        
        if newString == currentWord:
            bananagrams.append(currentWord)

    return bananagrams


key = [""] * 26
alphabet = "abcdefghijklmnopqrstuvwxyz"


for word in lines:
    word = word.strip()
    if (len(word) > 20):
        bananagrams = allBananagrams(word)
        for bananagram in bananagrams:
            for i in range(len(word)):
                index = alphabet.index(word[i])
                key[index] = bananagram[i]

key = "".join(key)
print(key)

        
