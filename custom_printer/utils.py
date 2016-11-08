import math


def to_hex(arr):
    """ convert a decimal array to an hexadecimal String"""
    return ''.join(chr(b) for b in arr)


def image_to_pos(im):
    """ convert an image to a raster bit array """

    (w, h) = im.size

    assert w == 608, 'Image width must be 608px'

    if im.mode != '1':
        im = im.convert('1')

    pixels = list(im.getdata())

    nb_bits = len(pixels) / 8
    byte_array = []
    for i in range(0, nb_bits):
        bit = 0
        for j in range(0, 8):
            offset = i * 8 + j
            v = pixels[offset]
            if v == 0:
                # black pixel
                bit += int(math.pow(2, 7-j))
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