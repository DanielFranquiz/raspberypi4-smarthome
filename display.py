#libraries
import time
import proximity
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess

RST = 0

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()     #Initialize the library
disp.clear()     #clear display
disp.display()

#sets the size of the display
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

# displays text and position
disp.clear()
disp.display()
draw.text((x, top),       "Hello!" ,  font=font, fill=255)
draw.text((x, top+8),     "Please wait a moment", font=font, fill=255)
draw.text((x, top+16),    "while we contact",  font=font, fill=255)
draw.text((x, top+25),    "the homeowner",  font=font, fill=255)

# open method used to open different extension image file
# for this project this was not used 
im = Image.open(r"/home/pi/Desktop/dog.png")  

# Display image. The display feature was not used
disp.image(image1)
disp.display()
#we displayed our communication to the visitor for 5 sec
time.sleep(5)
# this command turns off the display after the sleep for 5 sec
disp.command(Adafruit_SSD1306.SSD1306_DISPLAYOFF)

