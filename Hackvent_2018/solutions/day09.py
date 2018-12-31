#!/usr/bin/env python3

from PIL import Image

# Load the provided images
ball_original = Image.open('provided/medium_64.png')
ball_fake = Image.open('provided/medium-64-fake.png')

# Create a new image for the solution
solution = Image.new('1', (ball_original.height, ball_original.width))

# Get the pixels of the provided images
img1 = ball_original.load()
img2 = ball_fake.load()

# Loop through all the pixels in the images
for x in range(ball_original.height):
    for y in range(ball_original.width):
        # Get the components of each pixel
        r1, g1, b1, a1 = img1[x,y]
        r2, g2, b2, a2 = img2[x,y]

        # Perform an xor on the green component
        g3 = g1 ^ g2

        # Set the pixel accordingly in the solution image
        pixel = 0
        if (g3 > 0):
            pixel = 1
        solution.putpixel((x,y), pixel)

# Crop and save the image
cropped = solution.crop((20, 20, 45, 45))
cropped.save('day09.png')
