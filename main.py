import string


def shift_char(c, shift, is_upper):
    alphabet = string.ascii_uppercase if is_upper else string.ascii_lowercase
    idx = alphabet.index(c)
    new_idx = (idx + shift) % 26
    return alphabet[new_idx]


def encrypt_text(shift1, shift2):
    # Open and read original text file
    with open("raw_text.txt", "r", encoding="utf-8") as f:
        text = f.read()

    encrypted = ""

    # Loop through each character in the text
    for ch in text:

        # If lowercase letter
        if ch.islower():
            # a–m → shift forward by shift1*shift2
            if 'a' <= ch <= 'm':
                shift = shift1 * shift2
                encrypted += shift_char(ch, shift, is_upper=False)

            # n–z → shift backward by shift1+shift2
            elif 'n' <= ch <= 'z':
                shift = -(shift1 + shift2)
                encrypted += shift_char(ch, shift, is_upper=False)

            else:
                encrypted += ch

        # If uppercase letter
        elif ch.isupper():
            # A–M → shift backward by shift1
            if 'A' <= ch <= 'M':
                shift = -shift1
                encrypted += shift_char(ch, shift, is_upper=True)

            # N–Z → shift forward by shift2 squared
            elif 'N' <= ch <= 'Z':
                shift = shift2 ** 2
                encrypted += shift_char(ch, shift, is_upper=True)

            else:
                encrypted += ch

        # Non-alphabet characters stay unchanged
        else:
            encrypted += ch

    # Write encrypted text to file
    with open("encrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(encrypted)


def decrypt_text(shift1, shift2):
    # Read encrypted text file
    with open("encrypted_text.txt", "r", encoding="utf-8") as f:
        text = f.read()

    decrypted = ""

    # Loop through encrypted characters
    for ch in text:

        # If lowercase letter
        if ch.islower():
            # Reverse of a–m rule
            if 'a' <= ch <= 'm':
                shift = -(shift1 * shift2)
                decrypted += shift_char(ch, shift, is_upper=False)

            # Reverse of n–z rule
            elif 'n' <= ch <= 'z':
                shift = (shift1 + shift2)
                decrypted += shift_char(ch, shift, is_upper=False)

            else:
                decrypted += ch

        # If uppercase letter
        elif ch.isupper():
            # Reverse of A–M rule
            if 'A' <= ch <= 'M':
                shift = shift1
                decrypted += shift_char(ch, shift, is_upper=True)

            # Reverse of N–Z rule
            elif 'N' <= ch <= 'Z':
                shift = -(shift2 ** 2)
                decrypted += shift_char(ch, shift, is_upper=True)

            else:
                decrypted += ch

        # Non-alphabet characters stay unchanged
        else:
            decrypted += ch

    # Write decrypted text to file
    with open("decrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(decrypted)


def verify():
    with open("raw_text.txt", "r", encoding="utf-8") as f1, open("decrypted_text.txt", "r", encoding="utf-8") as f2:
        return f1.read() == f2.read()


# Main program
if __name__ == "__main__":
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    encrypt_text(shift1, shift2)
    decrypt_text(shift1, shift2)

    if verify():
        print("Decryption successful ✔")
    else:
        print("Decryption failed ✖")
 