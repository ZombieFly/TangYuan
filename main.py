import sys
import os
from re import sub
from io import BytesIO
from typing import Optional, cast

import win32clipboard as wc
from win32con import CF_DIB
from imgkit import from_string
from PIL.Image import open as ImageOpen

import config


class PrintWithoutHide:
    def __init__(self, extra: str = ''):
        self._extra = extra

    def __enter__(self):
        sys.stdout = sys.__stdout__

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(self._extra)
        sys.stdout = open(os.devnull, 'w')


class Clipboard:
    def __init__(self):
        self._clipboard = wc

    def __getattr__(self, item):
        return getattr(self._clipboard, item)

    def __enter__(self):
        self._clipboard.OpenClipboard()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clipboard.CloseClipboard()

    def open(self) -> None:
        self._clipboard.OpenClipboard()

    def close(self) -> None:
        self._clipboard.CloseClipboard()

    def get_html(self) -> str:
        try:
            raw = str(cast(bytes, wc.GetClipboardData(wc.EnumClipboardFormats(0))),
                      encoding='utf-8')
            return '\r\n'.join(raw.split('\r\n')[6:])
        except (IndexError, TypeError) as e:
            raise ValueError('Clipboard is not contain html') from e

    def write_img(self, data: bytes, _type: str) -> Optional[int]:
        out = ImageOpen(BytesIO(data))
        out.save(fp := BytesIO(), _type)
        return self._clipboard.SetClipboardData(CF_DIB, fp.getvalue()[14:])


def main(Config: config.Config):
    with Clipboard() as cb:
        html = cb.get_html()
        if html is None:
            return

        html = sub(
            r'<html>', '<html><head><link rel="stylesheet" href="style.css"></head>', html)

        html = sub(
            r'<body>', '<body><div class="box"><div id="header"><span style="color: #c9d1d9">Generated by TangYuan</span></div>', html)

        html = sub(r'</body>', '</div></body>', html)

        image: bytes = cast(bytes, from_string(html, None, css="style.css",
                                               options={
                                                   'enable-local-file-access': None}
                                               )
                            )
        cb.write_img(image, Config.image_type or 'BMP')


if __name__ == '__main__':
    sys.stdout = open(os.devnull, 'w')
    try:
        main(config.get_config())
    except OSError as os_error:
        with PrintWithoutHide(os_error.args[0]):
            pass
    except ValueError:
        print("Success, but clipboard is not contain html")
    except Exception as e:
        with PrintWithoutHide(str(e)):
            pass
    else:
        with PrintWithoutHide():
            print("Success")
