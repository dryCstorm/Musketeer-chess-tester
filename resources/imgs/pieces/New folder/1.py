from PIL import Image

# Open the original PNG file
original_image = Image.open("original.png")

# Define the size of the individual blocks
block_size = 100

# Iterate over the original image in 100 x 100 blocks
for y in range(0, original_image.height, block_size):
    for x in range(0, original_image.width, block_size):
        # Crop each 100 x 100 block
        box = (x, y, x + block_size, y + block_size)
        cropped_image = original_image.crop(box)
        
        # Save each cropped block as a separate image
        cropped_image.save(f"block_{x}_{y}.png")

# Close the original image
original_image.close()