import RPi.GPIO as GPIO
import pyaudio
from numpy import linspace,sin,pi,int16
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
import time
 
RATE = 4400
FREQ = 261.6

GPIO.setmode(GPIO.BCM)
 
GPIO_TRIGGER = 23
GPIO_ECHO = 18
 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)

pa = pyaudio.PyAudio()
s = pa.open(output=True,
            channels=2,
            rate=RATE,
            format=pyaudio.paInt16,
            output_device_index=2)

 
def distance():
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def note(freq, len, amp=5, rate=44100):
   t = linspace(0,len,len*rate)
   data = sin(2*pi*freq*t)*amp
   return data.astype(int16) # two byte integers
 
if _name_ == '_main_':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            if ( dist > 20 ):
                FREQ=261
            elif (dist > 10):
                FREQ=350
            else: 
                FREQ=600
            tone = note(FREQ, 1, amp=10000, rate=RATE)
            with canvas(device) as draw:
                draw.rectangle(device.bounding_box, outline="white", fill="black")
                draw.text((10, 40), "Distance = %.1f cm"%dist, fill="white")
            s.write(tone)
            #time.sleep(0.20)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()