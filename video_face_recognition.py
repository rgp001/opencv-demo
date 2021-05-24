import cv2
import numpy as np
import face_recognition
import urllib.request
import time

sources = {
    'Prasad': 'Prasad.jpg'
}

sourceImages = {}

sourceEncodings = {}

for k, v in sources.items():
    imgOriginal = face_recognition.load_image_file(v)
    imgOriginal = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2RGB)
    sourceImages[k] = imgOriginal
    faceLoc = face_recognition.face_locations(imgOriginal)[0]
    encodeFace = face_recognition.face_encodings(imgOriginal)[0]
    sourceEncodings[k] = encodeFace
    # cv2.rectangle(imgOriginal, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)

    img = cv2.resize(imgOriginal, (640, 480))
    # cv2.imshow(k, img)

# cap = cv2.VideoCapture(0)
#
# cap.set(3, 630)
# cap.set(4, 480)
#
# #set brightness
# cap.set(10,100)

url = 'http://192.168.0.105:8080/shot.jpg'


def webcam_video(url):
    while True:
        # Use urllib to get the image from the IP camera

        imgResp = urllib.request.urlopen(url)

        # Numpy to convert into a array
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)

        # Finally decode the array to OpenCV usable format ;)
        imgTest = cv2.imdecode(imgNp, -1)
        imgTest = cv2.resize(imgTest, (640, 480))

        imgTest = cv2.flip(imgTest, 1)

        # print('sending')

        # cv2.imshow("Video", imgTest)

        yield imgTest


def coroutine(func):
    def start(*args, **kwargs):
        _g = func(*args, **kwargs)
        print('start')
        next(_g)
        return _g

    return start


@coroutine
def identify_face():
    while True:
        imgReceived = (yield)
        # print('received')

        faceLocations = face_recognition.face_locations(imgReceived)
        # print('Found ', len(faceLocations), ' faces')

        locationToNameMap = {}

        for faceLocTest in faceLocations:
            top, right, bottom, left = faceLocTest
            # print(faceLocTest)
            #
            # cv2.rectangle(imgTest, (left+10, top+10), (right+10, bottom+10), (255, 0, 0), 2)
            face_image = imgReceived[top:bottom, left:right]
            encodeTestFace = face_recognition.face_encodings(face_image)
            # print(encodeTestFace)
            # print('Searching face')

            encodings = list(sourceEncodings.values())
            names = list(sourceEncodings.keys())

            if len(encodeTestFace) == 0:
                continue

            distances = face_recognition.face_distance(encodings, encodeTestFace[0])
            # print(distances)

            maxDistance = 1
            i = 0
            name = ''

            for distance in distances:
                if distance <= maxDistance:
                    name = names[i]
                    maxDistance = distance
                i += 1
            if face_recognition.compare_faces([sourceEncodings.get(name)], encodeTestFace[0])[0]:
                # print('Trying for ', name)
                locationToNameMap[faceLocTest] = name
            else:
                locationToNameMap[faceLocTest] = 'Unknown'

            for k, v in locationToNameMap.items():
                top, right, bottom, left = k
                cv2.rectangle(imgReceived, (left, top), (right, bottom), (255, 0, 0), 3)
                cv2.putText(imgReceived, v, (left, top), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 3)

                cv2.rectangle(imgReceived, (left, top), (right, bottom), (255, 0, 0), 3)
                cv2.putText(imgReceived, v, (left, top), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 3)

        cv2.imshow("Video", imgReceived)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    video = webcam_video(url)

    face_detector = identify_face()
    for image in video:
        face_detector.send(image)
