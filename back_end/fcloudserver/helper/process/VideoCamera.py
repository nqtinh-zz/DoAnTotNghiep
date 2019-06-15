import threading

import cv2
from django.http import StreamingHttpResponse
from django.views.decorators import gzip

from utils.result import Result


class VideoCamera(object):
    def __init__(self, stream_url):
        self.video = cv2.VideoCapture(stream_url)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera, request):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def livefe(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera(request.GET['stream_url']), request),
                                     content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        return Result.failed(
            message='Have some problems!'
        )
