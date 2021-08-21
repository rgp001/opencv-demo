from flask import Flask, stream_with_context, render_template, Response
import cv2
#Initialize the Flask app
app = Flask(__name__)

#camera = cv2.VideoCapture(0)

def gen_frames():
    success, frame = camera.read()  # read the camera frame
    if not success:
        pass
    else:
        frame = cv2.flip(frame, 1)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield frame
        #yield (b'--frame\r\n'
         #      b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')
    #return gen_frames()

if __name__ == "__main__":
    app.run(debug=True)
