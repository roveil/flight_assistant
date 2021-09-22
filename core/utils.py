import datetime

import imgkit

from core.config import WKHTMLTOIMAGE_PATH


def generate_image_from_html(html: str, width: int = 200, height: int = 200, zoom: float = 1,
                             format: str = 'jpg') -> bytes:
    """
    Generates image from html
    :param html: string with html code
    :param width: Width in pixels of image
    :param height: Height in pixels of image
    :param zoom: zoom
    :param format: image file format
    :return: image bytes
    """
    config = imgkit.config(wkhtmltoimage=WKHTMLTOIMAGE_PATH)
    return imgkit.from_string(html, False, config=config, options={'height': height, 'width': width, 'zoom': zoom,
                                                                   'format': format})


def get_timestamp_in_milliseconds() -> int:
    """
    Returns current timestamp in milliseconds
    :return: value of current timestamp in milliseconds
    """
    return int(datetime.datetime.now().timestamp() * 1000)


class SingletonMeta(type):
    """
    Realises singleton pattern
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
