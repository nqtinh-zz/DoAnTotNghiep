#  @Project FCloudConsole
#  @Homepage https://fsmartstore.com
#  @Copyright (c) 2018 Fujinet Systems JSC. All Rights Reserved.
#  @License All resources of the source code are owned by 'Fujinet Systems JSC'.
#  Intentionally infringing, stealing, exchanging, or trading in all of the
#  resources below without our consent, is a violation of intellectual property
#  rights. So, if you accidentally receive this source code, please send an email
#  to rd-support@fujinet.net, so we can find the best solution for this problem.

import base64
from io import BytesIO

import cv2
import numpy as np
import scipy.misc
from PIL import Image


def image_file_to_np_image(file, mode='RGB'):
    """
    Loads an image file (.jpg, .png, etc) into a numpy array

    :param file: image file name or file object to load
    :param mode: format to convert the image to. Only 'RGB' (8-bit RGB) and 'L' (black and white) are supported.
    :return: image contents as numpy array in RGB mode
    """
    return scipy.misc.imread(file, mode=mode)


def image_file_str_to_np_image(img_str):
    """
    Loads an image file (.jpg, .png, etc) into a numpy array

    :param img_str: image file as string
    :return: image contents as numpy array
    """
    nparr = np.fromstring(img_str, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)


def base64_str_to_np_image(base64_img_str):
    img_data = base64.b64decode(base64_img_str)
    pil_image = Image.open(BytesIO(img_data))
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_BGR2RGB)


def np_arr_to_base64(np_img):
    return base64.b64encode(np_img).decode('UTF-8')


def image_file_to_base64_str(file):
    with open(file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string


def multipart_file_to_np_image(buffered_file):
    # noinspection PyBroadException
    try:
        return cv2.imdecode(np.fromstring(buffered_file.read(), np.uint8), cv2.IMREAD_COLOR)
    except Exception:
        return None


def np_image_to_multipart_file(np_img):
    np_img = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)
    pil_img = Image.fromarray(np_img)
    byte_io = BytesIO()
    pil_img.save(byte_io, format='png')
    buffer = byte_io.getvalue()
    byte_io.close()
    return buffer
