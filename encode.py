from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from PIL import Image

def aes_cbc_encrypt(data, key):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    return iv + encrypted_data


def bytes_to_binary(byte_data):
    return ''.join(format(byte, '08b') for byte in byte_data)


def hide_data(image_path, data):

    key = get_random_bytes(16)  # AES-128
    print("key :" , key)
    encrypted_data = aes_cbc_encrypt(data.encode("utf-8"), key)
    print(encrypted_data)
   
    binary_data = bytes_to_binary(encrypted_data)
    binary_data += '1111111111111110'  # Adding a delimiter
    print(binary_data)  # Outputs the binary representation of the byte data

    # Open the image and convert it to RGB
    image = Image.open(image_path).convert("RGB")
    pixels = image.load()
    width, height = image.size

    # Check if the image can hold the text
    if len(binary_data) > width * height * 3:
        raise ValueError("Text too long to encode in the image")
    
    data_index = 0

    # Iterate through each pixel and modify the LSB
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))

            # Encode the text into the least significant bit of each color component
            if data_index < len(binary_data):
                r = r & ~1 | int(binary_data[data_index])
                data_index += 1
            if data_index < len(binary_data):
                g = g & ~1 | int(binary_data[data_index])
                data_index += 1
            if data_index < len(binary_data):
                b = b & ~1 | int(binary_data[data_index])
                data_index += 1

            pixels[x, y] = (r, g, b)

    # Save the new image
    image.save("stego_image.png")

# Usage
hide_data("input.png", "Your data goes here. You can type anything you want!")
print("Text encoded successfully")
