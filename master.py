import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import RPi.GPIO as GPIO
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # Sets the pin numbering system to use the physical layout

RST = 0

# Set up pin 11 for PWM
GPIO.setup(23,GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
p = GPIO.PWM(23, 50)     # Sets up pin 11 as a PWM pin
p.start(0)               # Starts running PWM on the pin and sets it to 0
# Sets up pin 18 as an input
GPIO.setup(18, GPIO.IN, GPIO.PUD_UP)

# Detects the button being pressed
def waitButton():
    GPIO.wait_for_edge(24, GPIO.RISING)
    print('Button pressed!')

def ping():
	#"""Get reading from HC-SR04"""
	GPIO.setmode(GPIO.BOARD)
	 
	TRIG = 8 
	ECHO = 6
	 
	GPIO.setup(TRIG,GPIO.OUT)
	GPIO.setup(ECHO,GPIO.IN)
	 
	GPIO.output(TRIG, False)
	time.sleep(1)
	 
	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)
	 
	while GPIO.input(ECHO)==0:
	  pulse_start = time.time()
	 
	while GPIO.input(ECHO)==1:
	  pulse_end = time.time()
	 
	pulse_duration = pulse_end - pulse_start
	 
	distance = pulse_duration * 17150
	 
	distance = round(distance, 2)
	 
	print ("Distance:",distance,"cm")
	 
	GPIO.cleanup()

print ("Reading Distance \n")

while True:
	ping()

# Runs function
waitButton()

# Move the servo back and forth
p.ChangeDutyCycle(3)     # Changes the pulse width to 3 (so moves the servo)
sleep(1)                 # Wait 1 second
p.ChangeDutyCycle(12)    # Changes the pulse width to 12 (so moves the servo)
sleep(1)

# Clean up everything
p.stop()                 # At the end of the program, stop the PWM
GPIO.cleanup()           # Resets the GPIO pins back to defaults

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height

image1 = Image.new('1', (width, height))

draw = ImageDraw.Draw(image1)
draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = -2
top = padding

bottom = height-padding
x = 0
font = ImageFont.load_default()

# Write two lines of text.

disp.clear()
disp.display()
draw.text((x, top),       "Welcome!" ,  font=font, fill=255)
draw.text((x, top+8),     "This is your ", font=font, fill=255)
draw.text((x, top+16),    "Smart home",  font=font, fill=255)
draw.text((x, top+25),    "Here for your",  font=font, fill=255)
draw.text((x, top+34),    "assistance =)",  font=font, fill=255)

# open method used to open different extension image file 
im = Image.open(r"/home/pi/Desktop/dog.png")  
  
# This method will show image in any image viewer  
im.show()  

# Display image.
disp.image(image1)
disp.display()
time.sleep(5)

if disp.height == 64:
   image = Image.open('/home/pi/Desktop/luigi.png').convert('1')
else:
   image = Image.open('/home/pi/Desktop/luigi.png').convert('1')

disp.image(image)
disp.display()
time.sleep(2)

if disp.height == 64:
   image = Image.open('img3.jpg').convert('1')
else:
   image = Image.open('img3.jpg').convert('1')




