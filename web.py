import numpy as np
import face_recognition
import cv2
import os
from datetime import datetime

def talk(words): #function to synthesize human-like speech
	try:
		print(words)
		os.system("cd ~")
		os.system(f'bash speech.sh "{words}"')
	except ValueError:
		print("Error")

path = 'KnownFaces'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

for cls in myList:
    curImg = cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    classNames.append(os.path.splitext(cls)[0])

#print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open("Attendance.csv", "r+") as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime("%H:%M:%S")
            f.writelines(f'\n{name}, {dtString}')

encodeListKnown = findEncodings(images)
print("Декодирование закончено")

cap = cv2.VideoCapture(0)

cv2.destroyAllWindows()
while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex]
            talk(f"Привет, {name}")
            markAttendance(name)
    if cv2.waitKey(1) & 0xFF == 27:
        cv2.destroyAllWindows()
        break

    cv2.imshow("WebCam", img)

cv2.destroyAllWindows()
   