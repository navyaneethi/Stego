from PIL import Image

def text_to_binary(text):
    """Convert text to binary."""
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary

def encode_text(image_path, output_image_path, text):
    """Encode text into image."""
    # Open the image
    img = Image.open(image_path)
    width, height = img.size

    # Convert text to binary
    binary_text = text_to_binary(text)
    binary_text += '1111111111111110'  # Adding a delimiter

    # Check if the image can hold the text
    if len(binary_text) > width * height * 3:
        raise ValueError("Text too long to encode in the image")

    data_index = 0
    encoded_pixels = img.load()

    # Iterate through each pixel and modify the LSB
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))

            # Encode the text into the least significant bit of each color component
            if data_index < len(binary_text):
                r = r & ~1 | int(binary_text[data_index])
                data_index += 1
            if data_index < len(binary_text):
                g = g & ~1 | int(binary_text[data_index])
                data_index += 1
            if data_index < len(binary_text):
                b = b & ~1 | int(binary_text[data_index])
                data_index += 1

            encoded_pixels[x, y] = (r, g, b)

    # Save the encoded image
    img.save(output_image_path)
    print("Text encoded successfully!")

# Example usage:
text = "Hello World !"
# Encode the text "Hello, world!" into the image "input_image.png" and save the result as "output_image.png"
encode_text("input_image.png", "output_image.png", text)
