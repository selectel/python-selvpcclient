import os
from contextlib import contextmanager

from tests.util.params import LOGO_BASE64


def get_temporary_logo():
    return os.path.join(os.path.dirname(__file__), 'logo.jpg')


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
