from functools import wraps

import usb.core

from .utils import to_hex


def send_command_to_device(func):
    """ decorator used to send the result of a command to the usb device"""
    def wrapper(*args, **kwargs):
        printer = args[0]
        byte_array = func(*args, **kwargs)
        printer.write_bytes(byte_array)
    return wrapper


class CustomPrinter(object):

    def __init__(self, id_product):

        id_vendor = 0x0dd4
        self.device = usb.core.find(idVendor=id_vendor, idProduct=id_product)
        self.out_ep = 0x02

        if self.device is None:
            raise ValueError("Printer not found. Make sure the cable is plugged in.")

        if self.device.is_kernel_driver_active(0):
            try:
                self.device.detach_kernel_driver(0)
            except usb.core.USBError as e:
                print("Could not detatch kernel driver: %s" % str(e))

    def write_bytes(self, byte_array):
        msg = to_hex(byte_array)
        self.write(msg)

    def write(self, msg):
        self.device.write(self.out_ep, msg,  timeout=20000)


class VKP80(CustomPrinter):

    def __init__(self):
        id_product = 0x0205
        super(VKP80, self).__init__(id_product)

    @send_command_to_device
    def print_and_feed_paper(self):
        """
        Prints the data in the print buffer and feeds paper 1 line
        :return:
        """
        return [10]

    @send_command_to_device
    def print_and_feed_paper_n_lines(self, n):
        """
        Prints the data in the print buffer and feeds paper n lines
        :param n: number of lines to be fed
        :return:
        """
        return [27, 100, n]

    @send_command_to_device
    def set_left_margin(self, nL, nH):
        """
        Sets the left margin as (nL + 256 * nH) * (horizontal motion unit)
        """
        return [29, 76, nL, nH]

    @send_command_to_device
    def set_printing_area_width(self,nL, nH):
        """
        Sets the printing area width to the area specified by nL and nH
        0 <= nL + nH * 256 <= 576
        """
        return [29, 87, nL, nH]

    @send_command_to_device
    def set_horizontal_and_vertical_motion_units(self, xH, xL, yH, yL):
        """
        Sets the horizontal and vertical motion units to 1/((xH * 256) + xL) inch and 1/((yH * 256) + yL) inch respectively
        """
        return [29, 80, xH, xL, yH, yL]

    @send_command_to_device
    def set_print_speed(self, n):
        """
        :param n: 0 <= n <= 2
        n=0 High quality
        n=1 Normal
        n=2 High speed
        :return:
        """
        return [29, 240, n]

    @send_command_to_device
    def set_print_density(self, n):
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

    @send_command_to_device
    def present_paper(self, a, b, c, d):
        """

        :param a: number of steps for the ticket present (1 step=5mm)
        :param b: b=0 led OFF, b=1 led blinking
        :param c: indicates the ticket movement after the print as follow c=E eject ticket c=R retract ticket
        :param d: timeout
        :return:
        """
        return [28, 80, a, b, c, d]

    @send_command_to_device
    def download_bit_image(self, x, y, data):
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

    @send_command_to_device
    def print_downloaded_bit_image(self, m=0):
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

    @send_command_to_device
    def print_raster_image(self, m, xL, xH, yL, yH, data):
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

    @send_command_to_device
    def initialize(self):
        return [27, 64]



