import numpy as np
import pyautogui
import imutils
import io
import cv2
from PIL import Image
import time
from google.cloud import vision
from google.cloud.vision import types
# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import nltk
nltk.download('punkt')
from nltk import tokenize
import re

client = vision.ImageAnnotatorClient()

def detect_text(image):

    with io.open("in_memory_to_disk.png", 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    retstr = '\n"{}"'.format(texts[0].description.encode('ascii', 'ignore'))
    return retstr

def screendata():
    # take a screenshot of the screen and store it in memory, then
    # convert the PIL/Pillow image to an OpenCV compatible NumPy array
    # and finally write the image to disk
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite("in_memory_to_disk.png", image)
    # this time take a screenshot directly to disk
    pyautogui.screenshot("straight_to_disk.png")	
    client = vision.ImageAnnotatorClient()
    finalstr = detect_text(image)
    # Instantiates a client
    client = language.LanguageServiceClient()
    a = tokenize.sent_tokenize(re.sub('\n', " .", finalstr))
    magnitude = []
    scores = []
    magnitude2 = []
    for final in a:
        #print(final)
        document = types.Document(
            content= final,
            type=enums.Document.Type.PLAIN_TEXT)
        # Detects the sentiment of the text
        sentiment = client.analyze_sentiment(document=document).document_sentiment
        magnitude.append(abs(sentiment.score) * sentiment.magnitude)
        scores.append(sentiment.score)
        sents = sorted(zip(magnitude, scores, a), key=lambda x: x[0], reverse = True)[:3]
        return sents[0][0]
    
