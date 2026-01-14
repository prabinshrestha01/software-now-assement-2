from main import decrypt_text

encrypted = input("Enter encrypted text: ")

shifts = list(map(int, input("Enter shifts separated by space: ").split()))

decrypted = decrypt_text(encrypted, shifts)
print("Decrypted text:", decrypted)