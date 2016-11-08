from PIL import Image

from .printers import VKP80
from .commands import print_and_feed_paper_n_lines, present_paper, download_bit_image, print_downloaded_bit_image
from .commands import initialize, set_print_speed, set_print_density, print_raster_image
from .commands import set_horizontal_and_vertical_motion_units
from utils import image_to_pos

if __name__ == '__main__':

    printer = VKP80()

    printer.write_bytes(initialize())

    # print 4 lines
    #command = print_and_feed_paper_n_lines(30)
    #printer.write_bytes(command)


    printer.write_bytes(set_print_speed(0))
    printer.write_bytes(set_print_density(5))
    printer.write_bytes(set_horizontal_and_vertical_motion_units(1, 0, 1, 0))

    # x = 72
    # y = 21
    # data_size = x * y * 8
    # data = [170, 85] * int(data_size / 2)
    # data = []
    # for i in range(0, x * 8):
    #     if i % 16 < 8:
    #         data.extend([0] * 20)
    #     else:
    #         data.extend([255] * 20)
    # print len(data)


    # data = [0, 255] * int(x * y * 8 / 2.0)
    # printer.write_bytes(download_bit_image(x, y, data))
    # printer.write_bytes(print_downloaded_bit_image(0))


    # xL = 76
    # xH = 0
    # x = xL + 256 * xH
    # yL = 0
    # yH = 2
    # y = yL + 256 * yH

    #data = [0, 255] * int(x * y / 2)

    # data = []
    # for i in range(0, y):
    #     if i % 2 == 0:
    #         data.extend([0, 255] * (x / 2))
    #     else:
    #         data.extend([255, 0] * (x / 2))
    # printer.write_bytes(print_raster_image(0, xL, xH, yL, yH, data))


    # xL = 76
    # xH = 0
    # x = xL + 256 * xH
    # yL = 255
    # yH = 0
    # y = yL + 256 * yH
    #
    # data = []
    # s = x / 4
    # for i in range(0, y):
    #     if i % 2 == 0:
    #         print("PAIR")
    #         data.extend([255] * s)
    #         data.extend([0] * s)
    #         data.extend([255] * s)
    #         data.extend([0] * s)
    #     else:
    #         print("IMPAIR")
    #         data.extend([0] * s)
    #         data.extend([255] * s)
    #         data.extend([0] * s)
    #         data.extend([255] * s)
    #
    #
    # printer.write_bytes(print_raster_image(0, xL, xH, yL, yH, data))
    # printer.write_bytes(print_and_feed_paper_n_lines(20))

    file_path = '/Users/benoit/Documents/Figure/Engineering/Imprimantes-Custom/template/ticket.jpg'

    im = Image.open(file_path)
    (w, h) = im.size
    data = image_to_pos(im)
    xL = w / 8
    xH = 0
    yL = h % 256
    yH = (h - yL) / 256
    printer.write_bytes(print_raster_image(0, xL, xH, yL, yH, data))

    command = present_paper(3, 1, 69, 5)
    printer.write_bytes(command)


