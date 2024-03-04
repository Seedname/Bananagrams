ALPHABET = "abcdefghijklmnopqrstuvwxyz"
def decrypt(key):
    new_message = ""
    correct = open('correct.txt', 'w')
    with open('message.txt', 'r') as f:
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
    
key = 'rajsbktcludmvenwfoxgpyhqzi'
decrypt(key)