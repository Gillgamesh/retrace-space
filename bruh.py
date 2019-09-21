import io
import cv2
from PIL import Image
import time
from google.cloud import vision
from google.cloud.vision import types
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)


def detect_text(content):

    image = types.Image(content=content)
    response = client.face_detection(image=image)
    faces = response.face_annotations

    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')
    for face in faces:
        print(face)
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))


if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False
# Instantiates a client
client = vision.ImageAnnotatorClient()


while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    file = cv2.imencode('.jpg', frame)[1].tostring()
    sleeptime = 10
    if sleeptime > 0:
        time.sleep(sleeptime)
    print(detect_text(file))

cv2.destroyWindow("preview")
