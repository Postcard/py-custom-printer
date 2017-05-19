
from PIL import Image
from custom_printer.utils import pixels_to_raster, image_to_raster


class TestUtils:

    def test_pixels_to_raster(self):
        pixels = [0, 255, 0, 255, 0, 255, 0, 255] * 5
        result = pixels_to_raster(pixels)
        expected = [170, 170, 170, 170, 170]
        assert result == expected

    def test_image_to_raster(self):
        im = Image.open('./test_ticket.png')
        raster = image_to_raster(im)
        with open('raster.data', 'rb') as f:
            expected = f.read().split(',')
        expected = [int(b) for b in expected]
        assert raster == expected