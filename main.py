# Double-shift encryption 

def encrypt_text(text, shift1, shift2):
    """
    
    Encrypts the given text using the double-shift rules.
    Returns the encrypted text and a list of shifts applied for each character.
    """
    encrypted = ""
    shifts = []
    for c in text:
        if c.islower():
            s = shift1*shift2 if 'a' <= c <= 'm' else -(shift1+shift2)
        elif c.isupper():
            s = -shift1 if 'A' <= c <= 'M' else shift2**2
        else:
            s = 0
        encrypted += chr((ord(c) + s) % 256)
        shifts.append(s)
    return encrypted, shifts

def decrypt_text(encrypted, shifts):
    decrypted = ""
    for c, s in zip(encrypted, shifts):
        decrypted += chr((ord(c) - s) % 256)
    return decrypted

def main():
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    # Read original file
    with open("raw_text.txt", "r", encoding="utf-8") as f:
        raw = f.read()

    # Encrypt
    encrypted, shifts = encrypt_text(raw, shift1, shift2)
    with open("encrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(encrypted)
    print("Encryption done ✔")

    # Decrypt
    decrypted = decrypt_text(encrypted, shifts)
    with open("decrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(decrypted)
    print("Decryption done ✔")

    # Verify
    print("Decryption successful ✔" if raw == decrypted else "Decryption failed ✖")

if __name__ == "__main__":
    main()

