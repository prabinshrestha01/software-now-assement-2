from main import decrypt_text  # improt decrypt function

# Reading encrypted text
with open("encrypted_text.txt", "r", encoding="utf-8") as f:
    encrypted = f.read()

# Reading shifts
with open("shifts.txt", "r", encoding="utf-8") as f:
    shift = list(map(int, f.read().split()))

# descrypt with imported  function
decrypted = decrypt_text(encrypted, shifts)

# save text from decrypted
with open("decrypted_text.txt", "w", encoding="utf-8") as f:
    f.write(decrypted)

print("description done ✔")