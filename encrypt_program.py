from main import encrypt_text  # import the encrypt_text function

# user to enter value
shift1 = int(input("Enter shift1: "))
shift2 = int(input("Enter shift2: "))

# Reading original text
with open("raw_text.txt", "r", encoding="utf-8") as f:
    raw = f.read()

# Encrypt with imported function
encrypted, shifts = encrypt_text(raw, shift1, shift2)

# saving encrypted text
with open("encrypted_text.txt", "w", encoding="utf-8") as f:
    f.write(encrypted)

# saving shifts for decryption
with open("shifts.txt", "w", encoding="utf-8") as f:
    f.write(" ".join(map(str, shifts)))

print("encryption done ✔")


