import pathlib

ROOT = pathlib.Path(__file__).absolute().parent
FONTS_DIR = ROOT.joinpath("./assets/fonts")
TEXT_FONT = FONTS_DIR.joinpath("FreePixel.ttf")