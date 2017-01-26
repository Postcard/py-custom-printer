
from custom_printer.utils import pixels_to_raster


class TestUtils:

    def test_pixels_to_raster(self):

        pixels = [0, 255, 0, 255, 0, 255, 0, 255] * 5
        result = pixels_to_raster(pixels)
        expected = [170, 170, 170, 170, 170]
        assert result == expected

