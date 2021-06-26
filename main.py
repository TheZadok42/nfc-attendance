from os import path
import pathlib

from PIL import Image, ImageDraw, ImageFont

from libs.screen import SPI, SSD1305

ROOT = pathlib.Path(__file__).absolute().parent
FONTS_DIR = ROOT.joinpath("./assets/fonts")
TEXT_FONT = FONTS_DIR.joinpath("FreePixel.ttf")

# Raspberry Pi pin configuration:
RST = None  # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 24
SPI_PORT = 0
SPI_DEVICE = 0
dispay_spi = SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000)
display = SSD1305.SSD1305_128_32(rst=RST, dc=DC, spi=dispay_spi)

display.begin()

display.clear()
display.display()

width = display.width
height = display.height

image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, width, height), outline=0, fill=0)
padding = 0
top = padding
bottom = height - padding
x = 0

font = ImageFont.truetype(str(TEXT_FONT))
draw.text((x, top), "Test", font=font, fill=255)

display.image(image)
display.display()
