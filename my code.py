import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import speech_recognition as sr
from gtts import gTTS
import os
import RPi.GPIO as GPIO
from datetime import datetime
predict=21
repete=20 
GPIO.setmode(GPIO.BCM)
GPIO.setup(predict, GPIO.IN)
GPIO.setup(repete, GPIO.IN)
cap = cv2.VideoCapture(0)
labels = []
bool=True
predict1=False
res = []

def speechToText():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            string = r.recognize_google(audio)
            print(string)
            return string
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            
def getTime():
    current_time = datetime.now().time()
    formatted_time = current_time.strftime("%I:%M:%p")
    return formatted_time           

def speech(labels):
    object_list = ""
    for item in range(0, len(labels)):
        if item == len(labels) - 1:
            object_list += labels[item]
        else:
            object_list += labels[item] + " and "
    if len(labels) == 0:
        mytext = f"no object is present in front of you."
    else:
        mytext = f"Their is {object_list} present in front of you."
    print(mytext)
    tts=gTTS(text=mytext,lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")
    
def text_to_speech(mytext):
    tts=gTTS(text=mytext,lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")


while True:
    if(bool):
        os.system("mpg321 beep.mp3")
        bool=False
    ret, frame = cap.read()
    cv2.imshow("output",frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cv2.waitKey(1) & 0xFF == ord('m') or GPIO.input(predict) == 0 or predict1:
        res=[]
        os.system("mpg321 beep.mp3")
        bbox, label, conf = cv.detect_common_objects(frame)
        output_image = draw_bbox(frame, bbox, label, conf)
        for item in label:
            if item in labels:
                pass
            else:
               labels.append(item)
        
        [res.append(x) for x in labels if x not in res]
        print(res)
        speech(res)
        labels = []
        predict1=False

    if cv2.waitKey(1) & 0xFF == ord('r') or GPIO.input(repete) == 0:
        os.system("mpg321 beep.mp3")
        print(res)
        speech(res)
        
    if cv2.waitKey(1) & 0xFF == ord('s'):
        os.system("mpg321 beep.mp3")    
        string = speechToText()
        if "time" in string:
            t = getTime()
            text_to_speech(t)
        if "predict" in string:    
            predict1=True
            continue
        if "repeat" in string:    
            os.system("mpg321 beep.mp3")
            print(res)
            speech(res)
