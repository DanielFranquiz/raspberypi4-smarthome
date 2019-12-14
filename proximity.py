#Libraries
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM) references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 18
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT) # Trigger
GPIO.setup(GPIO_ECHO, GPIO.IN)     # Echo
 
def distance():
    # set Trigger to LOW and wait 0.5 sec to give module time to settle
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(0.5)
 
    # set Trigger after 0.01ms to LOW. sends the 10ms trigger pulse to 
    #Trigger pin, then module will send the output to Echo pin
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
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
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            if dist < 1208.6:      
                #print ("Measured Distance = %.1f cm" % dist)
                time.sleep(1)
	    #this will be the trigger to activate camera/"wake" device
            if dist < 100.0:
                print ("Object or person is near your door!")
            else:
                print ("Out of range!")
                time.sleep(2)
                
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()