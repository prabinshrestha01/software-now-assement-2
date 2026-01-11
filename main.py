import string

def encrypt_text(shift1, shift2):
    with open("raw_text.txt", "r") as f:
        text = f.read()

    encrypted = ""

    for char in text:
        if char.islower():
            if char in "abcdefghijklm":
                shift = shift1 * shift2
                alphabet = string.ascii_lowercase
                new_char = alphabet[(alphabet.index(char) + shift) % 26]
            else:
                shift = shift1 + shift2
                alphabet = string.ascii_lowercase
                new_char = alphabet[(alphabet.index(char) - shift) % 26]
            encrypted += new_char

        elif char.isupper():
            if char in "ABCDEFGHIJKLM":
                shift = shift1
                alphabet = string.ascii_uppercase
                new_char = alphabet[(alphabet.index(char) - shift) % 26]
            else:
                shift = shift2 ** 2
                alphabet = string.ascii_uppercase
                new_char = alphabet[(alphabet.index(char) + shift) % 26]
            encrypted += new_char

        else:
            encrypted += char

    with open("encrypted_text.txt", "w") as f:
        f.write(encrypted)

def decrypt_text(shift1, shift2):
    with open("encrypted_text.txt", "r") as f:
        text = f.read()

    decrypted = ""

    for char in text:
        if char.islower():
            if char in "abcdefghijklm":
                shift = shift1 * shift2
                alphabet = string.ascii_lowercase
                new_char = alphabet[(alphabet.index(char) - shift) % 26]
            else:
                shift = shift1 + shift2
                alphabet = string.ascii_lowercase
                new_char = alphabet[(alphabet.index(char) + shift) % 26]
            decrypted += new_char

        elif char.isupper():
            if char in "ABCDEFGHIJKLM":
                shift = shift1
                alphabet = string.ascii_uppercase
                new_char = alphabet[(alphabet.index(char) + shift) % 26]
            else:
                shift = shift2 ** 2
                alphabet = string.ascii_uppercase
                new_char = alphabet[(alphabet.index(char) - shift) % 26]
            decrypted += new_char

        else:
            decrypted += char

    with open("decrypted_text.txt", "w") as f:
        f.write(decrypted)

def verify_decryption():
    with open("raw_text.txt", "r") as f1, open("decrypted_text.txt", "r") as f2:
        if f1.read() == f2.read():
            print("Decryption successful: files match ✔️")
        else:
            print("Decryption failed: files do NOT match ❌")

# -------- MAIN PROGRAM --------
shift1 = int(input("Enter shift1: "))
shift2 = int(input("Enter shift2: "))

encrypt_text(shift1, shift2)
decrypt_text(shift1, shift2)
verify_decryption()
