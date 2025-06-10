def caesar_decrypt(text, shift):
    decrypted = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')
            decrypted += chr((ord(char) - base - shift) % 26 + base)
        else:
            decrypted += char
    return decrypted

# Encrypted message
encrypted = ("QrydSulphFrruglqdwhv:Vhfwru-7Doskd &$&_*_!QrydSulphFrruglqdwhv:Vhfwru-7Doskd&$&_*_!QrydSulphFrruglqdwhv:Vhfwru-7-Doskd&$&_*_!QrydSulphFrruglqdwhv:Vhfwru-7-Doskd&$&_*_!QrydSulphFrruglqdwhv:Vhfwru-7Doskd&$&_*_!QrydSulphFrruglqdwhv:Vhfwru-7-Doskd")
encrypted_shortened = "QrydSulphFrruglqdwhv:Vhfwru-7Doskd &$&_*_!"

# Decrypt with Caesar cipher using shift one by one to check the possible message
for i in range(1, 25, 1):
    decrypted = caesar_decrypt(encrypted_shortened, i)
    print("Message ", i, ": ",decrypted)

print()
#found the actual key and define the full message
print("key = 3")
decrypted = caesar_decrypt(encrypted, 3)
print()
print("Full Message : ",decrypted)