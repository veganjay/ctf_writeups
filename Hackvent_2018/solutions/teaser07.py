#!/usr/bin/env python3

from PIL import Image

# Load the provided images
qr3c = Image.open('QR3C.png')

# Create a new image for the solution
solution = Image.new('RGB', (qr3c.height, qr3c.width))

# Get the pixels of the provided images
img = qr3c.load()

# Loop through all the pixels in the images
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BLUE = (0,0,255)
GREEN = (0,255,0)
CYAN = (0,255,255)
RED = (255, 0, 0)
PURPLE = (255,0,255)
YELLOW = (255,255,0)

def solve1(outputname):
    for x in range(qr3c.height):
        for y in range(qr3c.width):
            # Get the components of each pixel
            r, g, b  = img[x,y]
    
            if (r == 0 and g == 0 and b == 0):
                r2, g2, b2 = (0, 0, 0)
            elif (r == 255 and g == 255 and b == 255):
                r2, g2, b2 = (255, 255, 255)
            elif (r == 0):
                r2, g2, b2 = (0, 0, 0)
            else:
                r2, g2, b2 = (255, 255, 255)
    
            # Set the pixel accordingly in the solution image
            pixel = (r2, g2, b2)
            solution.putpixel((x,y), pixel)
    
    # Crop and save the image
    solution.save(outputname)

def solve2(outputname):
    for x in range(qr3c.height):
        for y in range(qr3c.width):
            # Get the components of each pixel
            r, g, b  = img[x,y]
    
            if (r == 0 and g == 0 and b == 0):
                r2, g2, b2 = (0, 0, 0)
            elif (r == 255 and g == 255 and b == 255):
                r2, g2, b2 = (255, 255, 255)
            elif (g == 0):
                r2, g2, b2 = (0, 0, 0)
            else:
                r2, g2, b2 = (255, 255, 255)
    
            # Set the pixel accordingly in the solution image
            pixel = (r2, g2, b2)
            solution.putpixel((x,y), pixel)
    
    # Crop and save the image
    solution.save(outputname)

def solve3(outputname):
    for x in range(qr3c.height):
        for y in range(qr3c.width):
            # Get the components of each pixel
            r, g, b  = img[x,y]
    
            if (r == 0 and g == 0 and b == 0):
                r2, g2, b2 = (0, 0, 0)
            elif (r == 255 and g == 255 and b == 255):
                r2, g2, b2 = (255, 255, 255)
            elif (b == 0):
                r2, g2, b2 = (0, 0, 0)
            else:
                r2, g2, b2 = (255, 255, 255)
    
            # Set the pixel accordingly in the solution image
            pixel = (r2, g2, b2)
            solution.putpixel((x,y), pixel)
    
    # Crop and save the image
    solution.save(outputname)

def main():
    solve1('solve1.png')
    solve2('solve2.png')
    solve3('solve3.png')

if __name__ == '__main__':
    main()
