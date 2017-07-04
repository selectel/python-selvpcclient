import os

from contextlib import contextmanager
from random import randint
from PIL import Image

from tests.util.params import LOGO_BASE64


@contextmanager
def get_temporary_logo():
    path_to_logo = os.path.join(os.path.abspath('.'),
                                'tests/util/temp_logo.png')
    try:
        image = Image.new("RGBA", (16, 16), (randint(1, 100),
                                             randint(1, 100),
                                             randint(1, 100),
                                             randint(1, 100)))
        image.save(path_to_logo)
        yield path_to_logo
    finally:
        os.remove(path_to_logo)


@contextmanager
def get_temporary_text_file():
    path_to_file = os.path.join(os.path.abspath('.'),
                                'tests/util/temp_txt.txt')
    try:
        with open(path_to_file, "w") as b64_file:
            b64_file.write(LOGO_BASE64)
        yield path_to_file
    finally:
        os.remove(path_to_file)
