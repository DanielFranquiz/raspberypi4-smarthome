# libraries
import cv2
import sys
import RPi.GPIO as GPIO
from mail import sendEmail
from flask import Flask, render_template, Response
from camera import VideoCamera
from proximity import distance
from flask_basicauth import BasicAuth
import time
import threading

email_update_interval = 7 # sends an email only once in this time interval
video_camera = VideoCamera(flip=False) # creates a camera object, flip vertically
object_classifier = cv2.CascadeClassifier("models/facial_recognition_model.xml") # an opencv classifier

# App Globals this is what the user will input when first accessing
# the stream
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'user'
app.config['BASIC_AUTH_PASSWORD'] = 'pass'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)
# epoch:- beginning of time
last_epoch = 0

# This function contains the 
def check_for_objects():
	global last_epoch
        # infinite loop
	while True:
		try:
			frame, found_obj = video_camera.get_object(object_classifier)
			# time() :- number of seconds elapsed since the epoch
			if found_obj and (time.time() - last_epoch) > email_update_interval:
				last_epoch = time.time()
				print ("Sending email...")
				sendEmail(frame)
				print ("done!")
		except:
			print ("Error sending email: "), sys.exc_info()[0]

# trigger for the html stream
@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')

# border for the camera
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# what is put in the frame on the stream
@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# function for the servo motor
def execute_servo():
    while True:    
        exec(open('servo.py').read())
        time.sleep(1)
        GPIO.cleanup()

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            if dist < 1208.6:      
                # print ("Measured Distance = %.1f cm" % dist)
                time.sleep(1)
	    # this will be the trigger to activate camera/"wake" device
            # If a hand is waved in front of the proximity, this will trigger
            if dist < 100.0:
                # terminal message for functionality check
                print ("Proximity triggered")
                # this is for multi-threading
                # starts the stream
                import display
                t1 = threading.Thread(target=check_for_objects, args=())
                t1.daemon = True
                t1.start()
                app.run(host='0.0.0.0', debug=False)

                # executes servo motor
                t2 = threading.Thread(target=execute_servo, args=())
                t2.daemon = True
                t2.start()
            else:
                # test for when nothing is directly in front of proximity sensor
                print ("Nothing yet")
                # pauses the program for 2 sec
                time.sleep(2)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Stopped by User")
        # resets ports to input. prevents damage from a short circuit
        GPIO.cleanup()



