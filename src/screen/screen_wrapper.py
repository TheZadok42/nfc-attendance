from typing import List
from libs.screen import SPI, SSD1305
from src import consts
from PIL import Image, ImageDraw, ImageFont

# Raspberry Pi pin configuration:
RST = None  # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 24
SPI_PORT = 0
SPI_DEVICE = 0
SCREEN_MAX_SPEED = 8000000

MAX_LINE_CHARECTHERS = 30


class ScreenWrapper:
    def __init__(self):
        self._connector = None
        self._width = None
        self._height = None

    def setup(self):
        dispay_spi = SPI.SpiDev(SPI_PORT, SPI_DEVICE, SCREEN_MAX_SPEED)
        self._connector = SSD1305.SSD1305_128_32(rst=RST,
                                                 dc=DC,
                                                 spi=dispay_spi)
        self._width = self._connector.width
        self._height = self._connector.height

        self._connector.begin()

    def write(self, text: str):
        lines = self._get_lines(text)
        image = self._create_image(lines)
        self.display_image(image)

    def display_image(self, image: Image):
        self._connector.clear()
        self._connector.image(image)
        self._connector.display()

    @property
    def _base_image(self):
        image = Image.new('1', (self._width, self._height))
        draw_image = ImageDraw.Draw(image)
        draw_image.rectangle((0, 0, self._width, self._height),
                             outline=0,
                             fill=0)
        return image, draw_image

    @property
    def _text_font(self):
        return ImageFont.truetype(str(consts.TEXT_FONT_PATH), 12)

    @staticmethod
    def _get_lines(text: str) -> List[str]:
        parsed_lines = list()
        base_lines = text.splitlines(False)
        for line in base_lines:
            for index in range(0, len(line), MAX_LINE_CHARECTHERS):
                parsed_lines.append(line[index:index + MAX_LINE_CHARECTHERS])
        return parsed_lines

    def _create_image(self, lines: List[str]) -> Image:
        image, draw_image = self._base_image
        for index, line in enumerate(lines):
            self._add_line(draw_image, line, index)
        return image

    def _add_line(self,
                  draw_image: ImageDraw.ImageDraw,
                  line: str,
                  line_index: int = 0):
        draw_image.text((0, 8 * line_index),
                        line,
                        font=self._text_font,
                        fill=255)
