import usb.core

from .utils import to_hex


class VKP80(object):

    def __init__(self):

        id_vendor = 0x0dd4
        id_product = 0x0205

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

