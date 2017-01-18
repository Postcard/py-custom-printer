import usb.core

from PIL import Image

from .printers import VKP80III
from .utils import byte_to_bits, image_to_raster, to_base_256


if __name__ == '__main__':

    printer = VKP80III()

    printer.initialize()

    #printer.manage_true_type_font(4, 14, "asmregular.ttf")
    #printer.set_character_font(48)
    #printer.select_character_size(0)
    #printer.manage_true_type_font(32, 0)
    #printer.select_international_character_set(1)
    #printer.select_character_code_table(4)
    #printer.set_left_margin(10, 0)
    #printer.write(chr(123))
    #printer.write('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer egestas sed lorem a molestie. Mauris sit amet sapien venenatis, sodales dolor sed, sodales nunc. Donec placerat eleifend purus et pharetra. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Suspendisse mollis dapibus sapien sed pellentesque. Duis eu sapien varius, posuere leo vel, ultricies risus. Maecenas non sem viverra, finibus dui et, rutrum eros. Aliquam purus magna, tristique et pulvinar eget, fringilla ut tortor. Praesent ex arcu, tincidunt vel placerat vel, tincidunt vel leo. Cras ut lectus at orci porttitor interdum. Cras fermentum gravida nisi, sed molestie elit pulvinar nec. In a lorem a dui sodales aliquam. Etiam tincidunt feugiat ante sed posuere.')
    #printer.print_and_feed_paper_n_lines(10)
    #printer.present_paper(3, 1, 69, 5)


    file_path = '/Users/benoit/Documents/Figure/Engineering/Imprimantes-Custom/template/ticket_640_sharpen.jpg'
    #
    im = Image.open(file_path)
    (w, h) = im.size
    #
    #
    data = image_to_raster(im)
    xH, xL = to_base_256(w / 8)
    yH, yL = to_base_256(h)
    #
    printer.print_raster_image(0, xL, xH, yL, yH, data)
    printer.present_paper(23, 1, 69, 0)

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

    #print("is online", printer.is_online())
    #print("paper present", printer.paper_present())
    #print("near paper end", printer.near_paper_end())

    #print(byte_to_bits(data[0]))





