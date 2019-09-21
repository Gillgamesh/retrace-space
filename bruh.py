import io
import cv2
from PIL import Image
import time
from google.cloud import vision
from google.cloud.vision import types
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)
if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else: rval = False
# Instantiates a client
client = vision.ImageAnnotatorClient()
starttime=time.time()
counter = 0
def detect_text(path):
    """Detects text in the file."""
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.face_detection(image=image)
    faces = response.face_annotations

    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')
    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    file = 'live' + str(counter) + '.png'
    if key == 27: # exit on ESC
        break
        file = 'live' + str(counter) + '.png'
    cv2.imwrite( file,frame)
    # print OCR text
    print(detect_text(file))
    counter += 1
    time.sleep(10.0 - ((time.time() - starttime) % 10.0))

cv2.destroyWindow("preview")
