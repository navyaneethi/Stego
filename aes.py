from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def encrypt_text(key, plaintext):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return ciphertext, cipher.iv

def decrypt_text(key, iv, ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

# Example usage
key = b'thisisasecretkey'
text = 'You are beautiful'

ciphertext, iv = encrypt_text(key, text)
print("Encrypted Text (hexadecimal):", ciphertext.hex())
print("IV (hexadecimal):", iv.hex())

decrypted_text = decrypt_text(key, iv, ciphertext)
decrypted_text = decrypted_text[:-ord(decrypted_text[-1:])].decode('utf-8')
print("Decrypted Text:", decrypted_text)
