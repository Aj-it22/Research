import numpy as np
import matplotlib.pyplot as plt

def convert_pe_to_image(pe_file):
    # Open the PE file in binary mode
    with open(pe_file, 'rb') as f:
        file_content = f.read()

    # Calculate the padding size to make the image dimensions square
    padding_size = (512 - len(file_content) % 512) % 512

    # Add the padding to the file content
    padded_content = file_content + bytearray(padding_size)

    # Convert the padded content to a list of integers
    padded_content_list = list(padded_content)

    # Ensure that the padding size is a multiple of the square root of the length of the padded content
    while int(np.sqrt(len(padded_content_list))) * int(np.sqrt(len(padded_content_list))) != len(padded_content_list):
        padded_content_list.append(0)

    # Create a 2D array of 8-bit integers from the padded content
    img_array = np.array(padded_content_list, dtype=np.uint8).reshape((int(np.sqrt(len(padded_content_list))), int(np.sqrt(len(padded_content_list)))))

    # Create a grayscale image from the 2D array
    img = plt.imshow(img_array, cmap='gray')

    # Display the image
    plt.show()
    plt.savefig('Output.png')
    plt.close()

# Example usage
pe_file = '002ce0d28ec990aadbbc89df457189de37d8adaadc9c084b78eb7be9a9820c81.exe'
convert_pe_to_image(pe_file)