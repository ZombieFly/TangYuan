from re import sub
from io import BytesIO
from typing import Optional, cast

import imgkit
import win32con
from PIL import Image
import win32clipboard as wc

import config


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
        except TypeError as e:
            raise ValueError('Clipboard is not contain html') from e
        try:
            return '\r\n'.join(raw.split('\r\n')[6:])
        except IndexError as e:
            raise ValueError('Clipboard is not contain html') from e

    def write_img(self, data: bytes, _type: str) -> Optional[int]:
        out = Image.open(BytesIO(data))
        out.save(fp := BytesIO(), _type)
        return self._clipboard.SetClipboardData(win32con.CF_DIB, fp.getvalue()[14:])


def main(Config: config.Config):
    with Clipboard() as cb:
        html = cb.get_html()
        if html is None:
            return

        html = sub(r'font-size: 13px;line-height: 18px;',
                   'font-size: 26px;line-height: 42px;', html)

        image: bytes = cast(bytes, imgkit.from_string(html, None))
        cb.write_img(image, Config.image_type or 'BMP')


if __name__ == '__main__':
    main(config.get_config())
