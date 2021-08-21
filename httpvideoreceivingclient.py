import cv2
import numpy as np
import urllib.request


url = 'http://127.0.0.1:5000/video_feed'

#camera = cv2.VideoCapture(0)

while True:
   #print('Getting image')
    req = urllib.request.Request(url)


    with urllib.request.urlopen(req) as resp:
        data = resp.read()

        #print('Got data')
        #print(type(data))


    # Numpy to convert into a array

    #print('Got image')
    # Finally decode the array to OpenCV usable format ;)
    #imgTest = cv2.imdecode(imgNp, -1)
    #imgTest = cv2.resize(imgTest, (640, 480))

    #imgTest = cv2.flip(imgTest, 1)

    imgNp = np.array(bytearray(data), dtype=np.uint8)
    imgTest = cv2.imdecode(imgNp, -1)

    imgTest = cv2.resize(imgTest, (640, 480))

    cv2.imshow("Video", imgTest)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break