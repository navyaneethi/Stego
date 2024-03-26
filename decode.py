from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from PIL import Image

def aes_cbc_decrypt(encrypted_data, key):
    encrypted_data = encrypted_data
    iv = encrypted_data[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data[16:]), AES.block_size)
    return decrypted_data.decode("utf-8")

def binary_to_bytes(binary_data):
    # Convert each 8-bit binary string to an integer
    integer_list = [int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8)]
    # Create a bytes object from the list of integers
    byte_data = bytes(integer_list)
    return byte_data


def decode_text(image_path,key):
    """Decode hidden text from image."""
    img = Image.open(image_path)
    width, height = img.size

    binary_data = ""
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            binary_data += bin(r)[-1] + bin(g)[-1] + bin(b)[-1]

    # Find the position of the delimiter
    delimiter_pos = binary_data.find('1111111111111110')
    if delimiter_pos == -1:
        raise ValueError("Delimiter not found. No hidden message detected.")

    # Extract the binary text
    binary_data = binary_data[:delimiter_pos]

    # Convert binary text to ASCII characters
    byte_data = binary_to_bytes(binary_data)
    print("Encrypted data:", byte_data)
    decoded_text = aes_cbc_decrypt(byte_data, key)
    return decoded_text

# Example usage:
# Decode the hidden message 
key = b'\x82\n\xf9B\x0e(\xd3\xc5\xaa}N\xe6\r\x0f\xd3G'
decoded_message = decode_text("stego_image.png",key)
print("Decoded message:", decoded_message)