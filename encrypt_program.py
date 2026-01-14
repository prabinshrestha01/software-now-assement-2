from main import encrypt_text  # import the encrypt_text function

# Ask user for shift values
shift1 = int(input("Enter shift1: "))
shift2 = int(input("Enter shift2: "))

# Read original text
with open("raw_text.txt", "r", encoding="utf-8") as f:
    raw = f.read()

# Encrypt using imported function
encrypted, shifts = encrypt_text(raw, shift1, shift2)

# Save encrypted text
with open("encrypted_text.txt", "w", encoding="utf-8") as f:
    f.write(encrypted)

# Save shifts for decryption
with open("shifts.txt", "w", encoding="utf-8") as f:
    f.write(" ".join(map(str, shifts)))

print("Encryption done ✔")


