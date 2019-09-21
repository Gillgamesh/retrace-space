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
from nltk import tokenize
import nltk
nltk.download('punkt')
import re

client = vision.ImageAnnotatorClient()


def detect_text(image):
    buf = io.BytesIO()
    image.save(buf, "JPEG")
    image = vision.types.Image(content=buf.getvalue())
    response = client.text_detection(image=image)
    texts = response.text_annotations
    retstr = '\n"{}"'.format(texts[0].description.encode('ascii', 'ignore'))
    return retstr


def screendata():
    image = pyautogui.screenshot()
    client = vision.ImageAnnotatorClient()
    finalstr = detect_text(image)
    # Instantiates a client
    client = language.LanguageServiceClient()
    a = tokenize.sent_tokenize(re.sub('\n', " .", finalstr))
    filter(
        lambda x: re.match('(([a-zA-Z1-9])+(\s)*)*', x),
        a
    )
    magnitude = []
    scores = []
    for final in a:
        document = types.Document(
            content=final,
            type=enums.Document.Type.PLAIN_TEXT)
        # Detects the sentiment of the text
        sentiment = client.analyze_sentiment(document=document).document_sentiment
        magnitude.append(abs(sentiment.score))
        scores.append(sentiment.score)
    sents = sorted(zip(magnitude, scores, a), key=lambda x: x[0], reverse=True)[:3]
    return sents

