import usb.core

from .printers import VKP80III
from .utils import byte_to_bits


if __name__ == '__main__':

    printer = VKP80III()

    printer.initialize()

    # file_path = '/Users/benoit/Documents/Figure/Engineering/Imprimantes-Custom/template/ticket.jpg'
    #
    # im = Image.open(file_path)
    # (w, h) = im.size
    # data = image_to_pos(im)
    # xH, xL = to_base_256(w / 8)
    # yH, yL = to_base_256(h)
    #
    # printer.print_raster_image(0, xL, xH, yL, yH, data)

    # x = 608
    # y = 1
    # xH, xL = to_base_256(x / 8)
    # yH, yL = to_base_256(y)
    # data = [255] * (x / 8)
    #
    # printer.print_raster_image(0, xL, xH, yL, yH, data)
    # printer.print_and_feed_paper_n_lines(10)
    #
    # printer.present_paper(3, 1, 69, 5)

    # printer.transmit_real_time_status(4)
    # data = printer.read()
    # print(byte_to_bits(data[0]))

    print("is online", printer.is_online())
    print("paper present", printer.paper_present())
    print("near paper end", printer.near_paper_end())

    #print(byte_to_bits(data[0]))





