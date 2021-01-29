from picamera import PiCamera
from time import sleep
from io import BytesIO
import requests

url = 'https://nadejde-collector-api.azurewebsites.net/api/collections/Panini - Football 2020/numbers/detect'


camera = PiCamera()
camera.rotation = 180
camera.resolution = (640, 480)
camera.start_preview()

def post_media(image_bytes, collection):

    resp = requests.post('https://nadejde-collector-api.azurewebsites.net/api/collections/'+collection+'/numbers/detect',
                        files={'file': ("image.jpeg", image_bytes.getvalue(), 'image/jpeg')})

    resp.raise_for_status()
    return resp.json()

def get_sticker_number(collection):
    my_stream = BytesIO()
    camera.capture(my_stream, 'jpeg')
    numbers = post_media(my_stream, collection)
    if (len(numbers) > 0):
        return numbers[0]
    else:
        return None

def stop():
    camera.stop_preview()