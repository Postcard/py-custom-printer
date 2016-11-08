

def print_and_feed_paper():
    """
    Prints the data in the print buffer and feeds paper 1 line
    :return:
    """
    return [10]


def print_and_feed_paper_n_lines(n):
    """
    Prints the data in the print buffer and feeds paper n lines
    :param n: number of lines to be fed
    :return:
    """
    return [27, 100, n]


def set_left_margin(nL, nH):
    """
    Sets the left margin as (nL + 256 * nH) * (horizontal motion unit)
    """
    return [29, 76, nL, nH]


def set_printing_area_width(nL, nH):
    """
    Sets the printing area width to the area specified by nL and nH
    0 <= nL + nH * 256 <= 576
    """
    return [29, 87, nL, nH]


def set_horizontal_and_vertical_motion_units(xH, xL, yH, yL):
    """
    Sets the horizontal and vertical motion units to 1/((xH * 256) + xL) inch and 1/((yH * 256) + yL) inch respectively
    """
    return [29, 80, xH, xL, yH, yL]


def set_print_speed(n):
    """
    :param n: 0 <= n <= 2
    n=0 High quality
    n=1 Normal
    n=2 High speed
    :return:
    """
    return [29, 240, n]


def set_print_density(n):
    """
    Set printing density
    :param n:
    n = 0 -50%
    n=1 -37,5%
    n=2 -25%
    n=3 -12,5%
    n=4 0%
    n=5 +12,5%
    n=6 +25%
    n=7 +37,5%
    n=8 + 50%
    :return:
    """
    return [29, 124, n]


def present_paper(a, b, c, d):
    """

    :param a: number of steps for the ticket present (1 step=5mm)
    :param b: b=0 led OFF, b=1 led blinking
    :param c: indicates the ticket movement after the print as follow c=E eject ticket c=R retract ticket
    :param d: timeout
    :return:
    """
    return [28, 80, a, b, c, d]


def download_bit_image(x, y, data):
    """
    Defines a downloaded bit image using the number of dots specified by x and y
    :param x: specifies the number of dots in the horizontal direction
    :param y: specifies the number of dots in the vertical direction
    :param data:
    :return:
    """
    data_size = x * y * 8
    assert len(data) == data_size
    bytes_arr = [29, 42, x, y]
    bytes_arr.extend(data)
    return bytes_arr


def print_downloaded_bit_image(m=0):
    """
    Prints a downloaded bit image using the mode specified by m.
    :param m: selects a mode from the table below:
    m = 0,48 Normal
    m = 1,49 Double width
    m = 2,50 Double height
    m = 3,51 Quadruple
    :return:
    """
    return [29, 47, m]


def print_raster_image(m, xL, xH, yL, yH, data):
    """
    Selects raster bit image mode
    :param m:
    m=0 Normal
    m=1 Double width
    m=2 Double height
    m=3 Quadruple
    :param xL, xH: number of data bits (xL + xH * 256) in the horizontal direction
    :param yL, yH: number of data bits (yL + yH * 256) in the vertical direction
    :param data:
    :return:
    """
    bytes_arr = [29, 118, 48, m, xL, xH, yL, yH]
    bytes_arr.extend(data)
    return bytes_arr


def initialize():
    return [27, 64]