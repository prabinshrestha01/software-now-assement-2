from main import decrypt_text  # improt decrypt function

# Read encrypted text
with open("encrypted_text.txt", "r", encoding="utf-8") as f:
    encrypted = f.read()

# Read shifts
with open("shifts.txt", "r", encoding="utf-8") as f:
    shifts = list(map(int, f.read().split()))

# Decrypt using imported function
decrypted = decrypt_text(encrypted, shifts)

# Save decrypted text
with open("decrypted_text.txt", "w", encoding="utf-8") as f:
    f.write(decrypted)

print("Decryption done ✔")