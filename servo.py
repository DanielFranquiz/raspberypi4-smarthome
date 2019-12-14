# Set up libraries and overall settings
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program
GPIO.setmode(GPIO.BCM) # Sets the pin numbering system to use the physical layout

# Set up pin 11 for PWM
GPIO.setup(17,GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
p = GPIO.PWM(17, 50)     # Sets up pin 11 as a PWM pin 50 frequency Hz
p.start(0)               # Starts running PWM on the pin and sets it to 0
# Sets up pin 18 as an input
GPIO.setup(24, GPIO.IN, GPIO.PUD_UP) #pin 18

# Detects the button being pressed
def waitButton():
    GPIO.wait_for_edge(24, GPIO.RISING) #pin 18
    print('Button pressed!')
    time.sleep(1)

# Runs function
waitButton()


# Move the servo back and forth
p.ChangeDutyCycle(3)     # Changes the pulse width to 3 (so moves the servo)
sleep(3)                 # Wait 3 seconds
p.ChangeDutyCycle(12)    # Changes the pulse width to 12 (so moves the servo)
sleep(1)
    
# Clean up everything
p.stop()                 # At the end of the program, stop the PWM
GPIO.cleanup()           # Resets the GPIO pins back to defaults



