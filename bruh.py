from screenshot import screendata
import io
import cv2
from PIL import Image
import datetime
import time
import json
import threading
from google.cloud import vision
from google.cloud.vision import types
# cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)


def detect_text(content):
    image = types.Image(content=content)
    response = client.face_detection(image=image)
    faces = response.face_annotations

    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    emotion = ""
    for face in faces:
        if face.anger_likelihood >= 4:
            emotion = "Anger"
        elif face.joy_likelihood >= 4:
            emotion = "Joy"
        elif face.sorrow_likelihood >= 4 :
            emotion = "Sorrow"
        elif face.surprise_likelihood >= 4:
            emotion = "Surprise"
    return emotion


if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False
# Instantiates a client

client = vision.ImageAnnotatorClient()
final_results = []


def update():
    rval, frame = vc.read()
    while (rval):
        try:
            # press 'q' to exit
            # cv2.imshow("preview", frame)
            rval, frame = vc.read()
            file = cv2.imencode('.jpg', frame)[1].tostring()
            expression = detect_text(file)
            if (expression != ""):
                textinfo = screendata()
                if (len(textinfo) >= 3):
                    json_dict = {
                        "expression": {
                            "emotion": expression,
                            "magnitude1": textinfo[0][0],
                            "message1": textinfo[0][2],
                            "magnitude2": + textinfo[1][0],
                            "message2": textinfo[1][2],
                            "magnitude3": textinfo[2][0],
                            "message3": textinfo[2][2],
                            "time": datetime.datetime.now().isoformat()
                        }
                    }
                    final_results.append(json_dict)
                for i in range(40):
                    time.sleep(0.1)
        except (KeyboardInterrupt):
            return


update()
with open('./client/src/data.json', 'w') as fp:
    json.dump(final_results, fp, indent=4, sort_keys=True)
print(final_results)
# cv2.destroyWindow("preview")
