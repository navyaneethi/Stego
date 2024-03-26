from PIL import Image

def binary_to_text(binary_str):
    """Convert binary string to text."""
    text = ""
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        text += chr(int(byte, 2))
    return text.rstrip("\x00")

def decode_text(image_path):
    """Decode hidden text from image."""
    img = Image.open(image_path)
    width, height = img.size

    binary_text = ""
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            binary_text += bin(r)[-1] + bin(g)[-1] + bin(b)[-1]

    # Find the position of the delimiter
    delimiter_pos = binary_text.find('1111111111111110')
    if delimiter_pos == -1:
        raise ValueError("Delimiter not found. No hidden message detected.")

    # Extract the binary text
    binary_text = binary_text[:delimiter_pos]

    # Convert binary text to ASCII characters
    decoded_text = binary_to_text(binary_text)

    return decoded_text

# Example usage:
# Decode the hidden message from the image "output_image.png"
decoded_message = decode_text("output_image.png")
print("Decoded message:", decoded_message)
