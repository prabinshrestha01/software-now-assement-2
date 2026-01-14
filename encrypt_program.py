from main import encrypt_text

text = input("Enter text to encrypt: ")
shift1 = int(input("Enter shift1: "))
shift2 = int(input("Enter shift2: "))

encrypted, shifts = encrypt_text(text, shift1, shift2)
print("Encrypted text:", encrypted)
print("Shifts:", shifts)



