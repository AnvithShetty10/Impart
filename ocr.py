import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO
from pypdf_to_image import convert


def process_image(url):
    return pytesseract.image_to_string(Image.open(url))




def _get_image(url):
    return Image.open(StringIO(requests.get(url).content))
