"""
EDGE DETECTION USING SOBEL OPERATOR

The Sobel operator, sometimes called the Sobel–Feldman operator or Sobel filter, is used in image processing
and computer vision, particularly within edge detection algorithms where it creates an image emphasising edges
"""

from simpleimage import SimpleImage
import math


def main():
    image = SimpleImage("index.jpg")  # READING IN THE IMAGE
    image.show()  # SHOWING THE IMAGE

    grayed = gray_scale(image)  # PASSING THE IMAGE THAT HAS BEEN CONVERTED TO GRAYSCALE TO A VARIABLE
    grayed.show()
    grayed.pil_image.save("grayed.png")  # SAVING THE IMAGE

    horizontal_edge = horizontal_edge_detect(grayed)  # DETECTING THE HORIZONTAL EDGES IN THE GRAYED IMAGE
    horizontal_edge.show()
    horizontal_edge.pil_image.save("horizontal_detect.png")

    vertical_edge = vertical_edge_detect(grayed)    # DETECTING THE VERTICAL EDGES IN THE GRAYED IMAGE
    vertical_edge.show()
    vertical_edge.pil_image.save("vertical_detect.png")

    edge_detection = edge_detect(horizontal_edge, vertical_edge)    # DETECTING THE EDGES IN THE IMAGE
    edge_detection.show()
    edge_detection.pil_image.save("detected_edge.png")

    together = output_together(image, edge_detection)   # PUTTING BOTH THE ORIGINAL IMAGE AND THE ONE WITH EDGES DETECTED IN THE SAME FRAME
    together.show()


def gray_scale(image):
    """
    Simply takes in an image and converts it to grayscale by it by multiplying the red, green and blue value
    of each pixel by 0.299, 0.587 and 0.114 respectively.
    :param image: An image or picture
    :return copy: The grayscale version of the image that was passed in
    """
    copy = copy_image(image)
    for pixel in copy:
        gray = (0.299 * pixel.red) + (0.587 * pixel.green) + (0.114 * pixel.blue)
        pixel.red = gray
        pixel.green = gray
        pixel.blue = gray
    return copy


def copy_image(image):
    """
    Simply takes in an image and copies it
    :param image: An image or picture
    :return image_copy: a copy of the image that was passed in
    """
    width = image.width
    height = image.height

    image_copy = SimpleImage.blank(width, height)

    for x in range(width):
        for y in range(height):
            pixel = image.get_pixel(x, y)
            image_copy.set_pixel(x, y, pixel)
    return image_copy


def in_bound(x, y, width, height):
    """
    Returns True if the given pixel coordinates (x, y)
    is located inside the image with dimension (width, height).
    Returns False otherwise.
    All parameters are integers
    """
    if 0 <= x < width and 0 <= y < height:
        return True
    return False


def horizontal_edge_detect(image):
    """
    Loops over the pixels in an image and detects the horizontal edges
    :param image: An image or picture that must've been converted to grayscale
    :return new_image: a copy of the image passed in with the horizontal edges detected
    """
    rows = image.width
    columns = image.height

    new_image = copy_image(image)

    for x in range(1, rows - 2):
        for y in range(1, columns - 2):
            horizontal_gradient(x, y, image, new_image)
    return new_image


def horizontal_gradient(x, y, image, image_copy):
    """
    Forms a 3x3 matrix around the pixel been looped over and then multiply each value in the matrix
    by the corresponding value in the list 'gx'. The result of the multiplication in the matrix is added together
    and this sum is set as the new value of the pixel being lopped over to get the horizontal detection
    :param x: integer along with y depicting the position of a pixel
    :param y: integer along with x depicting the position of a pixel
    :param image: an image which its pixels will be looped over
    :param image_copy: The result of the computation on 'image' is set as the pixel values of image_copy
    :return image_copy:
    """
    gx = [-1, 0, 1, -2, 0, 2, -1, 0, 1]

    add = 0
    index = 0

    for i in range(x - 1, x + 1 + 1):
        for j in range(y - 1, y + 1 + 1):
            if in_bound(i, j, image.width, image.height):
                pixel = image.get_pixel(i, j)
                average = (pixel.red + pixel.green + pixel.blue) // 3
                multiply_matrix = average * gx[index]
                add += multiply_matrix
                index += 1
    pix = image_copy.get_pixel(x, y)
    pix.red = add
    pix.green = add
    pix.blue = add
    return image_copy


def vertical_edge_detect(image):
    """
    Loops over the pixels in an image and detects the vertical edges
    :param image: An image or picture that must've been converted to grayscale
    :return new_image: a copy of the image passed in with the vertical edges detected
    """
    rows = image.width
    columns = image.height

    new_image = copy_image(image)

    for x in range(1, rows - 2):
        for y in range(1, columns - 2):
            vertical_gradient(x, y, image, new_image)
    return new_image


def vertical_gradient(x, y, image, image_copy):
    """
    Forms a 3x3 matrix around the pixel been looped over and then multiply each value in the matrix
    by the corresponding value in the list 'gy'. The result of the multiplication in the matrix is added together
    and this sum is set as the new value of the pixel being lopped over to get the vertical detection
    :param x: integer along with y depicting the position of a pixel
    :param y: integer along with x depicting the position of a pixel
    :param image: an image which its pixels will be looped over
    :param image_copy: The result of the computation on 'image' is set as the pixel values of image_copy
    :return image_copy:
    """
    gy = [-1, -2, -1, 0, 0, 0, 1, 2, 1]

    add = 0
    index = 0

    for i in range(x - 1, x + 1 + 1):
        for j in range(y - 1, y + 1 + 1):
            if in_bound(i, j, image.width, image.height):
                pixel = image.get_pixel(i, j)
                average = (pixel.red + pixel.green + pixel.blue) // 3
                multiply_matrix = average * gy[index]
                add += multiply_matrix
                index += 1
    pix = image_copy.get_pixel(x, y)
    pix.red = add
    pix.green = add
    pix.blue = add
    return image_copy


def edge_detect(horizontal, vertical):
    """
    For each corresponding pixel in both images passed in, the pixel values are squared and added
    together then the square root of the result is found. The result is set as the pixel value od the
    copied image 'new_image'
    :param horizontal: Image with horizontal edges detected
    :param vertical: Image with vertical edges detected
    :return new_image: An image with all the edges detected
    """
    width = horizontal.width
    height = horizontal.height

    new_image = copy_image(horizontal)

    for x in range(width):
        for y in range(height):
            x_pix = horizontal.get_pixel(x, y)
            x_average = (x_pix.red + x_pix.green + x_pix.blue) // 3
            y_pix = vertical.get_pixel(x, y)
            y_average = (y_pix.red + y_pix.green + y_pix.blue) // 3

            magnitude = int(math.sqrt(x_average ** 2 + y_average ** 2))

            pixel = new_image.get_pixel(x, y)
            pixel.red = magnitude
            pixel.green = magnitude
            pixel.blue = magnitude
    return new_image


def output_together(image1, image2):
    """
    Takes in two images and makes them one by placing them by each other
    Both parameters are images
    :return double: returns an image which is a combination of the images passed in
    """
    width = image1.width
    height = image1.height

    double = SimpleImage.blank(width * 2, height)

    for x in range(width):
        for y in range(height):
            pixel1 = image1.get_pixel(x, y)
            pixel2 = image2.get_pixel(x, y)
            double.set_pixel(x, y, pixel1)
            double.set_pixel(width + x, y, pixel2)
    return double


if __name__ == '__main__':
    main()
