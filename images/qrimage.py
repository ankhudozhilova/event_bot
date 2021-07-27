import qrcode
from PIL import Image

def get_qrcode_image(ticket):
    return qrcode.make(ticket)