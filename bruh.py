import io
import cv2
from PIL import Image
import time
from google.cloud import vision
from google.cloud.vision import types
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)
from screenshot import screendata

def detect_text(content):
    image = types.Image(content=content)
    response = client.face_detection(image=image)
    faces = response.face_annotations

    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    emotion = ""
    for face in faces:
        if face.anger_likelihood >= 4:
            emotion = "anger"
        elif face.joy_likelihood >= 4:
            emotion = "joy"
        elif face.sorrow_likelihood >= 4 :
            emotion = "sorrow"
        elif face.surprise_likelihood >= 4:
            emotion = "surprise"
    return emotion

if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False
# Instantiates a client

client = vision.ImageAnnotatorClient()
if rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    file = cv2.imencode('.jpg', frame)[1].tostring()
    expression = detect_text(file)

if (expression != ""):
    textinfo = screendata()
    json_string = """
    {
    "expression": {
        "emotion":""" + expression +  """,
        "magnitude1":""" + textinfo[0][0] + """,
        "message1":""" + textinfo[0][2] + """,
        "magnitude2":""" + textinfo[1][0] + """,
        "message2":""" + textinfo[1][2] + """,
        "magnitude2":""" + textinfo[2][0] + """,
        "message2":""" + textinfo[2][2] + """,
        }
        """
    data = json.loads(json_string)
    print data
    
cv2.destroyWindow("preview")
