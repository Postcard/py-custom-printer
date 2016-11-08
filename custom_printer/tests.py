from PIL import Image

from .printers import VKP80
from utils import image_to_pos, to_base_256

if __name__ == '__main__':

    printer = VKP80()

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

    x = 608
    y = 1
    xH, xL = to_base_256(x / 8)
    yH, yL = to_base_256(y)
    data = [255] * (x / 8)

    printer.print_raster_image(0, xL, xH, yL, yH, data)
    printer.print_and_feed_paper_n_lines(10)

    printer.present_paper(3, 1, 69, 5)



