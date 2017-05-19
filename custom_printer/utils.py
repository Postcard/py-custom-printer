import math

import numpy as np


def to_hex(arr):
    """ convert a decimal array to an hexadecimal String"""
    return ''.join(chr(b) for b in arr)


def image_to_raster(im):
    """ convert an image to a raster bit array used in the print raster command"""

    if im.mode != '1':
        im = im.convert('1')
    pixels = np.asarray(im, dtype=int)
    pixels.flatten()
    return pixels_to_raster(pixels)


def pixels_to_raster(pixels):

    packed = np.packbits(pixels)
    inverted = np.invert(packed)
    return inverted.tolist()


def image_to_bit_image(im):
    """ convert an image to a bit array used in the download bit image command """

    (w, h) = im.size

    assert h == 160, 'Image height must be 160px'

    if im.mode != '1':
        im = im.convert('1')

    pixels = list(im.getdata())

    return pixels_to_bit_image(pixels, w, h)


def pixels_to_bit_image(pixels, w, h):

    nb_lines = h / 8
    nb_columns = w
    byte_array = []

    assert nb_columns * nb_lines * 8 == len(pixels)

    for i in range(0, nb_columns):
        for j in range(0, nb_lines):
            bit = 0
            for k in range(0, 8):
                offset = (j * 8 + k) * w + i
                v = pixels[offset]
                if v == 0:
                    # black pixel
                    bit += int(math.pow(2, 7-k))
            byte_array.append(bit)
    return byte_array


def to_base_256(number):
    """ returns the base 256 representation of the number """
    nL = number % 256
    nH = (number - nL) / 256
    return nH, nL


def byte_to_bits(b):

    assert b <= 255

    r = b

    bits = {}

    for i in range(0, 8):
        a = math.pow(2, 7 - i)
        bits[7 - i] = int(r // a)
        r = r % a

    return bits