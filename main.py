import os
import sys

import config
from exception import TYException
from utils import PrintWithoutHide, Clipboard, html2img


def main(Config: config.Config):
    with Clipboard() as cb:
        html = cb.get_html()
        if html is None:
            return

        cb.write_img(html2img(html), Config.image_type or 'BMP')


if __name__ == '__main__':
    sys.stdout = open(os.devnull, 'w')
    try:
        main(config.get_config())
    except Exception as e:
        TYException(e)
    else:
        with PrintWithoutHide():
            print("Success")
