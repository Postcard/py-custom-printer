# -*- coding: utf8 -*-

import usb.core
import usb.util

from .utils import to_hex, byte_to_bits


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

        if self.device is None:
            raise ValueError("Printer not found. Make sure the cable is plugged in.")

        if self.device.is_kernel_driver_active(0):
            try:
                self.device.detach_kernel_driver(0)
            except usb.core.USBError as e:
                print("Could not detatch kernel driver: %s" % str(e))

        configuration = self.device.get_active_configuration()
        interface = configuration[(0, 0)]

        def out_endpoint_match(ep):
            return usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_OUT

        self.out_endpoint = usb.util.find_descriptor(interface, custom_match=out_endpoint_match)

        def in_endpoint_match(ep):
            return usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_IN

        self.in_endpoint = usb.util.find_descriptor(interface, custom_match=in_endpoint_match)

    def write_bytes(self, byte_array):
        msg = to_hex(byte_array)
        self.write(msg)

    def write(self, msg):
        self.out_endpoint.write(msg, timeout=5000)

    def read(self):
        try:
            return self.in_endpoint.read(self.in_endpoint.wMaxPacketSize)
        except usb.core.USBError as e:
            print(e)
            return None

    def flush_read(self):
        while True:
            data = self.read()
            if not data:
                break


class VKP80III(CustomPrinter):

    def __init__(self):
        id_product = 0x0205
        super(VKP80III, self).__init__(id_product)

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
    def define_downloaded_bit_image(self, x, y, data):
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

    @send_command_to_device
    def transmit_real_time_status(self, n):
        """ Transmits the selected printer status specified by n in real time according to the following parameters:
        :param n:
        n= 1 transmit printer status
        n= 2 transmit off-line status
        n= 3 transmit error status
        n= 4 transmit paper roll sensor status
        n = 17 transmit print status
        n = 20 transmit FULL STATUS
        :return:
        """
        return [16, 4, n]

    def is_online(self):
        self.transmit_real_time_status(1)
        data = self.read()
        bits = byte_to_bits(data[0])
        return bits[3] == 0

    def paper_present(self):
        self.flush_read()
        self.transmit_real_time_status(4)
        data = self.read()
        bits = byte_to_bits(data[0])
        return bits[5] == 0

    def near_paper_end(self):
        self.transmit_real_time_status(4)
        data = self.read()
        bits = byte_to_bits(data[0])
        return bits[2] == 1

    @send_command_to_device
    def set_left_margin(self, nL, nH):
        """
        Set the left margin.
        The left margin is set to [(nL + nH * 256) * horizontal motion unit]
        :return:
        """
        return [29, 76, nL, nH]

    @send_command_to_device
    def enable_mass_storage(self, m):
        """
        Enable or disable the mass storage function in RAM according to m value
        :param m: m=0 enable mass storage m=1 disable mass storage
        :return:
        """
        return [28, 110, m]

    def manage_true_type_font(self, m, n, font_name=None):
        """
        Manage the TrueType fonts depending on the following values of m
        :param m:
        :param n:
        :param data:
        :return:
        """
        byte_array = [28, 102, m, n]
        msg = to_hex(byte_array)
        self.write(msg)
        if font_name:
            self.write(font_name)

    @send_command_to_device
    def set_character_font(self, n):
        """
        Selects characters font depending of cpi value set (Char/Inch)
        :param n:
        :return:
        """
        return [27, 77, n]

    @send_command_to_device
    def select_character_size(self, n):
        """
        Select character size
        Selects character height and width, as follows:
        :param n: 0 <= n <= 255
        • Bits 0 to 3: to select character height
        • Bits 4 to 7: to select character width
        :return:
        """
        return [29, 33, n]


    @send_command_to_device
    def select_international_character_set(self, n):
        """
        :param n:
        n=0 USA
        n=1 France
        n=2 Germany
        n=3 United Kingdom
        n=4 Denmark I
        n=5 Sweden
        n=6 Italy
        n=7 Spain I
        n=8 Japan
        n=9 Norway
        n=10 Denmark II
        :return:
        """
        return [27, 82, n]


    def select_character_code_table(self, n):
        return [27, 116, n]


